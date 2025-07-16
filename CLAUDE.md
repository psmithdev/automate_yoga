# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a yoga class availability automation project for Jetts Thailand. The system monitors yoga class availability through the mobile app's API and sends notifications when spots become available.

## Repository Structure

- `yoga_monitor.py` - Main monitoring script with notification capabilities
- `test_notifications.py` - Test script for email and Telegram notifications
- `requirements.txt` - Python dependencies
- `config.example.env` - Configuration template
- `API_CAPTURE_GUIDE.md` - Instructions for capturing app API endpoints
- `.gitignore` - Protects sensitive configuration files

## Development Commands

### Setup
```bash
pip install -r requirements.txt
cp config.example.env .env
# Edit .env with your credentials
```

### Testing
```bash
python test_notifications.py  # Test notification systems
python yoga_monitor.py        # Run single check (API endpoints needed)
```

### Configuration Required
Before the monitor can work, you need to:
1. Follow `API_CAPTURE_GUIDE.md` to capture Jetts app API endpoints
2. Update `yoga_monitor.py` with actual API details
3. Configure notification credentials in `.env`

## Architecture Notes

The `YogaMonitor` class handles:
- API requests to Jetts Thailand backend
- Email notifications via SMTP
- Telegram notifications via bot API
- Continuous monitoring with configurable intervals

The system is designed to run on a DigitalOcean droplet for 24/7 monitoring.