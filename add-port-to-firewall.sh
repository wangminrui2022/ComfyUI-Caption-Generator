#!/bin/bash

# Function to add port to firewall
add_port_to_firewall() {
    # Enable ufw (if not already enabled)
    sudo ufw enable > /dev/null 2>&1

    # Prompt user for port number
    read -p "Enter the port number to add to firewall (or type 'quit' to exit): " port

    # Check if user wants to quit
    if [ "$port" = "quit" ]; then
        echo "Exiting..."
        exit 0
    fi

    # Validate port number
    if ! [[ "$port" =~ ^[0-9]+$ ]]; then
        echo "Error: Invalid port number. Please enter a valid integer port number."
        add_port_to_firewall
        return
    fi

    # Allow incoming traffic on specified port
    sudo ufw allow $port > /dev/null 2>&1

    # Optionally, you can reload ufw to apply changes
    sudo ufw reload > /dev/null 2>&1

    echo "Port $port added to firewall"
    echo

    # Display current ufw status
    echo "Current ufw status:"
    sudo ufw status verbose
    echo

    # Call the function recursively to allow adding more ports without restarting
    add_port_to_firewall
}

# Call the function to start adding ports to firewall
add_port_to_firewall

