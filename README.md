# SMTP-TESTING-
Python-based manual SMTP client for testing and debugging mail servers
# Simple Manual SMTP Client (Python)

A lightweight and direct SMTP client written in Python for testing SMTP servers, analyzing responses, and sending raw emails.  
This tool allows you to interact with SMTP services manually without relying on external libraries.  
Supports both **plain text** and **HTML** email content.

---

## Features

- Connects directly to any SMTP server (default port: 25)
- Sends manual SMTP commands (`EHLO`, `MAIL FROM`, `RCPT TO`, `DATA`, etc.)
- Supports **HTML** and **plain text** emails
- Displays full client/server communication
- Useful for:
  - Security research  
  - SMTP debugging  
  - Email delivery testing  
  - Protocol analysis  

---

## Requirements

This project uses Python’s built-in libraries only:

- `socket`
- `sys`

No external dependencies are required.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/USERNAME/REPO.git
cd REPO
