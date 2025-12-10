# Automated-Bulk-WhatsApp-Message-Sender
Send personalized WhatsApp messages to hundreds of contacts directly from Excel. No coding required - just import, customize, and send!
Here’s a professional and well-structured `README.md` file tailored for your WhatsApp automation script using Selenium and Python:

# 📲 Automated WhatsApp Bulk Messenger using Selenium & Python

This project automates the process of sending personalized WhatsApp messages to multiple contacts using **Selenium WebDriver** and **WhatsApp Web**.

> ⚠️ **Note:** This script is for educational purposes only. Use it responsibly and respect WhatsApp's [terms of service](https://www.whatsapp.com/legal/terms-of-service).

---

## ✨ Features
# 🔧 Core Functionality
- 📊 Excel Integration - Import contacts directly from .xlsx or .xls files
- 💬 Smart Messaging - Send personalized messages with {Variable} replacement
- 🌍 Auto-Formatting - Automatically adds country codes (+92) to phone numbers
- 🔄 Retry Logic - Automatically retries failed messages (3 attempts)
- 📁 Error Logging - Detailed logs of failed messages for debugging

---

## 📦 Installation
1. **Clone the repository:**

```bash
git clone https://github.com/AliAsgherZoaib/Automated-Bulk-WhatsApp-Message-Sender.git
cd Automated-Bulk-WhatsApp-Message-Sender
````

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

# Prerequisites
- 🖥️ Windows 7/8/10/11 (64-bit recommended)
- 🌐 Google Chrome browser (latest version)
- 📧 WhatsApp account on your mobile device

---

## 🧪 Usage Guide

**Step 1:** Prepare Your Excel File
Create an Excel file with these columns:

| Name     | Contact    |
| -------- | ---------- |
| John Doe | 3001234567 |

or you can download sample.xlsx and run the test file.

**Step 2:** Configure the Application

1. 📁 Click "Choose Excel" and select your file
2. 📞 Select the phone number column
3. ✅ Check variables to include in messages
4. ✍️ Write your message template:

   Hello {Name},
   
   This is an automated test Message.
   
   Best regards,
   Thank You.

**Step 3:** Send Messages
1. 🚀 Click "Start Sending Messages"
2. 🔒 The GUI closes (prevents freezing)
3. 🌐 Chrome opens with WhatsApp Web
4. 📱 Scan QR code with your phone
5. ⏳ Messages send automatically
6. 📊 View results in the console window

---

## 🛑 Disclaimer

* This project is **not affiliated with WhatsApp**.
* Spamming users may result in your number being banned by WhatsApp.
* Use this script only with consent from message recipients.

**1. ✅ Appropriate Use Cases:**

- Customer notifications with prior consent
- Appointment reminders
- Educational announcements
- Internal team communications
- Event invitations

**2. ❌ Prohibited Use Cases:**

- Spamming or unsolicited messages
- Harassment or bullying
- Phishing attempts
- Automated marketing without consent
- Any illegal activities

**3. 🔒 User Responsibility:**

- Ensure compliance with WhatsApp's Terms of Service
- Respect recipients' privacy and consent
- Adhere to local laws and regulations
- Use appropriate message frequency

---

## 🧰 Common Solutions
| Issue                | Solution                                                 |
| -------------------- | -------------------------------------------------------- |
| ChromeDriver error   | Download matching version from chromedriver.chromium.org |
| -------------------- | -------------------------------------------------------- |
| QR code not scanning | Ensure WhatsApp is updated on your phone                 |
| -------------------- | -------------------------------------------------------- |
| Messages not sending | Check internet connection and Excel file format          |
| -------------------- | -------------------------------------------------------- |
| GUI not opening      | Run as Administrator, check antivirus exceptions         |

---

## 🙌 Acknowledgments
* Built with CustomTkinter for the modern GUI
* Uses Selenium for browser automation
* Powered by Pandas for Excel processing
* Inspired by community needs for ethical automation tools

---

## 🧠 Credits

Developed by [Ali Asghar Darwala](https://github.com/AliAsgherZoaib)

---
