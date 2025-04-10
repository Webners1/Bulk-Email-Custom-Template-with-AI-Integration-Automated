# IMPORTANT LEGAL DISCLAIMER
# ==========================
# This script is provided for educational purposes only. Before using this tool
# for sending emails, please ensure you comply with all applicable laws and regulations
# regarding electronic communications, including but not limited to:
#
# 1. CAN-SPAM Act (US): Requires commercial emails to include opt-out mechanisms,
#    valid physical address, and prohibits deceptive headers/subject lines.
#
# 2. GDPR (EU): Requires explicit consent before sending marketing emails to EU residents,
#    and includes rights to access, rectify, and erase personal data.
#
# 3. CASL (Canada): Requires express or implied consent, identification information,
#    and unsubscribe mechanisms.
#
# 4. Local anti-spam laws: Many countries have their own regulations governing
#    commercial electronic messages.
#
# By using this script, you acknowledge that:
# - You have obtained proper consent from recipients or have a lawful basis for contact
# - You will provide clear identification of yourself/organization in all messages
# - You will honor opt-out requests promptly
# - You will maintain proper records of consent as required by applicable laws
#
# The author of this script accepts no responsibility for misuse or any legal
# consequences resulting from the use of this tool. Always consult with a legal
# professional before implementing any email marketing campaign.



import smtplib, ssl
import time
import random
import csv
import requests
import json
import os
import platform
import sys
import argparse
from email.message import EmailMessage
from email.headerregistry import Address
from email.header import Header
import colorama
from colorama import Fore, Style
from datetime import datetime, date, timedelta
import schedule
import threading
import pytz
from colorama import Fore
import argparse
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import json

# Load the configuration from the JSON file
with open("config.json", "r") as config_file:
    CONFIG = json.load(config_file)

# uk_timezone = pytz.timezone("Asia/Karachi")
uk_timezone = pytz.timezone("Europe/London")

# Constants
SENT_RECORD_FILE = "sent_emails.json"
DAILY_EMAIL_LIMIT = 10  # Send 10 emails per day

# Config reference (assuming this comes from your main script)
CONFIG = {
    "csv_path": "./data.csv",
    "delay_between_emails": 5,  # seconds
}


# Initialize colorama
colorama.init(autoreset=True)

# Clear screen function based on OS
if platform.system() == "Linux":
    clear = lambda: os.system("clear")
else:
    clear = lambda: os.system("cls")

# Banner
today = date.today()
print(
    Fore.RED
    + """
        
                             SMTP Bulk Sender v 3.0.0        Coded By:  Muzammil Siddiqui     
                                                                                      
              Date: {today}
                                                               """
)

# Configuration variables


# Email template (used as fallback if AI generation fails)
# Switch to triple single quotes to avoid string escaping issues
# Using triple single quotes for the entire template
# Simplified template without problematic CSS

# AI prompt template for generating better emails
EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>StackUss - Your Tech Transformation Partner</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      line-height: 1.6;
      color: #333333;
      background-color: #ffffff;
      font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    .email-container {
      max-width: 650px;
      margin: 0 auto;
      padding: 0;
      background-color: #ffffff;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .banner-container {
      width: 100%;
      max-width: 650px;
      margin-bottom: 0;
      background-color: #0e1c36;
    }
    
    .banner-image {
      width: 100%;
      max-width: 650px;
      height: auto;
      display: block;
    }
    
    .header {
      text-align: center;
      padding: 24px;
      border-bottom: 1px solid #eeeeee;
      background-color: #ffffff;
    }
    
    .header img {
      max-width: 180px;
      height: auto;
    }
    
    .content {
      padding: 35px;
      background-color: #ffffff;
    }
    
    .tagline {
      font-size: 20px;
      font-weight: bold;
      color: #0e1c36;
      margin: 25px 0;
      text-align: center;
      border-left: 4px solid #ffcb05;
      padding-left: 15px;
      line-height: 1.4;
    }
    
    .footer {
      padding: 20px 35px;
      border-top: 1px solid #eeeeee;
      font-size: 14px;
      color: #777777;
      background-color: #f9f9f9;
    }
    
    .signature {
      margin-top: 35px;
      padding-top: 20px;
      border-top: 1px solid #f0f0f0;
    }
    
    .signature-name {
      font-weight: bold;
      color: #0e1c36;
    }
    
    .signature-title {
      color: #555;
      margin-bottom: 4px;
    }
    
    .cta-button {
      display: inline-block;
      background-color: #ffcb05;
      color: #0e1c36;
      text-decoration: none;
      padding: 14px 28px;
      border-radius: 4px;
      font-weight: bold;
      margin: 10px 0;
      text-align: center;
      font-size: 16px;
      transition: background-color 0.3s;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .highlight {
      color: #0e1c36;
      font-weight: bold;
    }
    
    .cta-section {
      background-color: #f9f9f9;
      padding: 28px;
      border-radius: 6px;
      margin: 30px 0;
      text-align: center;
      border: 1px solid #eeeeee;
    }
    
    .cta-heading {
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 15px;
      color: #0e1c36;
    }
    
    .services {
      background-color: #f9f9f9;
      padding: 20px 25px;
      border-radius: 6px;
      margin: 25px 0;
      border-left: 4px solid #ffcb05;
    }
    
    .services ul {
      margin: 15px 0;
      padding-left: 25px;
    }
    
    .services li {
      padding: 6px 0;
    }
    
    .intro-text {
      font-size: 16px;
      line-height: 1.7;
    }
    
    .trust-indicators {
      margin-top: 15px;
      padding: 15px;
      background-color: #f9f9f9;
      border-radius: 6px;
      font-size: 14px;
    }
    
    .contact-info {
      margin-top: 10px;
      font-size: 14px;
      color: #555;
    }
    
    .social-proof {
      font-style: italic;
      border-left: 3px solid #ddd;
      padding-left: 15px;
      margin: 20px 0;
      color: #555;
    }
  </style>
</head>
<body>
  <div class="email-container">
    <!-- Banner Image -->

    

    
    <div class="content">
      <p class="intro-text">Hey {first_name},</p>
      
      <p class="intro-text">{ai_content}</p>
      
      <div class="tagline">Innovate. Develop. Deliver.</div>
      
      <div class="services">
        <ul>
          <li><strong>Custom web & mobile application development</strong> - Tailored solutions that align with your business goals</li>
          <li><strong>Digital transformation strategy</strong> - Roadmaps that drive measurable business outcomes</li>
          <li><strong>UI/UX enhancement</strong> - Optimized designs that increase engagement and conversion</li>
          <li><strong>Technology stack modernization</strong> - Updates that improve performance and security</li>
        </ul>
      </div>
      
      <p class="social-proof">Many of our clients in the {industry} sector have seen a 30-40% increase in customer engagement and up to 25% improvement in operational efficiency within just 3 months of implementing our solutions.</p>
      
      <div class="cta-section">
        <div class="cta-heading">Ready to transform your digital presence?</div>
        <p>Let's discuss how StackUss can help {company} achieve its technology goals and enhance your competitive advantage.</p>
        <a href="" class="cta-button">Schedule Your Free Consultation →</a>
      </div>
      
      <p class="intro-text">Would you be open to a brief 15-minute call to explore how we might help {company} achieve similar results? I'd be happy to share some relevant case studies from our work with similar businesses.</p>
      
      <div class="signature">
        <p class="signature-name">Best regards,<br>
        {signature}</p>
        <p class="signature-title">CEO, StackUss</p>
        <p>StackUss - Your Trust Partner In High-Tech Transformation</p>
        
        <div class="contact-info">
          <p>Email: contact@stackuss.com </p>
          <p>Website: <a href="https://www.stackuss.com">www.stackuss.com</a></p>
        </div>
        
        <div class="trust-indicators">
          <p>Member of International Association of Web Professionals | ISO 27001 Certified</p>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <p>© 2025 StackUss. All rights reserved.</p>
      <p>If you'd prefer not to receive further communications, simply reply with "unsubscribe" in the subject line.</p>
    </div>
  </div>
</body>
</html>
"""


def format_with_template(ai_content, recipient_data):
    """Format the AI-generated content with the provided template"""
    print(ai_content, "datatat")
    try:
        # Get recipient info with fallbacks
        first_name = recipient_data.get("First Name", "")
        if not first_name:
            first_name = recipient_data.get("FirstName", "")

        company = recipient_data.get("Company", "")
        if not company:
            company = recipient_data.get("CompanyName", "your company")

        industry = recipient_data.get("Industry", "technology")
        signature = CONFIG.get("letter_signature", "Syed\nCEO, StackUss")

        # Use the template with placeholders
        email_html = EMAIL_TEMPLATE

        # Replace all placeholders
        email_html = email_html.replace("{first_name}", str(first_name))
        email_html = email_html.replace("{company}", str(company))
        email_html = email_html.replace("{industry}", str(industry))
        email_html = email_html.replace("{signature}", str(signature))
        email_html = email_html.replace("{ai_content}", str(ai_content))

        print(Fore.GREEN + f"[+] Successfully formatted email with AI content")
        return email_html

    except Exception as e:
        print(Fore.RED + f"[-] Error formatting email with template: {str(e)}")
        # In case of error, fall back to the original template
        return generate_email_content(recipient_data)


def setup_config():
    """Setup the configuration for SMTP and scheduling"""
    try:
        print(f"\n[+] SETUP SMTP SERVER FIRST:")
        CONFIG["smtp_server"] = input("Enter your SMTP server HOST: ")
        CONFIG["smtp_port"] = input("Enter your SMTP port: ")
        CONFIG["smtp_user"] = input("Please enter your SMTP USERNAME: ")
        CONFIG["smtp_pass"] = input("Enter your SMTP password: ")

        clear()
        print(
            Fore.RED
            + f"""
        
                             Bulk-Email-Custom-Template-with-AI-Integration-Automated v3.0.0        Coded By:       
              MuzammilSiddiqui_14 (Updated with Template and Cronjob)
              Date: {today}
              Contact: https://t.me/MuzammilSiddiqui_14                                               """
        )

        print(f"\n NOW THE EMAIL DETAILS:")
        CONFIG["letter_subject"] = input("Subject of email: ")
        CONFIG["letter_from"] = input("Enter From Name (Ex: Syed): ")
        custom_signature = input(
            'Custom signature (leave empty to use default "Syed\\nCEO, StackUss"): '
        )
        if custom_signature:
            CONFIG["letter_signature"] = custom_signature

        # AI email generation setup
        use_ai = input(
            "Use OpenAI to generate better personalized emails? (y/n): "
        ).lower()
        CONFIG["use_ai"] = use_ai == "y"

        if CONFIG["use_ai"]:
            CONFIG["openai_api_key"] = input("Enter your OpenAI API Key: ")

        delay = input("Delay between emails (default 5 seconds): ")
        if delay:
            CONFIG["delay_between_emails"] = int(delay)

        limit = input("Daily email sending limit (default 100): ")
        if limit:
            CONFIG["daily_limit"] = int(limit)

        # Get CSV file path
        CONFIG["csv_path"] = input("Enter path to your CSV file: ")

        # Scheduling options
        setup_schedule = input(
            "Do you want to set up a schedule for sending? (y/n): "
        ).lower()
        if setup_schedule == "y":
            CONFIG["schedule_time"] = input(
                "Enter time to send emails daily (HH:MM format, 24-hour): "
            )

            days_input = input(
                'Enter days to send (comma-separated, e.g. monday,wednesday,friday) or "daily": '
            ).lower()
            if days_input == "daily":
                CONFIG["schedule_days"] = [
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                    "sunday",
                ]
            else:
                CONFIG["schedule_days"] = [day.strip() for day in days_input.split(",")]

            print(
                Fore.GREEN
                + f"[+] Schedule set for {CONFIG['schedule_time']} on {', '.join(CONFIG['schedule_days'])}"
            )

    except KeyboardInterrupt:
        print("\nCTRL+C Detected, exiting...")
        exit()


def read_csv_data(filename):
    """Read recipient data from CSV file"""
    recipients = []
    try:
        with open(filename, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                recipients.append(row)
        print(f"[+] Successfully loaded {len(recipients)} recipients from CSV")
        return recipients
    except Exception as e:
        print(Fore.RED + f"[-] Error reading CSV file: {str(e)}")
        exit()


def format_ai_content_with_template(ai_content, recipient_data):
    """Format AI-generated content into our enhanced HTML template"""

    # Get recipient info with fallbacks
    first_name = recipient_data.get("First Name", "")
    if not first_name:
        first_name = recipient_data.get("FirstName", "")

    company = recipient_data.get("Company", "")
    if not company:
        company = recipient_data.get("CompanyName", "your company")

    industry = recipient_data.get("Industry", "technology")
    signature = CONFIG.get("letter_signature", "Syed\nCEO, StackUss")

    # Split AI content into paragraphs
    paragraphs = ai_content.split("\n\n")

    # Create HTML from paragraphs (only keeping paragraphs with content)
    html_content = ""
    for paragraph in paragraphs:
        if paragraph.strip():
            html_content += f'<p class="intro-text">{paragraph.strip()}</p>\n\n'

    # Create our enhanced HTML template
    email_html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <title>StackUss - Your Tech Transformation Partner</title>
  <style>
    /* Base styles */
    body {{
      margin: 0;
      padding: 0;
      line-height: 1.6;
      color: #333333;
      background-color: #ffffff;
      font-family: 'Segoe UI', Arial, sans-serif;
      -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
    }}
    
    /* Container styles */
    .email-container {{
      max-width: 650px;
      margin: 0 auto;
      padding: 0;
      background-color: #ffffff;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }}
    
    /* Banner styles with text fallback */
    .banner-container {{
      width: 100%;
      max-width: 650px;
      margin-bottom: 0;
      background-color: #0e1c36;
      text-align: center;
    }}
    
    .banner-image {{
      width: 100%;
      max-width: 650px;
      height: auto;
      display: block;
    }}
    
    .banner-fallback {{
      padding: 25px 15px;
      color: #ffffff;
      font-size: 22px;
      font-weight: bold;
      background-color: #0e1c36;
    }}
    
    /* Header styles with text fallback */
    .header {{
      text-align: center;
      padding: 24px;
      border-bottom: 1px solid #eeeeee;
      background-color: #ffffff;
    }}
    
    .header img {{
      max-width: 180px;
      height: auto;
    }}
    
    .logo-fallback {{
      font-size: 28px;
      font-weight: bold;
      color: #0e1c36;
    }}
    
    /* Content area */
    .content {{
      padding: 35px 20px;
      background-color: #ffffff;
    }}
    
    .tagline {{
      font-size: 20px;
      font-weight: bold;
      color: #0e1c36;
      margin: 25px 0;
      text-align: center;
      border-left: 4px solid #ffcb05;
      padding-left: 15px;
      line-height: 1.4;
    }}
    
    /* Footer */
    .footer {{
      padding: 20px;
      border-top: 1px solid #eeeeee;
      font-size: 14px;
      color: #777777;
      background-color: #f9f9f9;
      text-align: center;
    }}
    
    /* Signature area */
    .signature {{
      margin-top: 35px;
      padding-top: 20px;
      border-top: 1px solid #f0f0f0;
    }}
    
    .signature-name {{
      font-weight: bold;
      color: #0e1c36;
    }}
    
    .signature-title {{
      color: #555;
      margin-bottom: 4px;
    }}
    
    /* CTA button */
    .cta-button {{
      display: inline-block;
      background-color: #ffcb05;
      color: #0e1c36 !important;
      text-decoration: none;
      padding: 14px 28px;
      border-radius: 4px;
      font-weight: bold;
      margin: 10px 0;
      text-align: center;
      font-size: 16px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    
    /* Text highlights */
    .highlight {{
      color: #0e1c36;
      font-weight: bold;
    }}
    
    /* CTA section */
    .cta-section {{
      background-color: #f9f9f9;
      padding: 25px 20px;
      border-radius: 6px;
      margin: 30px 0;
      text-align: center;
      border: 1px solid #eeeeee;
    }}
    
    .cta-heading {{
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 15px;
      color: #0e1c36;
    }}
    
    /* Services section */
    .services {{
      background-color: #f9f9f9;
      padding: 20px 20px;
      border-radius: 6px;
      margin: 25px 0;
      border-left: 4px solid #ffcb05;
    }}
    
    .services ul {{
      margin: 15px 0;
      padding-left: 25px;
    }}
    
    .services li {{
      padding: 6px 0;
    }}
    
    /* Text styles */
    .intro-text {{
      font-size: 16px;
      line-height: 1.7;
    }}
    
    .trust-indicators {{
      margin-top: 15px;
      padding: 15px;
      background-color: #f9f9f9;
      border-radius: 6px;
      font-size: 14px;
    }}
    
    .contact-info {{
      margin-top: 10px;
      font-size: 14px;
      color: #555;
    }}
    
    .social-proof {{
      font-style: italic;
      border-left: 3px solid #ddd;
      padding-left: 15px;
      margin: 20px 0;
      color: #555;
    }}
    
    /* Mobile optimizations */
    @media screen and (max-width: 600px) {{
      .content {{
        padding: 25px 15px !important;
      }}
      
      .services, .cta-section {{
        padding: 15px !important;
      }}
      
      .cta-button {{
        display: block !important;
        padding: 16px 10px !important;
      }}
      
      .tagline {{
        text-align: left !important;
      }}
    }}
    
    /* Outlook-specific fixes */
    .ExternalClass {{
      width: 100%;
    }}
    
    .ExternalClass,
    .ExternalClass p,
    .ExternalClass span,
    .ExternalClass font,
    .ExternalClass td,
    .ExternalClass div {{
      line-height: 100%;
    }}
    
    /* Link styles */
    a {{
      color: #0e1c36;
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <center>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 650px;" class="email-container">
      <!-- Banner with text fallback -->
      <tr>
        <td class="banner-container">
          <!--[if mso]>
          <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr><td align="center" style="background-color: #0e1c36; padding: 25px 15px;">
          <div style="color: #ffffff; font-size: 22px; font-weight: bold;">StackUss - Technology Meets Transformation</div>
          </td></tr>
          </table>
          <![endif]-->
          <!--[if !mso]><!-->
          <img src="" alt="StackUss - Technology Meets Transformation" class="banner-image" style="display:block; width:100%;">
          <div class="banner-fallback" style="display:none;">StackUss - Technology Meets Transformation</div>
          <!--<![endif]-->
        </td>
      </tr>
      
      <!-- Logo/Header with text fallback -->
      <tr>
        <td class="header">
          <!--[if mso]>
          <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr><td align="center" style="background-color: #ffffff; padding: 24px;">
          <div style="color: #0e1c36; font-size: 28px; font-weight: bold;">StackUss</div>
          </td></tr>
          </table>
          <![endif]-->
          <!--[if !mso]><!-->
          <div class="logo-fallback" style="display:none;">StackUss</div>
          <!--<![endif]-->
        </td>
      </tr>
      
      <!-- Main Content -->
      <tr>
        <td class="content">
          {html_content}
          
          <div class="tagline">Innovate. Develop. Deliver.</div>
          
          <div class="services">
            <ul>
              <li><strong>Custom web & mobile application development</strong> - Tailored solutions that align with your business goals</li>
              <li><strong>Digital transformation strategy</strong> - Roadmaps that drive measurable business outcomes</li>
              <li><strong>UI/UX enhancement</strong> - Optimized designs that increase engagement and conversion</li>
              <li><strong>Technology stack modernization</strong> - Updates that improve performance and security</li>
            </ul>
          </div>
          
          <p class="social-proof">Many of our clients in the {industry} sector have seen a 30-40% increase in customer engagement and up to 25% improvement in operational efficiency within just 3 months of implementing our solutions.</p>
          
          <div class="cta-section">
            <div class="cta-heading">Ready to transform your digital presence?</div>
            <p>Let's discuss how StackUss can help {company} achieve its technology goals and enhance your competitive advantage.</p>
            <a href="" class="cta-button">Schedule Your Free Consultation →</a>
          </div>
          
          <div class="signature">
            <p class="signature-name">Best regards,<br>
            {signature}</p>
            <p class="signature-title">CEO, StackUss</p>
            <p>StackUss - Your Trust Partner In High-Tech Transformation</p>
            
            <div class="contact-info">
            </div>
            
            <div class="trust-indicators">
              <p>Member of International Association of Web Professionals | ISO 27001 Certified</p>
            </div>
          </div>
        </td>
      </tr>
      
      <!-- Footer -->
      <tr>
        <td class="footer">
          <p>© 2025 StackUss. All rights reserved.</p>
          <p>If you'd prefer not to receive further communications, simply reply with "unsubscribe" in the subject line.</p>
        </td>
      </tr>
    </table>
  </center>
</body>
</html>"""
    return email_html


# Updated main function to generate email content
def generate_email_content(recipient_data):
    """Generate personalized email content using template or AI"""
    if CONFIG["use_ai"]:
        try:
            # Use AI to generate personalized email
            print(Fore.CYAN + f"[*] Using AI to create personalized email...")
            return generate_ai_email_content(recipient_data)
        except Exception as e:
            print(Fore.RED + f"[-] Error with AI email generation: {str(e)}")
            print(Fore.YELLOW + "[!] Falling back to template email")
            # Fall back to template if AI fails

    # Use template for email generation if AI is not enabled or fails
    try:
        print(Fore.CYAN + f"[*] Using template for email...")

        # Format the template with recipient data
        # Default to 'technology' if industry not available
        industry = recipient_data.get("Industry", "")
        if not industry:
            industry = recipient_data.get("Industry", "technology")

        # Debug: Print recipient data
        print(Fore.CYAN + f"[DEBUG] Recipient data: {recipient_data}")

        # Get the values with defaults to prevent None errors
        first_name = recipient_data.get("First Name", "")
        if not first_name:
            first_name = recipient_data.get("FirstName", "")

        company = recipient_data.get("Company", "")
        if not company:
            company = recipient_data.get("CompanyName", "your company")

        signature = CONFIG.get("letter_signature", "Syed\nCEO, StackUss")

        # Create our enhanced HTML template (same as in the format_ai_content_with_template function)
        email_html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>StackUss - Your Tech Transformation Partner</title>
  <style>
    body {{
      margin: 0;
      padding: 0;
      line-height: 1.6;
      color: #333333;
      background-color: #ffffff;
      font-family: 'Segoe UI', Arial, sans-serif;
    }}
    
    .email-container {{
      max-width: 650px;
      margin: 0 auto;
      padding: 0;
      background-color: #ffffff;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }}
    
    .banner-container {{
      width: 100%;
      max-width: 650px;
      margin-bottom: 0;
      background-color: #0e1c36;
    }}
    
    .banner-image {{
      width: 100%;
      max-width: 650px;
      height: auto;
      display: block;
    }}
    
    .header {{
      text-align: center;
      padding: 24px;
      border-bottom: 1px solid #eeeeee;
      background-color: #ffffff;
    }}
    
    .header img {{
      max-width: 180px;
      height: auto;
    }}
    
    .content {{
      padding: 35px;
      background-color: #ffffff;
    }}
    
    .tagline {{
      font-size: 20px;
      font-weight: bold;
      color: #0e1c36;
      margin: 25px 0;
      text-align: center;
      border-left: 4px solid #ffcb05;
      padding-left: 15px;
      line-height: 1.4;
    }}
    
    .footer {{
      padding: 20px 35px;
      border-top: 1px solid #eeeeee;
      font-size: 14px;
      color: #777777;
      background-color: #f9f9f9;
    }}
    
    .signature {{
      margin-top: 35px;
      padding-top: 20px;
      border-top: 1px solid #f0f0f0;
    }}
    
    .signature-name {{
      font-weight: bold;
      color: #0e1c36;
    }}
    
    .signature-title {{
      color: #555;
      margin-bottom: 4px;
    }}
    
    .cta-button {{
      display: inline-block;
      background-color: #ffcb05;
      color: #0e1c36;
      text-decoration: none;
      padding: 14px 28px;
      border-radius: 4px;
      font-weight: bold;
      margin: 10px 0;
      text-align: center;
      font-size: 16px;
      transition: background-color 0.3s;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    
    .highlight {{
      color: #0e1c36;
      font-weight: bold;
    }}
    
    .cta-section {{
      background-color: #f9f9f9;
      padding: 28px;
      border-radius: 6px;
      margin: 30px 0;
      text-align: center;
      border: 1px solid #eeeeee;
    }}
    
    .cta-heading {{
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 15px;
      color: #0e1c36;
    }}
    
    .services {{
      background-color: #f9f9f9;
      padding: 20px 25px;
      border-radius: 6px;
      margin: 25px 0;
      border-left: 4px solid #ffcb05;
    }}
    
    .services ul {{
      margin: 15px 0;
      padding-left: 25px;
    }}
    
    .services li {{
      padding: 6px 0;
    }}
    
    .intro-text {{
      font-size: 16px;
      line-height: 1.7;
    }}
    
    .trust-indicators {{
      margin-top: 15px;
      padding: 15px;
      background-color: #f9f9f9;
      border-radius: 6px;
      font-size: 14px;
    }}
    
    .contact-info {{
      margin-top: 10px;
      font-size: 14px;
      color: #555;
    }}
    
    .social-proof {{
      font-style: italic;
      border-left: 3px solid #ddd;
      padding-left: 15px;
      margin: 20px 0;
      color: #555;
    }}
  </style>
</head>
<body>
  <div class="email-container">
    <!-- Banner Image -->
    <div class="banner-container">
      <img src="" alt="StackUss - Technology Meets Transformation" class="banner-image">
    </div>
    
    <div class="header">
      <!-- Logo image -->
      <img src="" alt="StackUss Logo">
    </div>
    
    <div class="content">
      <p class="intro-text">Hey {first_name},</p>
      
      <p class="intro-text">I came across <span class="highlight">{company}</span> and was genuinely impressed by your work in the {industry} space. Following a review of your current digital presence, I believe we could help enhance your user experience and operational efficiency.</p>
      
      <div class="tagline">Innovate. Develop. Deliver.</div>
      
      <div class="services">
        <ul>
          <li><strong>Custom web & mobile application development</strong> - Tailored solutions that align with your business goals</li>
          <li><strong>Digital transformation strategy</strong> - Roadmaps that drive measurable business outcomes</li>
          <li><strong>UI/UX enhancement</strong> - Optimized designs that increase engagement and conversion</li>
          <li><strong>Technology stack modernization</strong> - Updates that improve performance and security</li>
        </ul>
      </div>
      
      <p class="social-proof">Many of our clients in the {industry} sector have seen a 30-40% increase in customer engagement and up to 25% improvement in operational efficiency within just 3 months of implementing our solutions.</p>
      
      <div class="cta-section">
        <div class="cta-heading">Ready to transform your digital presence?</div>
        <p>Let's discuss how StackUss can help {company} achieve its technology goals and enhance your competitive advantage.</p>
        <a href="" class="cta-button">Schedule Your Free Consultation →</a>
      </div>
      
      <p class="intro-text">Would you be open to a brief 15-minute call to explore how we might help {company} achieve similar results? I'd be happy to share some relevant case studies from our work with similar businesses.</p>
      
      <div class="signature">
        <p class="signature-name">Best regards,<br>
        {signature}</p>
        <p class="signature-title">CEO, StackUss</p>
        <p>StackUss - Your Trust Partner In High-Tech Transformation</p>
        
        <div class="contact-info">
        </div>
        
        <div class="trust-indicators">
          <p>Member of International Association of Web Professionals | ISO 27001 Certified</p>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <p>© 2025 StackUss. All rights reserved.</p>
      <p>If you'd prefer not to receive further communications, simply reply with "unsubscribe" in the subject line.</p>
    </div>
  </div>
</body>
</html>"""

        print(Fore.GREEN + f"[+] Email content generation successful")
        return email_html

    except Exception as e:
        print(Fore.RED + f"[-] Error generating email content: {str(e)}")
        traceback_info = (
            str(e.__traceback__.tb_frame.f_code.co_filename)
            + ":"
            + str(e.__traceback__.tb_lineno)
        )
        print(Fore.RED + f"[-] Error occurred at: {traceback_info}")

        # Fallback template with basic styling for emergencies
        return """<!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .signature {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <p>Hey {recipient_data.get('First Name', '')},</p>
                <p>I came across {recipient_data.get('Company', '')} and was impressed by what you're doing. I specialize in web and app development at StackUss and noticed an opportunity to enhance your online presence.</p>
                <p>Would you be open to a quick chat to explore how we can help?</p>
                <div class="signature">
                    <p>Best,<br>{CONFIG.get("letter_signature", "Syed\nCEO, StackUss")}</p>
                </div>
            </div>
        </body>
        </html>"""


def extract_main_content(api_response):
    """Extract only the main body content from the API response, removing subject, greeting, and signature."""
    try:
        # Split the content by lines
        lines = api_response.strip().split("\n")

        # Filter out empty lines
        lines = [line.strip() for line in lines if line.strip()]

        if len(lines) <= 2:  # If there are only 1-2 lines, just return everything
            return api_response.strip()

        # Remove the subject line (if it starts with "Subject:" or similar)
        if any(
            lines[0].lower().startswith(prefix)
            for prefix in ["subject:", "re:", "fwd:"]
        ):
            lines = lines[1:]

        # Remove greeting line (if it starts with "Hi", "Hello", "Dear", etc.)
        greeting_prefixes = ["hi", "hello", "dear", "hey", "greetings"]
        if any(lines[0].lower().startswith(prefix) for prefix in greeting_prefixes):
            lines = lines[1:]

        # Remove signature (typically the last 1-3 lines, if they start with "best", "regards", "sincerely", etc.)
        signature_prefixes = [
            "best",
            "regards",
            "sincerely",
            "thank",
            "cheers",
            "yours",
        ]

        # Find where the signature starts (if it exists)
        signature_start_index = None
        for i in range(len(lines) - 1, max(0, len(lines) - 4), -1):
            if any(
                lines[i].lower().startswith(prefix) for prefix in signature_prefixes
            ):
                signature_start_index = i
                break

        # If signature was found, remove it
        if signature_start_index is not None:
            lines = lines[:signature_start_index]

        # Combine the remaining lines into the main content
        main_content = " ".join(lines).strip()

        # Special case handling: look for patterns like a main body enclosed in quotes
        if '"""' in api_response:
            import re

            pattern = r'"""(.*?)"""'
            matches = re.findall(pattern, api_response, re.DOTALL)
            if matches:
                return matches[0].strip()

        return main_content

    except Exception as e:
        print(Fore.RED + f"[-] Error extracting main content: {str(e)}")
        # If extraction fails, return the original API response
        return api_response.strip()


def generate_ai_email_content(recipient_data):
    """Generate personalized email content using custom API"""
    try:
        # Get recipient information with fallbacks
        first_name = recipient_data.get("First Name", "")
        if not first_name:
            first_name = recipient_data.get("FirstName", "")

        last_name = recipient_data.get("Last Name", "")
        if not last_name:
            last_name = recipient_data.get("LastName", "")

        # Generate a user ID based on last name
        if last_name:
            # Create a hash from the last name to generate a consistent ID
            import hashlib

            hash_object = hashlib.md5(last_name.encode())
            user_id = str(int(hash_object.hexdigest(), 16) % 10000)  # Limit to 4 digits
        else:
            # Fallback to random number if no last name
            import random

            user_id = str(random.randint(1000, 9999))

        # Prepare the payload for your custom API
        payload = {
            "company": "StackUss",
            "action": "your existing website is good but there is room for improvement we Identified issues in their existing website and potential improvements and make the email under 100 words max and also dont mention I’m [Your Name] remember",
            "tone": "Exciting, Confident and Persuasive under 100 words, be extra specific for what stackuss offering, make an offer which sound irresistible and make it impossible to compare with any other brand",
            "recepient": (
                f"Mr. {last_name}" if last_name else "Sir/Madam of the Company"
            ),
            "product": "Custom-coded Website Optimization and Redesign with performance-first approach — no templates 1-week MVP delivery, unlimited design revisions, and 24/7 real-time development updates",
            "proposition": "Get 20% off for the next 3 months plus a FREE UX audit (worth $300) and a 30-day full refund guarantee.let's schedule a complimentary strategy call where I can provide personalized suggestions.",
            "sender": CONFIG["letter_from"],
            "user_id": user_id,  # Using the hash of last name
        }

        headers = {"Content-Type": "application/json"}

        print(
            Fore.CYAN
            + f"[*] Generating email with user_id: {user_id} for {first_name} {last_name}"
        )

        try:
            # Make the request to your custom API
            response = requests.post(
                "api_for_ai_email_generation",
                headers=headers,
                json=payload,
                timeout=30,
            )

            if response.status_code == 200:
                # Extract the email content from the response
                full_response = response.text

                # Extract just the main body content
                ai_content = extract_main_content(full_response)
                print(
                    Fore.GREEN
                    + f"[+] Successfully extracted main content from API response"
                )
                print(Fore.GREEN + f"[+] {ai_content}")

                # Format the AI-generated content into the provided template
                return format_with_template(ai_content, recipient_data)
            else:
                print(
                    Fore.RED
                    + f"[-] API Error: {response.status_code} - {response.text}"
                )
                raise Exception(f"API error: {response.status_code}")
        except Exception as e:
            print(Fore.RED + f"[-] Failed to get response from API: {str(e)}")
            raise Exception(f"Failed to get response from API: {str(e)}")

    except Exception as e:
        print(Fore.RED + f"[-] Failed to generate email content: {str(e)}")
        raise Exception(f"Failed to generate AI content: {str(e)}")


def generate_email_content(recipient_data):
    """Generate personalized email content using template or AI"""
    if CONFIG["use_ai"]:
        try:
            # Use AI to generate personalized email
            print(Fore.CYAN + f"[*] Using AI to create personalized email...")
            return generate_ai_email_content(recipient_data)
        except Exception as e:
            print(Fore.RED + f"[-] Error with AI email generation: {str(e)}")
            print(Fore.YELLOW + "[!] Falling back to template email")
            # Fall back to template if AI fails

    # Use template for email generation if AI is not enabled or fails
    try:
        print(Fore.CYAN + f"[*] Using template for email...")

        # Get the values with defaults to prevent None errors
        first_name = recipient_data.get("First Name", "")
        if not first_name:
            first_name = recipient_data.get("FirstName", "")

        company = recipient_data.get("Company", "")
        if not company:
            company = recipient_data.get("CompanyName", "your company")

        industry = recipient_data.get("Industry", "technology")
        signature = CONFIG.get("letter_signature", "Syed\nCEO, StackUss")

        # Use the template provided directly
        email_html = EMAIL_TEMPLATE

        # Replace placeholders one at a time with explicit error handling
        try:
            email_html = email_html.replace("{first_name}", str(first_name))
            print(Fore.CYAN + f"[DEBUG] Replaced first_name: {first_name}")
        except Exception as e:
            print(Fore.RED + f"[-] Error replacing first_name: {str(e)}")
            email_html = email_html.replace("{first_name}", "")

        try:
            email_html = email_html.replace("{company}", str(company))
            print(Fore.CYAN + f"[DEBUG] Replaced company: {company}")
        except Exception as e:
            print(Fore.RED + f"[-] Error replacing company: {str(e)}")
            email_html = email_html.replace("{company}", "")

        try:
            email_html = email_html.replace("{industry}", str(industry))
            print(Fore.CYAN + f"[DEBUG] Replaced industry: {industry}")
        except Exception as e:
            print(Fore.RED + f"[-] Error replacing industry: {str(e)}")
            email_html = email_html.replace("{industry}", "technology")

        try:
            email_html = email_html.replace("{signature}", str(signature))
            print(Fore.CYAN + f"[DEBUG] Replaced signature")
        except Exception as e:
            print(Fore.RED + f"[-] Error replacing signature: {str(e)}")
            email_html = email_html.replace("{signature}", "Syed\nCEO, StackUss")

        print(Fore.GREEN + f"[+] Email content generation successful")
        return email_html

    except Exception as e:
        print(Fore.RED + f"[-] Error generating email content: {str(e)}")

        # Fallback template with basic styling for emergencies
        return """<!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .signature {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <p>Hey {recipient_data.get('First Name', '')},</p>
                <p>I came across {recipient_data.get('Company', '')} and was impressed by what you're doing. I specialize in web and app development at StackUss and noticed an opportunity to enhance your online presence.</p>
                <p>Would you be open to a quick chat to explore how we can help?</p>
                <div class="signature">
                    <p>Best,<br>{CONFIG.get("letter_signature", "Syed\nCEO, StackUss")}</p>
                </div>
            </div>
        </body>
        </html>"""


def extract_main_content(api_response):
    """Extract only the main body content from the API response, removing subject, greeting, and signature."""
    try:
        # Split the content by lines
        lines = api_response.strip().split("\n")

        # Filter out empty lines
        lines = [line.strip() for line in lines if line.strip()]

        if len(lines) <= 2:  # If there are only 1-2 lines, just return everything
            return api_response.strip()

        # Remove the subject line (if it starts with "Subject:" or similar)
        if any(
            lines[0].lower().startswith(prefix)
            for prefix in ["subject:", "re:", "fwd:"]
        ):
            lines = lines[1:]

        # Remove greeting line (if it starts with "Hi", "Hello", "Dear", etc.)
        greeting_prefixes = ["hi", "hello", "dear", "hey", "greetings"]
        if any(lines[0].lower().startswith(prefix) for prefix in greeting_prefixes):
            lines = lines[1:]

        # Remove signature (typically the last 1-3 lines, if they start with "best", "regards", "sincerely", etc.)
        signature_prefixes = [
            "best",
            "regards",
            "sincerely",
            "thank",
            "cheers",
            "yours",
        ]

        # Find where the signature starts (if it exists)
        signature_start_index = None
        for i in range(len(lines) - 1, max(0, len(lines) - 4), -1):
            if any(
                lines[i].lower().startswith(prefix) for prefix in signature_prefixes
            ):
                signature_start_index = i
                break

        # If signature was found, remove it
        if signature_start_index is not None:
            lines = lines[:signature_start_index]

        # Combine the remaining lines into the main content
        main_content = " ".join(lines).strip()

        # Special case handling: look for patterns like a main body enclosed in quotes
        if '"""' in api_response:
            import re

            pattern = r'"""(.*?)"""'
            matches = re.findall(pattern, api_response, re.DOTALL)
            if matches:
                return matches[0].strip()

        return main_content

    except Exception as e:
        print(Fore.RED + f"[-] Error extracting main content: {str(e)}")
        # If extraction fails, return the original API response
        return api_response.strip()


def generate_messages(recipients, limit=None):
    """Generate email messages for each recipient"""
    count = 0
    for recipient in recipients:
        # If limit is set and we've reached it, stop generating
        if limit and count >= limit:
            break

        print(
            Fore.YELLOW
            + f"[*] Generating email for {recipient.get('First Name', '')} {recipient.get('Last Name', '')} at {recipient.get('Company', '')}..."
        )

        # Get personalized content
        if CONFIG["use_ai"] and CONFIG["openai_api_key"]:
            print(Fore.CYAN + f"[*] Using AI to create personalized email...")
        else:
            print(Fore.CYAN + f"[*] Using template for email...")

        email_html = generate_email_content(recipient)

        # Create email message
        message = EmailMessage()
        CONFIG["letter_subject"] = (
            "We Found Something You Should Fix on Your {company} Website"
        )
        message["Subject"] = CONFIG["letter_subject"].format(
            company=recipient.get("Company", "")
        )
        message["From"] = Address(
            CONFIG["letter_from"], *CONFIG["smtp_user"].split("@")
        )
        message["To"] = recipient.get("Email", "")
        message.set_content(email_html, "html")

        yield message, recipient
        count += 1


def send_emails(messages):
    """Send emails via SMTP without saving logs to text file"""
    try:
        port = CONFIG["smtp_port"]
        emails_sent = 0

        if port == "587":
            with smtplib.SMTP(CONFIG["smtp_server"], port) as server:
                try:
                    server.starttls(context=ssl.create_default_context())
                    server.login(CONFIG["smtp_user"], CONFIG["smtp_pass"])
                    print(
                        Fore.GREEN
                        + f"""
                    \n\n\nSMTP CONNECTION ESTABLISHED:
                    SERVER: {CONFIG["smtp_server"]}
                    USER: {CONFIG["smtp_user"]}
                    PORT: {port}
                    NO CONNECTION ERRORS!
                    """
                    )

                    for message, recipient in messages:
                        try:
                            time.sleep(CONFIG["delay_between_emails"])
                            server.send_message(message)
                            emails_sent += 1
                            status = f"SUCCESS: Email sent to {recipient.get('First Name', '')} {recipient.get('Last Name', '')} ({message['To']}) at {time.strftime('%X')}"
                            print(Fore.GREEN + f"[+] {status}")
                        except Exception as e:
                            status = (
                                f"ERROR: Failed to send to {message['To']}: {str(e)}"
                            )
                            print(Fore.RED + f"[-] {status}")

                    print(
                        Fore.GREEN
                        + f"\n###################################################################### {emails_sent} EMAILS SENT"
                    )

                except smtplib.SMTPException as e:
                    print(Fore.RED + f"[-] SMTP ERROR: {str(e)}")

        elif port == "465":
            with smtplib.SMTP_SSL(
                CONFIG["smtp_server"], port, context=ssl.create_default_context()
            ) as server:
                try:
                    server.login(CONFIG["smtp_user"], CONFIG["smtp_pass"])
                    print(
                        Fore.GREEN
                        + f"""
                    \n\n\nSMTP CONNECTION ESTABLISHED:
                    SERVER: {CONFIG["smtp_server"]}
                    USER: {CONFIG["smtp_user"]}
                    PORT: {port}
                    NO CONNECTION ERRORS!
                    """
                    )

                    for message, recipient in messages:
                        try:
                            time.sleep(CONFIG["delay_between_emails"])
                            server.send_message(message)
                            emails_sent += 1
                            status = f"SUCCESS: Email sent to {recipient.get('First Name', '')} {recipient.get('Last Name', '')} ({message['To']}) at {time.strftime('%X')}"
                            print(Fore.GREEN + f"[+] {status}")
                        except Exception as e:
                            status = (
                                f"ERROR: Failed to send to {message['To']}: {str(e)}"
                            )
                            print(Fore.RED + f"[-] {status}")

                    print(
                        Fore.GREEN
                        + f"\n###################################################################### {emails_sent} EMAILS SENT"
                    )

                except smtplib.SMTPException as e:
                    print(Fore.RED + f"[-] SMTP ERROR: {str(e)}")
        else:
            print(Fore.RED + "Wrong PORT. Only 587 (TLS) or 465 (SSL) are supported.")

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] CTRL+C Detected, exiting...")
        exit()


def run_scheduled_task():
    """Function to run when scheduled"""
    try:
        print(
            Fore.GREEN
            + f"[+] Running scheduled email sending at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # Read recipients from CSV
        recipients = read_csv_data(CONFIG["csv_path"])

        # Generate and send messages with daily limit
        messages = generate_messages(recipients, CONFIG["daily_limit"])
        send_emails(messages)

        print(
            Fore.GREEN
            + f"[+] Scheduled task completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    except Exception as e:
        print(Fore.RED + f"[-] Error in scheduled task: {str(e)}")


def start_scheduler():
    """Start the scheduler based on configuration"""
    if not CONFIG["schedule_time"] or not CONFIG["schedule_days"]:
        print(Fore.YELLOW + "[!] No schedule configured. Exiting scheduler.")
        return

    print(
        Fore.GREEN
        + f"[+] Starting scheduler for {CONFIG['schedule_time']} on {', '.join(CONFIG['schedule_days'])}"
    )

    # Schedule for specific days
    for day in CONFIG["schedule_days"]:
        # Convert day string to schedule method
        if hasattr(schedule.every(), day):
            getattr(schedule.every(), day).at(CONFIG["schedule_time"]).do(
                run_scheduled_task
            )

    # Run the scheduler in a loop
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


def test_ai_email_generation():
    """Test AI email generation with sample data"""
    print(Fore.CYAN + "\n[*] Testing AI email generation...")

    # Sample recipient data
    sample_recipient = {
        "First Name": "John",
        "Last Name": "Doe",
        "Title": "Owner",
        "Company": "Amazing Restaurant",
        "Company City": "New York",
        "Company State": "NY",
        "Company Country": "USA",
    }

    try:
        # Generate email content
        print(Fore.YELLOW + "[*] Generating sample email...")
        email_content = generate_ai_email_content(sample_recipient)

        # Output the generated email
        print(Fore.GREEN + "\n[+] Sample AI-generated email:")
        print("=" * 80)
        print(email_content)
        print("=" * 80)

        # Save to file
        test_file = f"sample_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(test_file, "w") as f:
            f.write(email_content)
        print(Fore.GREEN + f"[+] Sample email saved to {test_file}")

    except Exception as e:
        print(Fore.RED + f"[-] AI Email generation test failed: {str(e)}")


def get_uk_time():
    """Get current time in UK timezone"""
    return datetime.now(uk_timezone)


def is_weekday():
    """Check if today is a weekday (Monday to Friday)"""
    uk_time = get_uk_time()
    return uk_time.weekday() < 5  # 0-4 are Monday to Friday


def is_optimal_day():
    """Check if today is an optimal day (Tuesday, Wednesday, Thursday)"""
    uk_time = get_uk_time()
    return uk_time.weekday() in [1, 2, 3]  # Tuesday, Wednesday, Thursday


def read_csv_data(filename):
    """Read recipient data from CSV file and filter out invalid entries"""
    recipients = []
    try:
        with open(filename, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                # Skip rows without an email address
                if not row.get("Email", "").strip():
                    continue

                # Basic validation of email format
                email = row.get("Email", "").strip().lower()
                if "@" not in email or "." not in email:
                    print(Fore.YELLOW + f"[!] Skipping invalid email: {email}")
                    continue

                # Add valid recipient
                recipients.append(row)

        print(
            Fore.GREEN
            + f"[+] Successfully loaded {len(recipients)} valid recipients from CSV"
        )
        return recipients
    except Exception as e:
        print(Fore.RED + f"[-] Error reading CSV file: {str(e)}")
        sys.exit(1)


def load_sent_records():
    """Load the record of sent emails"""
    if os.path.exists(SENT_RECORD_FILE):
        try:
            with open(SENT_RECORD_FILE, "r") as f:
                data = json.load(f)
                # Ensure the structure is correct
                if "sent_emails" not in data:
                    data["sent_emails"] = []
                if "last_run_date" not in data:
                    data["last_run_date"] = None
                return data
        except Exception as e:
            print(Fore.RED + f"[-] Error loading sent records: {str(e)}")
            return {"sent_emails": [], "last_run_date": None}
    else:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(SENT_RECORD_FILE), exist_ok=True)
        return {"sent_emails": [], "last_run_date": None}


def get_next_batch(all_recipients, sent_records, batch_size):
    """Get the next batch of recipients who haven't been emailed yet"""
    # Extract just the email addresses from the sent records
    sent_email_addresses = set()

    for record in sent_records.get("sent_emails", []):
        if isinstance(record, dict) and "email" in record:
            # If it's stored as a dict with an email field
            sent_email_addresses.add(record["email"].lower())
        elif isinstance(record, str):
            # If it's stored as a string directly
            sent_email_addresses.add(record.lower())

    # Filter out recipients that have already been emailed
    unsent_recipients = [
        r
        for r in all_recipients
        if r.get("Email", "").strip().lower() not in sent_email_addresses
    ]

    if not unsent_recipients:
        print(Fore.YELLOW + "[!] All recipients have been emailed. Starting over.")
        # Clear sent records and start over
        sent_records["sent_emails"] = []
        save_sent_records(sent_records)
        unsent_recipients = all_recipients

    # Return the next batch (up to batch_size)
    return unsent_recipients[:batch_size]


def update_sent_records(sent_records, batch):
    """Update the sent records with newly sent emails"""
    today = datetime.now().strftime("%Y-%m-%d")

    # Add newly sent emails to the record
    for recipient in batch:
        email = recipient.get("Email", "").strip().lower()
        if email:
            # Store each email as a dictionary with email and send_date
            record = {"email": email, "send_date": today}
            # Make sure we're not adding duplicates
            if record not in sent_records["sent_emails"]:
                sent_records["sent_emails"].append(record)

    # Update the last run date
    sent_records["last_run_date"] = today

    # Save the updated records
    save_sent_records(sent_records)


def save_sent_records(records):
    """Save the record of sent emails and remove entries older than 2 days"""
    try:
        # Calculate the date 2 days ago
        two_days_ago = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

        # Filter out records older than 2 days
        filtered_emails = []
        for record in records.get("sent_emails", []):
            # Handle both dict and string records
            if isinstance(record, dict) and "send_date" in record:
                if record["send_date"] >= two_days_ago:
                    filtered_emails.append(record)
            else:
                # If it doesn't have a date, keep it to be safe
                filtered_emails.append(record)

        # Update the records with filtered emails
        old_count = len(records.get("sent_emails", []))
        records["sent_emails"] = filtered_emails
        new_count = len(records["sent_emails"])

        if old_count > new_count:
            print(
                Fore.YELLOW
                + f"[!] Removed {old_count - new_count} email records older than 2 days"
            )

        # Make sure the directory exists
        os.makedirs(os.path.dirname(SENT_RECORD_FILE), exist_ok=True)

        # Save to file
        with open(SENT_RECORD_FILE, "w") as f:
            json.dump(records, f, indent=4)

    except Exception as e:
        print(Fore.RED + f"[-] Error saving sent records: {str(e)}")
        print(Fore.RED + f"[-] Records data: {records}")


def run_daily_email_campaign():
    """Run a daily email campaign based on Pakistan optimal times"""
    try:
        print(
            Fore.GREEN
            + f"[+] Starting daily email campaign at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print(
            Fore.YELLOW
            + f"[!] Current Pakistan time: {get_uk_time().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # Load sent records
        sent_records = load_sent_records()

        # Make sure the structure is correct
        if not isinstance(sent_records, dict):
            print(
                Fore.RED
                + f"[-] Error: sent_records is not a dictionary: {type(sent_records)}"
            )
            sent_records = {"sent_emails": [], "last_run_date": None}

        if "sent_emails" not in sent_records:
            sent_records["sent_emails"] = []

        if "last_run_date" not in sent_records:
            sent_records["last_run_date"] = None

        # Read all recipients
        all_recipients = read_csv_data(CONFIG["csv_path"])

        # Get the next batch to send
        batch = get_next_batch(all_recipients, sent_records, DAILY_EMAIL_LIMIT)

        if not batch:
            print(Fore.YELLOW + "[!] No recipients to email today.")
            return

        print(Fore.GREEN + f"[+] Sending emails to {len(batch)} recipients")

        # Generate and send messages
        messages = generate_messages(batch)
        send_emails(messages)

        # Update sent records
        update_sent_records(sent_records, batch)

        print(
            Fore.GREEN
            + f"[+] Daily email campaign completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print(
            Fore.GREEN
            + f"[+] Sent {len(batch)} emails. Total sent so far: {len(sent_records['sent_emails'])}"
        )

    except Exception as e:
        print(Fore.RED + f"[-] Error in email campaign: {str(e)}")
        import traceback

        traceback.print_exc()


def setup_uk_optimized_cronjob():
    """Set up an optimized cron-like schedule for UK recipients"""
    print(Fore.CYAN + "[*] Setting up UK-optimized email cronjob...")

    # Get the current UK day of week (0=Monday, 6=Sunday)
    uk_day = get_uk_time().weekday()

    # Determine times based on day of the week
    if uk_day == 0:  # Monday
        # Monday afternoon only (avoid morning)
        send_time = random_time_string(15, 17)  # 3 PM - 5 PM
    elif uk_day == 4:  # Friday
        # Friday morning only (avoid afternoon)
        send_time = random_time_string(8, 11)  # 8 AM - 11 AM
    # elif uk_day in [1, 2, 3]:  # Tuesday, Wednesday, Thursday (optimal days)
    elif uk_day in [1, 5, 6]:  # Tuesday, Wednesday, Thursday (optimal days)
        # Choose randomly between morning, lunch and afternoon

        time_slots = [
            (8, 10),  # Morning: 8 AM - 10 AM
            (12, 13),  # Lunch: 12 PM - 1 PM
            (16, 17),  # Afternoon: 4 PM - 5 PM
        ]
        start_hour, end_hour = random.choice(time_slots)
        send_time = random_time_string(start_hour, end_hour)

    else:  # Weekend
        # No emails on weekends
        print(Fore.YELLOW + "[!] Today is a weekend. No emails will be sent.")
        return

    # Schedule single run at the selected time
    print(Fore.GREEN + f"[+] Emails will be sent today at {send_time} UK time")
    schedule.every().day.at(send_time).do(run_daily_email_campaign)


def random_time_string(start_hour, end_hour):
    """Generate a random time string between start and end hour"""
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"


def random_time_components(start_hour, end_hour):
    """Generate random hour and minute components for a time between start and end hour"""
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    return hour, minute


# main code
# def start_cronjob():
#     """Start the cronjob scheduler using APScheduler for better performance"""

#     # Create a background scheduler
#     scheduler = BackgroundScheduler(timezone=uk_timezone)

#     # Add a job listener to log job execution
#     def job_listener(event):
#         if event.exception:
#             print(Fore.RED + f"[-] Job failed: {event.exception}")
#         else:
#             print(Fore.GREEN + f"[+] Job executed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

#     scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

#     # Determine schedule based on UK day of week
#     uk_day = get_uk_time().weekday()

#     # Set up the cron schedule based on the day of week
#     if uk_day == 0:  # Monday
#         # Monday afternoon (3-5 PM)
#         hour, minute = random_time_components(15, 17)
#         cron_schedule = f"{minute} {hour} * * 0"  # 0 = Monday in cron
#         time_desc = f"{hour}:{minute:02d} PM"
#     elif uk_day == 4:  # Friday
#         # Friday morning (8-11 AM)
#         hour, minute = random_time_components(8, 11)
#         cron_schedule = f"{minute} {hour} * * 4"  # 4 = Friday in cron
#         time_desc = f"{hour}:{minute:02d} AM"
#     elif uk_day in [1, 2, 3]:  # Tuesday, Wednesday, Thursday
#         # Choose from optimal time slots
#         time_slots = [
#             (8, 10),    # Morning: 8 AM - 10 AM
#             (12, 13),   # Lunch: 12 PM - 1 PM
#             (16, 17)    # Afternoon: 4 PM - 5 PM
#         ]

#         start_hour, end_hour = random.choice(time_slots)
#         hour, minute = random_time_components(start_hour, end_hour)
#         cron_schedule = f"{minute} {hour} * * {uk_day}"
#         time_desc = f"{hour}:{minute:02d}" + (" AM" if hour < 12 else " PM")
#     else:  # Weekend
#         print(Fore.YELLOW + "[!] Today is a weekend. No emails will be sent.")
#         return

#     # Add the job with a cron trigger
#     scheduler.add_job(
#         run_daily_email_campaign,
#         CronTrigger.from_crontab(cron_schedule),
#         id='daily_email_campaign',
#         replace_existing=True
#     )

#     # Print schedule information
#     print(Fore.GREEN + f"[+] Emails scheduled to send at {time_desc} UK time")
#     print(Fore.GREEN + f"[+] Cron schedule: {cron_schedule}")

#     # Print all scheduled jobs
#     print(Fore.CYAN + "[*] Scheduled jobs:")
#     for job in scheduler.get_jobs():
#       try:
#         next_run = job.next_run_time if hasattr(job, 'next_run_time') else "Not scheduled"
#         print(Fore.CYAN + f"    - {job.id} (Next run: {next_run})")
#       except AttributeError:
#         # For older versions of APScheduler or schedule module
#         job_info = str(job)
#         print(Fore.CYAN + f"    - {job_info}")

#     # Start the scheduler
#     scheduler.start()

#     # Keep the main thread alive
#     try:
#     # Display a running counter instead of just sleeping
#       print(Fore.YELLOW + "[!] Scheduler running. Press Ctrl+C to exit.")
#       count = 0
#       while True:
#         time.sleep(1)
#         count += 1
#         if count % 60 == 0:  # Every minute
#             # Show next run time
#             jobs = scheduler.get_jobs()
#             if jobs:
#                 for job in jobs:
#                     try:
#                         next_run = getattr(job, 'next_run_time', None)
#                         if next_run:
#                             current_time = datetime.now(uk_timezone)
#                             if hasattr(next_run, 'tzinfo') and next_run.tzinfo is None:
#                                 next_run = next_run.replace(tzinfo=uk_timezone)

#                             time_remaining = next_run - current_time
#                             hours, remainder = divmod(time_remaining.total_seconds(), 3600)
#                             minutes, seconds = divmod(remainder, 60)

#                             if time_remaining.total_seconds() > 0:
#                                 print(Fore.CYAN + f"[*] Next email batch in: {int(hours)}h {int(minutes)}m {int(seconds)}s")
#                             else:
#                                 print(Fore.CYAN + f"[*] Job running now or scheduled to run very soon")
#                             break
#                     except (AttributeError, TypeError) as e:
#                         print(Fore.YELLOW + f"[!] Could not determine next run time: {e}")
#             else:
#                 print(Fore.YELLOW + f"[!] No scheduled jobs found")
#     except KeyboardInterrupt:
#         scheduler.shutdown()
#         print(Fore.YELLOW + "\n[!] Scheduler stopped.")


def start_cronjob():
    """Start the cronjob scheduler using APScheduler for better performance"""

    # Create a background scheduler with Pakistan timezone
    scheduler = BackgroundScheduler(
        timezone=uk_timezone
    )  # uk_timezone is actually set to 'Asia/Karachi'

    # Add a job listener to log job execution
    def job_listener(event):
        if event.exception:
            print(Fore.RED + f"[-] Job failed: {event.exception}")
        else:
            print(
                Fore.GREEN
                + f"[+] Job executed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    # Get current time in Pakistan timezone
    current_time = get_uk_time()

    # Determine schedule based on Pakistan day of week
    pakistan_day = current_time.weekday()

    # Define day names for better output
    day_names = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # Print current time information
    print(
        Fore.GREEN
        + f"[+] Current time in Pakistan: {current_time.strftime('%Y-%m-%d %H:%M:%S')} ({day_names[pakistan_day]})"
    )

    # Add a one-time job to run in next few minutes for immediate testing
    run_time = current_time + timedelta(minutes=5)
    scheduler.add_job(
        run_daily_email_campaign,
        "date",
        run_date=run_time,
        id="today_campaign",
        replace_existing=True,
    )
    print(
        Fore.GREEN
        + f"[+] Job scheduled to run today at {run_time.strftime('%H:%M:%S')} Pakistan time (in 5 minutes)"
    )

    # Define optimal time slots for each day of the week based on Pakistan time
    # Each tuple represents (start_hour, end_hour) in 24-hour format
    optimal_slots = {
        0: [(17, 18), (21, 22)],  # Monday: 5-6:30 PM, 9-10:30 PM
        1: [(13, 15), (17, 18), (21, 22)],  # Tuesday: 1-3 PM, 5-6:30 PM, 9-10:30 PM
        2: [(13, 15), (17, 18), (21, 22)],  # Wednesday: 1-3 PM, 5-6:30 PM, 9-10:30 PM
        3: [(13, 15), (17, 18), (21, 22)],  # Thursday: 1-3 PM, 5-6:30 PM, 9-10:30 PM
        4: [(13, 15), (17, 18)],  # Friday: 1-3 PM, 5-6:30 PM (avoid after 8 PM)
        5: [],  # Saturday: No optimal slots
        6: [],  # Sunday: No optimal slots
    }

    # Display the optimal sending times for the current week
    print(
        Fore.CYAN
        + "\n[*] Optimal sending times for this week (Pakistan Time, PKT - GMT+5):"
    )

    # Calculate the start of the current week (Monday)
    start_of_week = current_time - timedelta(days=pakistan_day)
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # Show schedule for each day in the current week
    for day_offset in range(7):
        day_date = start_of_week + timedelta(days=day_offset)
        day_of_week = day_date.weekday()
        day_slots = optimal_slots[day_of_week]

        # Format date as "Monday (April 3)"
        formatted_date = day_date.strftime(f"{day_names[day_of_week]} (%B %d)")

        if day_slots:
            slot_descriptions = []
            for start_hour, end_hour in day_slots:
                start_time = f"{start_hour if start_hour <= 12 else start_hour-12}:00 {'AM' if start_hour < 12 else 'PM'}"
                end_time = f"{end_hour if end_hour <= 12 else end_hour-12}:00 {'AM' if end_hour < 12 else 'PM'}"
                slot_descriptions.append(f"{start_time} - {end_time}")

            status = "TODAY" if day_of_week == pakistan_day else ""
            print(
                Fore.GREEN
                + f"  • {formatted_date}: {', '.join(slot_descriptions)} {status}"
            )
        else:
            print(
                Fore.RED
                + f"  • {formatted_date}: No scheduled emails (Weekend/Holiday)"
            )

    print("\n")

    # Calculate the next business day and its optimal slots
    # If today is Friday (4), the next business day is Monday (0)
    # If today is any other day, the next business day is tomorrow
    next_day = 0 if pakistan_day == 4 else (pakistan_day + 1) % 7

    # If tomorrow is weekend, we need to go to Monday
    if next_day in [5, 6]:
        next_day = 0

    # Get the available time slots for the next business day
    next_day_slots = optimal_slots[next_day]

    if not next_day_slots:
        print(
            Fore.YELLOW
            + f"[!] No optimal time slots available for next business day (day {next_day})."
        )
        return

    # Choose a random time slot from the available ones
    start_hour, end_hour = random.choice(next_day_slots)

    # Generate random hour and minute within the chosen slot
    hour, minute = random_time_components(start_hour, end_hour)

    # Calculate the date for the next business day
    days_ahead = 1
    if pakistan_day == 4:  # Friday -> Monday
        days_ahead = 3
    elif pakistan_day == 5:  # Saturday -> Monday
        days_ahead = 2
    elif pakistan_day == 6:  # Sunday -> Monday
        days_ahead = 1

    next_run_date = current_time + timedelta(days=days_ahead)
    next_run_date = next_run_date.replace(
        hour=hour, minute=minute, second=0, microsecond=0
    )

    # Format time description for display
    if hour >= 12:
        hour_12 = hour - 12 if hour > 12 else 12
        time_desc = f"{hour_12}:{minute:02d} PM"
    else:
        time_desc = f"{hour}:{minute:02d} AM"

    # Add the job for the next business day using a specific run date instead of cron
    scheduler.add_job(
        run_daily_email_campaign,
        "date",
        run_date=next_run_date,
        id="next_business_day_campaign",
        replace_existing=True,
    )

    # Calculate human-readable day name for output
    next_day_name = day_names[next_day]

    # Print schedule information
    print(
        Fore.GREEN
        + f"[+] Next business day email scheduled for {next_day_name} at {time_desc} Pakistan time"
    )
    print(
        Fore.GREEN + f"[+] Next run date: {next_run_date.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # Print all scheduled jobs
    print(Fore.CYAN + "[*] Scheduled jobs:")
    for job in scheduler.get_jobs():
        try:
            next_run = (
                job.next_run_time if hasattr(job, "next_run_time") else "Not scheduled"
            )
            print(Fore.CYAN + f"    - {job.id} (Next run: {next_run})")
        except AttributeError:
            # For older versions of APScheduler or schedule module
            job_info = str(job)
            print(Fore.CYAN + f"    - {job_info}")

    # Start the scheduler
    scheduler.start()

    # Keep the main thread alive
    try:
        # Display a running counter instead of just sleeping
        print(Fore.YELLOW + "[!] Scheduler running. Press Ctrl+C to exit.")
        count = 0
        while True:
            time.sleep(1)
            count += 1
            if count % 60 == 0:  # Every minute
                # Show next run time
                jobs = scheduler.get_jobs()
                if jobs:
                    for job in jobs:
                        try:
                            next_run = getattr(job, "next_run_time", None)
                            if next_run:
                                current_time = datetime.now(
                                    uk_timezone
                                )  # Get current Pakistan time
                                if (
                                    hasattr(next_run, "tzinfo")
                                    and next_run.tzinfo is None
                                ):
                                    next_run = next_run.replace(tzinfo=uk_timezone)

                                time_remaining = next_run - current_time
                                hours, remainder = divmod(
                                    time_remaining.total_seconds(), 3600
                                )
                                minutes, seconds = divmod(remainder, 60)

                                if time_remaining.total_seconds() > 0:
                                    print(
                                        Fore.CYAN
                                        + f"[*] Next email batch in: {int(hours)}h {int(minutes)}m {int(seconds)}s"
                                    )
                                else:
                                    print(
                                        Fore.CYAN
                                        + f"[*] Job running now or scheduled to run very soon"
                                    )
                                break
                        except (AttributeError, TypeError) as e:
                            print(
                                Fore.YELLOW
                                + f"[!] Could not determine next run time: {e}"
                            )
                else:
                    print(Fore.YELLOW + f"[!] No scheduled jobs found")
    except KeyboardInterrupt:
        scheduler.shutdown()
        print(Fore.YELLOW + "\n[!] Scheduler stopped.")


def reset_sent_records():
    """Reset the sent records file"""
    sent_records = {"sent_emails": [], "last_run_date": None}
    save_sent_records(sent_records)
    print(Fore.GREEN + "[+] Sent records have been reset.")


def show_sent_records():
    """Show the current sent records"""
    sent_records = load_sent_records()
    print(
        Fore.GREEN + f"[+] Last run date: {sent_records.get('last_run_date', 'Never')}"
    )
    print(
        Fore.GREEN
        + f"[+] Total emails sent: {len(sent_records.get('sent_emails', []))}"
    )

    if sent_records.get("sent_emails"):
        print(Fore.CYAN + "[*] First 10 sent emails:")
        for i, email in enumerate(sent_records.get("sent_emails", [])[:10]):
            print(Fore.CYAN + f"    {i+1}. {email}")


def run_once_now():
    """Run the email campaign once right now"""
    print(Fore.YELLOW + "[!] Running email campaign immediately...")
    run_daily_email_campaign()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UK Cold Email Cronjob Scheduler")
    parser.add_argument("--reset", action="store_true", help="Reset sent records")
    parser.add_argument("--show", action="store_true", help="Show sent records")
    parser.add_argument("--now", action="store_true", help="Run once immediately")
    parser.add_argument("--limit", type=int, help="Set daily email limit (default: 10)")
    args = parser.parse_args()

    try:
        # Process command line arguments
        if args.reset:
            reset_sent_records()
            sys.exit(0)

        if args.show:
            show_sent_records()
            sys.exit(0)

        if args.limit:
            DAILY_EMAIL_LIMIT = args.limit
            print(Fore.GREEN + f"[+] Daily email limit set to {DAILY_EMAIL_LIMIT}")

        # Run immediately if requested
        if args.now:
            run_once_now()
        else:
            # Start the cronjob scheduler
            start_cronjob()

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Cronjob scheduler stopped by user")
    except Exception as e:
        print(Fore.RED + f"\n[-] Error: {str(e)}")
