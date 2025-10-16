# 🛒 Amazon Product Availability Checker (Python)

This Python script automatically checks the **availability of an Amazon product** (by ASIN) and **sends you an email** when it becomes available — perfect for grabbing limited-stock deals!

---

## 🚀 Features

- Tracks product availability on Amazon.
- Sends an instant email when the product is available.
- Runs continuously at a defined interval (every 1 minute by default).
- Fully automated using Python.

---

## 🧠 How It Works

1. You provide the **ASIN (Amazon Standard Identification Number)** of a product.  
2. The script uses `requests` and `lxml` to scrape product availability info.
3. If the product is in stock, it triggers an **email alert** using `smtplib`.

---

## 🛠️ Requirements

Install all required libraries before running the script:

```bash
pip install requests lxml schedule
