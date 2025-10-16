# Amazon Product Availability Checker using Python
# ------------------------------------------------
# This script tracks the availability of an Amazon product (by ASIN)
# and sends an email alert when the product becomes available.

from lxml import html
import requests
from time import sleep
import time
import schedule
import smtplib

# Email ID of the user who wants to receive notifications
receiver_email_id = "EMAIL_ID_OF_USER"


def check(url):
    """Check product availability from the given Amazon URL"""
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/42.0.2311.90 Safari/537.36'
        )
    }

    page = requests.get(url, headers=headers)

    for i in range(20):
        # Avoid sending too many requests in a short time
        sleep(3)

        # Parse HTML content
        doc = html.fromstring(page.content)

        # Extract availability info
        XPATH_AVAILABILITY = '//div[@id ="availability"]//text()'
        raw_availability = doc.xpath(XPATH_AVAILABILITY)
        availability = ''.join(raw_availability).strip() if raw_availability else None
        return availability


def send_email(ans, product):
    """Send an email alert when product is available"""
    GMAIL_USERNAME = "YOUR_GMAIL_ID"
    GMAIL_PASSWORD = "YOUR_GMAIL_PASSWORD"

    recipient = receiver_email_id
    body_of_email = ans
    email_subject = f"{product} product availability"

    # Create SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()  # Secure connection

    # Login credentials
    s.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    # Prepare the message
    headers = "\r\n".join([
        "from: " + GMAIL_USERNAME,
        "subject: " + email_subject,
        "to: " + recipient,
        "mime-version: 1.0",
        "content-type: text/html"
    ])

    content = headers + "\r\n\r\n" + body_of_email

    # Send email
    s.sendmail(GMAIL_USERNAME, recipient, content)
    s.quit()


def read_asin():
    """Read ASIN and check product availability"""
    # ASIN ID (unique product ID on Amazon)
    asin = 'B077PWK5BT'
    url = "https://www.amazon.in/dp/" + asin
    print("Processing:", url)

    ans = check(url)
    print("Availability:", ans)

    availability_texts = [
        'Only 1 left in stock.',
        'Only 2 left in stock.',
        'In stock.'
    ]

    if ans in availability_texts:
        send_email(ans, asin)


# Schedule the script to run every 1 minute
def job():
    print("Tracking....")
    read_asin()


schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
