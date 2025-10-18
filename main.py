#!/usr/bin/env python3
"""
Ticket Booking Queue System
Features:
 - FIFO normal queue
 - VIP queue (priority)
 - Enqueue, Dequeue, Display
 - Estimate waiting time per customer
 - Save / Load queue to JSON (persistence)
Simple CLI interface for VS Code terminal.
"""

import json
import os
from collections import deque
from datetime import datetime

DATA_FILE = "queue_data.json"

class TicketQueue:
    def __init__(self, avg_service_time=5):
        # avg_service_time in minutes
        self.vipQueue = deque()
        self.normalQueue = deque()
        self.avg_service_time = avg_service_time

    # Add a customer (dict contains at least name and timestamp)
    def enqueue(self, name, vip=False):
        customer = {
            "name": name,
            "time": datetime.now().isoformat()
        }
        if vip:
            self.vipQueue.append(customer)
        else:
            self.normalQueue.append(customer)
        return customer

    # Remove next customer (VIP served first)
    def dequeue(self):
        if self.vipQueue:
            return self.vipQueue.popleft()
        elif self.normalQueue:
            return self.normalQueue.popleft()
        else:
            return None

    # Display all waiting customers in order of service
    def display(self):
        print("\n--- Current Waiting List ---")
        if not self.vipQueue and not self.normalQueue:
            print("[No customers waiting]")
            return
        # VIP section
        if self.vipQueue:
            print("VIP Queue:")
            for i, c in enumerate(self.vipQueue, start=1):
                print(f"  {i}. {c['name']} (joined: {c['time']})")
        # Normal section
        if self.normalQueue:
            print("Normal Queue:")
            for i, c in enumerate(self.normalQueue, start=1):
                print(f"  {i}. {c['name']} (joined: {c['time']})")
        print("----------------------------\n")

    # Get queue size (total)
    def size(self):
        return len(self.vipQueue) + len(self.normalQueue)

    # Estimate wait time in minutes for a given customer name
    def estimate_wait_time(self, name):
        # Search VIP queue
        vip_list = list(self.vipQueue)
        normal_list = list(self.normalQueue)

        for idx, c in enumerate(vip_list):
            if c["name"].lower() == name.lower():
                # customers ahead are idx (0-based)
                return idx * self.avg_service_time

        for idx, c in enumerate(normal_list):
            if c["name"].lower() == name.lower():
                # all VIP ahead + position in normal
                ahead = len(vip_list) + idx
                return ahead * self.avg_service_time

        return None  # not found

    # Save queues to JSON file
    def save_to_file(self, filename=DATA_FILE):
        data = {
            "vip": list(self.vipQueue),
            "normal": list(self.normalQueue),
            "avg_service_time": self.avg_service_time
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return filename

    # Load queues from JSON file (overwrites current queues)
    def load_from_file(self, filename=DATA_FILE):
        if not os.path.exists(filename):
            return False
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.vipQueue = deque(data.get("vip", []))
        self.normalQueue = deque(data.get("normal", []))
        self.avg_service_time = data.get("avg_service_time", self.avg_service_time)
        return True

# --- CLI Interface ---
def print_menu():
    print("""
Ticket Queue System - Commands:
1. add         -> Add a normal customer
2. addvip      -> Add a VIP customer
3. serve       -> Serve next customer (dequeue)
4. list        -> Display waiting list
5. size        -> Show total customers waiting
6. estimate    -> Estimate waiting time for a customer
7. save        -> Save queue to file
8. load        -> Load queue from file
9. settime     -> Set average service time (minutes per customer)
0. quit        -> Exit
""")

def main():
    tq = TicketQueue(avg_service_time=5)

    # auto-load if file exists
    if os.path.exists(DATA_FILE):
        loaded = tq.load_from_file()
        if loaded:
            print(f"[Loaded saved queues from {DATA_FILE}]")

    print("Welcome to the Ticket Booking Queue System (CLI)")
    print_menu()

    while True:
        cmd = input("Enter command: ").strip().lower()
        if cmd in ("1", "add"):
            name = input("Customer name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            tq.enqueue(name, vip=False)
            print(f"Added normal customer: {name}")

        elif cmd in ("2", "addvip"):
            name = input("VIP name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            tq.enqueue(name, vip=True)
            print(f"Added VIP customer: {name}")

        elif cmd in ("3", "serve"):
            served = tq.dequeue()
            if served:
                print(f"Served: {served['name']} (joined: {served['time']})")
            else:
                print("No customers to serve.")

        elif cmd in ("4", "list"):
            tq.display()

        elif cmd in ("5", "size"):
            print("Total waiting:", tq.size())

        elif cmd in ("6", "estimate"):
            name = input("Customer name to estimate: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            est = tq.estimate_wait_time(name)
            if est is None:
                print("Customer not found in any queue.")
            else:
                print(f"Estimated wait time for {name}: {est} minutes")

        elif cmd in ("7", "save"):
            path = tq.save_to_file()
            print(f"Queues saved to {path}")

        elif cmd in ("8", "load"):
            ok = tq.load_from_file()
            if ok:
                print(f"Queues loaded from {DATA_FILE}")
            else:
                print("No saved file found.")

        elif cmd in ("9", "settime"):
            try:
                val = float(input("Avg service time (minutes): ").strip())
                if val <= 0:
                    raise ValueError
                tq.avg_service_time = val
                print(f"Average service time set to {val} minutes")
            except ValueError:
                print("Please enter a positive number.")

        elif cmd in ("0", "quit", "exit"):
            # ask to save before quitting
            ans = input("Save queues before exit? (y/n): ").strip().lower()
            if ans == "y":
                tq.save_to_file()
                print(f"Saved to {DATA_FILE}")
            print("Goodbye!")
            break

        elif cmd in ("help", "menu"):
            print_menu()

        else:
            print("Unknown command. Type 'menu' or 'help' to see commands.")

if __name__ == "__main__":
    main()
