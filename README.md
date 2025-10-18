# 🎟️ Ticket Booking Queue System (Python)

A simple command-line based **Ticket Booking Queue Management System** implemented using the **Queue Data Structure** in Python.  
This project was developed as part of the **Programming Data Structures and Algorithms – I** module at NIBM.

---

## 🧠 Project Overview

The **Ticket Booking Queue System** is designed to simulate a real-world ticket counter or service queue.  
It uses the **FIFO (First In, First Out)** concept to ensure that customers are served in the same order they arrive.

This version also includes two enhanced features:
1. **Priority Queue for VIP customers** – VIP customers are served before regular ones.  
2. **Estimated Waiting Time Calculation** – Each customer can check their approximate waiting time.

---

## 🧩 Features

✅ Add new customers to the queue  
✅ Add VIP customers (served first)  
✅ Serve next customer (dequeue)  
✅ Display all waiting customers  
✅ Estimate waiting time for any customer  
✅ Save and load queues using JSON file  
✅ Change average service time dynamically  

---

## ⚙️ Technologies Used

| Component | Description |
|------------|-------------|
| **Language** | Python 3.x |
| **IDE / Editor** | Visual Studio Code |
| **Data Structure** | Queue (`collections.deque`) |
| **Storage** | JSON File |
| **Libraries** | `collections`, `json`, `datetime`, `os` |

---

## 🧮 Data Structure Concept

The system is built upon the **Queue** data structure — a linear structure following the **FIFO principle**.

| Operation | Description | Time Complexity |
|------------|--------------|-----------------|
| Enqueue | Add customer to queue | O(1) |
| Dequeue | Serve/remove customer | O(1) |
| Display | Show current queue | O(n) |
| Estimate Wait Time | Calculate time based on position | O(1) |

VIP customers are handled using a separate **priority queue**, which always gets served first.

---

## 🧰 How to Run the Project

### 🪟 Requirements
- Windows / macOS / Linux
- Python 3.8 or newer
- VS Code (recommended) with Python extension

---

### ▶️ Setup Steps

1. **Clone this repository**
   ```bash
   git clone https://github.com/Manindu01/ticket-booking-queue-system.git
   cd ticket-booking-queue-system

