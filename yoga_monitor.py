#!/usr/bin/env python3
"""
Yoga Class Availability Monitor for Jetts Thailand
Checks for available yoga classes and sends notifications
"""

import requests
import smtplib
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os

class YogaMonitor:
    def __init__(self):
        # These will need to be configured after capturing API calls
        self.api_base_url = ""  # To be determined from app analysis
        self.headers = {}       # Authentication headers from app
        self.session = requests.Session()
        
        # Email configuration
        self.smtp_server = "smtp.gmail.com"  # or your preferred provider
        self.smtp_port = 587
        self.email_user = os.getenv('EMAIL_USER', '')
        self.email_pass = os.getenv('EMAIL_PASS', '')
        self.notify_email = os.getenv('NOTIFY_EMAIL', '')
        
    def check_yoga_classes(self):
        """Check for available yoga classes"""
        try:
            # This endpoint will be determined from app analysis
            response = self.session.get(
                f"{self.api_base_url}/classes/yoga",  # Placeholder endpoint
                headers=self.headers
            )
            response.raise_for_status()
            
            classes = response.json()
            available_classes = []
            
            # Parse response to find available classes
            # Structure will depend on actual API response
            for class_item in classes.get('classes', []):
                if class_item.get('available_spots', 0) > 0:
                    available_classes.append({
                        'name': class_item.get('name'),
                        'time': class_item.get('time'),
                        'spots': class_item.get('available_spots'),
                        'date': class_item.get('date')
                    })
            
            return available_classes
            
        except requests.RequestException as e:
            print(f"Error checking classes: {e}")
            return None
    
    def send_email_notification(self, available_classes):
        """Send email notification about available classes"""
        if not self.email_user or not self.notify_email:
            print("Email not configured")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = self.notify_email
            msg['Subject'] = "🧘 Yoga Classes Available!"
            
            body = "Available yoga classes:\n\n"
            for cls in available_classes:
                body += f"• {cls['name']} - {cls['date']} at {cls['time']} ({cls['spots']} spots)\n"
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            text = msg.as_string()
            server.sendmail(self.email_user, self.notify_email, text)
            server.quit()
            
            print(f"Notification sent at {datetime.now()}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def run_check(self):
        """Run a single check for available classes"""
        print(f"Checking for available yoga classes at {datetime.now()}")
        
        available_classes = self.check_yoga_classes()
        
        if available_classes is None:
            print("Failed to check classes")
            return
            
        if available_classes:
            print(f"Found {len(available_classes)} available classes!")
            self.send_email_notification(available_classes)
        else:
            print("No available classes found")
    
    def monitor_continuously(self, check_interval=300):  # 5 minutes default
        """Continuously monitor for available classes"""
        print(f"Starting continuous monitoring (checking every {check_interval} seconds)")
        
        while True:
            self.run_check()
            time.sleep(check_interval)

def main():
    monitor = YogaMonitor()
    
    # For testing, run a single check
    monitor.run_check()
    
    # For continuous monitoring, uncomment:
    # monitor.monitor_continuously()

if __name__ == "__main__":
    main()