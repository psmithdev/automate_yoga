# API Capture Guide for Jetts Thailand App

This guide will help you capture the API endpoints from the Jetts Thailand Android app so the yoga monitor can check class availability.

## Method 1: Using mitmproxy (Recommended)

### Setup
1. Install mitmproxy on your computer:
   ```bash
   pip install mitmproxy
   ```

2. Start mitmproxy:
   ```bash
   mitmweb --listen-port 8080
   ```

3. Configure your Android phone:
   - Connect to same WiFi as your computer
   - Go to WiFi settings → Modify network → Advanced
   - Set proxy to Manual
   - Proxy hostname: Your computer's IP address
   - Proxy port: 8080

4. Install mitmproxy certificate:
   - Open browser on phone and go to mitm.it
   - Download and install the certificate

### Capturing API Calls
1. Open the Jetts Thailand app
2. Navigate to yoga class booking/viewing
3. Check available classes, attempt booking, etc.
4. Monitor mitmweb interface for API calls

### What to Look For
- **Base URL**: Usually something like `https://api.jetts.com` or `https://jetts-api.example.com`
- **Authentication**: Look for Authorization headers, API keys, or session tokens
- **Class listing endpoint**: Endpoint that returns available classes
- **User identification**: User ID, member number, or similar identifiers

## Method 2: Using Charles Proxy

### Setup
1. Download Charles Proxy (30-day free trial)
2. Start Charles and enable proxy on port 8888
3. Configure Android phone proxy settings (similar to mitmproxy)
4. Install Charles certificate on phone

### Capturing
1. Use the app while Charles is recording
2. Look for HTTPS requests to Jetts servers
3. Examine request/response data

## Method 3: Android Debug Bridge (ADB)

### Setup
1. Enable Developer Options on Android
2. Enable USB Debugging
3. Connect phone to computer
4. Install ADB tools

### Capturing
```bash
adb logcat | grep -i "http\|api\|jetts"
```

## Information to Collect

Once you identify the API calls, document:

1. **Base URL**
   ```
   Example: https://api.jetts.com/v1
   ```

2. **Authentication Method**
   ```
   Header: Authorization: Bearer <token>
   OR
   Header: X-API-Key: <key>
   OR
   Cookie: session_id=<id>
   ```

3. **Class Listing Endpoint**
   ```
   GET /classes/yoga?location=<location_id>&date=<date>
   ```

4. **Required Headers**
   ```
   User-Agent: JettsApp/1.2.3 (Android)
   Accept: application/json
   Authorization: Bearer <token>
   ```

5. **Sample Response Structure**
   ```json
   {
     "classes": [
       {
         "id": "123",
         "name": "Hatha Yoga",
         "time": "18:00",
         "date": "2024-01-15",
         "instructor": "Jane Doe",
         "available_spots": 5,
         "total_spots": 20
       }
     ]
   }
   ```

## Updating the Monitor Script

After capturing the API details, update `yoga_monitor.py`:

1. Set `api_base_url` in the constructor
2. Add authentication headers to `self.headers`
3. Update the `check_yoga_classes()` method with the correct endpoint
4. Modify the response parsing logic to match the actual API response structure

## Testing

Create a simple test script to verify API access:

```python
import requests

headers = {
    'Authorization': 'Bearer YOUR_TOKEN',
    'User-Agent': 'JettsApp/1.2.3'
}

response = requests.get(
    'https://api.jetts.com/v1/classes/yoga',
    headers=headers
)

print(response.status_code)
print(response.json())
```

## Certificate Pinning Solutions

If the app uses certificate pinning (no traffic visible in proxy), try these methods:

### Method A: Frida (Recommended for non-rooted phones)
1. Install Frida tools:
   ```bash
   pip install frida-tools
   ```

2. Download and run Frida server on device:
   ```bash
   # Download frida-server for your Android architecture from GitHub
   adb push frida-server /data/local/tmp/
   adb shell "chmod 755 /data/local/tmp/frida-server"
   adb shell "/data/local/tmp/frida-server &"
   ```

3. Use SSL Kill Switch:
   ```bash
   # Download ssl-kill-switch.js from GitHub
   frida -U -l ssl-kill-switch.js -f com.jetts.app
   ```

4. Now run mitmproxy and use the app - traffic should be visible

### Method B: Check for Web Version
Many fitness apps have mobile web versions without certificate pinning:
- Try logging into Jetts via mobile browser
- Check if class booking works on web
- Capture web API calls instead

### Method C: APK Patching (Advanced)
1. Extract APK using APK Extractor
2. Decompile with apktool
3. Find and modify certificate pinning code
4. Recompile and install modified APK

## Security Notes

- Keep API tokens and credentials secure
- Don't commit real credentials to git
- Use environment variables for sensitive data
- Certificate pinning is a security feature - bypass only for legitimate automation