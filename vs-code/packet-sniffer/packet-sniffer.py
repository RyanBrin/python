"""
Project: Packet Sniffer
Author: Ryan Brinkman
Date: February 20, 2025
GitHub Repository: https://github.com/RyanBrin/python/tree/main/vs-code/packet-sniffer/
"""

import scapy

def main ():
    print("Packet Sniffer")
    print("1. Capture packets")
    print("2. Display packets")
    print("3. Exit")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        print("Capturing packets...\n")
        #capture_packets()
    elif choice == "2":
        print("Displaying packets...\n")
        #display_packets()
    elif choice == "3":
        print("Exiting...\n")
        exit()
    else:
        print("Invalid choice. Please try again.\n")

while True:
    main()