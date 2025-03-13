import requests
import json
import socket
import netifaces
from typing import Dict, Optional

class AppIPAddress:
    def __init__(self):
        self.ip_apis = [
            "http://icanhazip.com",
            "https://ipapi.co/json/",
            "http://ifconfig.me/ip",
            "https://checkip.amazonaws.com/",
            "http://api.ip.sb/ip",
            "https://ipecho.net/plain",
            "http://whatismyipaddress.com/api",
            "https://ident.me/",
            "https://api.ipify.org?format=json",
            "https://api.myip.com",            
        ]
        self.vpn_check_apis = [
            "http://ip-api.com/json/{ip}",
            "https://ipinfo.io/{ip}/json",  # 需要token以获得完整功能
            "https://api.iplocation.net/?ip={ip}",
            "https://vpnapi.io/api/{ip}"    # 专业VPN检测API，需要免费API key
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        # 可选：添加vpnapi.io的API key（注册后获取）
        self.vpnapi_key = "YOUR_VPNAPI_IO_KEY"  # 替换为您的key或留空

    def get_public_ip(self) -> Optional[str]:
        for api in self.ip_apis:
            try:
                response = requests.get(api, headers=self.headers, timeout=10)
                response.raise_for_status()
                if "ipify" in api:
                    return response.json().get("ip")
                elif "myip" in api:
                    return response.json().get("ip")
                elif "ipapi" in api:
                    return response.json().get("ip")
                else:
                    return response.text.strip()
            except requests.RequestException as e:
                #print(f"尝试 {api} 获取公网IP失败: {e}")
                print(f"Failed to get public IP using {api}: {e}")
                continue
        #print("所有API尝试均失败")
        print("All API attempts failed")
        return None

    def get_router_ip(self) -> Optional[str]:
        try:
            gateways = netifaces.gateways()
            default_gateway = gateways.get('default', {}).get(netifaces.AF_INET)
            return default_gateway[0] if default_gateway else None
        except Exception as e:
            #print(f"获取路由器IP失败: {e}")
            print(f"Failed to get router IP: {e}")
            return None

    def check_vpn_proxy(self, ip: str, router_ip: Optional[str] = None) -> Dict[str, any]:
        result = {
            "ip": ip,
            "is_vpn_or_proxy": False,
            "country": None,
            "isp": None,
            "proxy": False,
            "hosting": False,
            "error": None,
            "additional_checks": {}
        }
        
        for api in self.vpn_check_apis:
            try:
                url = api.format(ip=ip)
                if "vpnapi.io" in api and self.vpnapi_key != "YOUR_VPNAPI_IO_KEY":
                    url += f"?key={self.vpnapi_key}"
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                api_name = api.split('/')[2]
                if "ip-api.com" in api:
                    if data.get("status") == "success":
                        result["country"] = data.get("country")
                        result["isp"] = data.get("isp")
                        result["proxy"] = data.get("proxy", False)
                        result["hosting"] = data.get("hosting", False)
                        result["is_vpn_or_proxy"] = result["is_vpn_or_proxy"] or (data.get("proxy", False) or data.get("hosting", False))
                elif "ipinfo.io" in api:
                    result["additional_checks"]["ipinfo"] = {
                        "org": data.get("org"),
                        "country": data.get("country")
                    }
                    if "vpn" in data.get("org", "").lower():
                        result["is_vpn_or_proxy"] = True
                elif "iplocation.net" in api:
                    result["additional_checks"]["iplocation"] = {
                        "isp": data.get("isp"),
                        "country": data.get("country_name")
                    }
                elif "vpnapi.io" in api:
                    result["additional_checks"]["vpnapi"] = {
                        "vpn": data.get("security", {}).get("vpn", False),
                        "proxy": data.get("security", {}).get("proxy", False),
                        "tor": data.get("security", {}).get("tor", False)
                    }
                    if data.get("security", {}).get("vpn", False):
                        result["is_vpn_or_proxy"] = True
                
            except requests.RequestException as e:
                #result["error"] = f"检查VPN/代理失败 ({api}): {e}"
                result["error"] = f"VPN/Proxy check failed ({api}): {e}"
                continue
        
        # 对比公网IP和路由器IP的国家
        if router_ip and result["country"]:
            try:
                router_data = requests.get(
                    self.vpn_check_apis[0].format(ip=router_ip),
                    headers=self.headers,
                    timeout=10
                ).json()
                router_country = router_data.get("country")
                if router_country and router_country != result["country"]:
                    result["is_vpn_or_proxy"] = True
                    result["additional_checks"]["country_mismatch"] = {
                        "public_ip_country": result["country"],
                        "router_ip_country": router_country
                    }
            except Exception as e:
                #result["error"] = result["error"] + f" | 路由器IP检查失败: {e}" if result["error"] else f"路由器IP检查失败: {e}"
                result["error"] = result["error"] + f" | Router IP check failed: {e}" if result["error"] else f"Router IP check failed: {e}"
        
        return result

    def compare_ips(self) -> Dict[str, any]:
        public_ip = self.get_public_ip()
        router_ip = self.get_router_ip()
        #所有API尝试均失败
        if(public_ip==None or router_ip==None):
            return None

        result = {
            "public_ip": public_ip,
            "router_ip": router_ip,
            "is_same_network": False,
            "vpn_check": None,
            "error": None
        }
        
        if not public_ip:
            #result["error"] = "无法获取公网IP"
            result["error"] = "Unable to get public IP"
        if not router_ip:
            #result["error"] = result["error"] + " | 无法获取路由器IP" if result["error"] else "无法获取路由器IP"
            result["error"] = result["error"] + " | Unable to get router IP" if result["error"] else "Unable to get router IP"
        
        if public_ip and router_ip:
            public_prefix = '.'.join(public_ip.split('.')[:-1])
            router_prefix = '.'.join(router_ip.split('.')[:-1])
            result["is_same_network"] = (public_prefix == router_prefix)
            result["vpn_check"] = self.check_vpn_proxy(public_ip, router_ip)
        
        return result

    def is_restricted_country(self,data):
        # 定义受限制国家的 ISO 代码列表
        restricted_countries = {
            "KP",  # 朝鲜
            "RU",  # 俄罗斯
            "VE",  # 委内瑞拉
            "SO",  # 索马里
            "LY",  # 利比亚
            "CU",  # 古巴
            "SD",  # 苏丹
            "CD",  # 刚果民主共和国
            "SS",  # 南苏丹
            "BY",  # 白俄罗斯
            "ZW",  # 津巴布韦
            # 中东国家
            "AF",  # 阿富汗
            "BH",  # 巴林
            "IR",  # 伊朗
            "IQ",  # 伊拉克
            "IL",  # 以色列
            "JO",  # 约旦
            "KW",  # 科威特
            "LB",  # 黎巴嫩
            "OM",  # 阿曼
            "QA",  # 卡塔尔
            "SA",  # 沙特阿拉伯
            "SY",  # 叙利亚
            "TR",  # 土耳其
            "AE",  # 阿联酋
            "YE",  # 也门
            "PS",  # 巴勒斯坦
            # 东南亚国家
            "BN",  # 文莱
            "KH",  # 柬埔寨
            "ID",  # 印度尼西亚
            "LA",  # 老挝
            "MY",  # 马来西亚
            "MM",  # 缅甸
            "PH",  # 菲律宾
            "SG",  # 新加坡
            "TH",  # 泰国
            "TL",  # 东帝汶
            "VN",  # 越南   
        }
        # 提取国家代码
        country_code = data["vpn_check"]["additional_checks"]["ipinfo"]["country"]
        # 判断是否在受限制国家列表中
        if country_code.upper() in restricted_countries:
            print(f"Warning: Restricted Country Detected（{country_code}）！")#警告：检测到受限制国家
            return True
        else:
            print(f"Security: No restricted countries detected. Current country code:{country_code}")#安全：未检测到受限制国家。当前国家代码：
            return False

def main():
    ip_checker = AppIPAddress()
    #IP对比结果
    result = ip_checker.compare_ips()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(result["vpn_check"]["additional_checks"]["ipinfo"])
    # 测试代码
    r = ip_checker.is_restricted_country(result)
    print("是否属于受限地区:", r)  # 输出: 是否属于受限地区: True

if __name__ == "__main__":
    main()