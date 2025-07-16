#!/usr/bin/env python3
"""
Test script for yoga monitor notifications
Run this to test email and Telegram notifications
"""

import os
from yoga_monitor import YogaMonitor

def test_notifications():
    """Test notification systems with mock data"""
    
    # Load environment variables from .env file if it exists
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    monitor = YogaMonitor()
    
    # Mock available classes data
    mock_classes = [
        {
            'name': 'Hatha Yoga',
            'time': '18:00',
            'date': '2024-01-15',
            'spots': 3
        },
        {
            'name': 'Vinyasa Flow',
            'time': '19:30',
            'date': '2024-01-15',
            'spots': 1
        }
    ]
    
    print("Testing notification systems...")
    print("Mock data:")
    for cls in mock_classes:
        print(f"  - {cls['name']} on {cls['date']} at {cls['time']} ({cls['spots']} spots)")
    print()
    
    # Test notifications
    success = monitor.send_notifications(mock_classes)
    
    if success:
        print("✅ Notification test completed successfully!")
    else:
        print("❌ No notifications were sent. Check your configuration.")
        print("\nConfiguration status:")
        print(f"  Email configured: {'✅' if monitor.email_user and monitor.notify_email else '❌'}")
        print(f"  Telegram configured: {'✅' if monitor.telegram_bot and monitor.telegram_chat_id else '❌'}")
        print("\nMake sure to:")
        print("1. Copy config.example.env to .env")
        print("2. Fill in your notification credentials")
        print("3. Run this test again")

if __name__ == "__main__":
    test_notifications()