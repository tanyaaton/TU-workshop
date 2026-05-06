# Gmail and Calendar Service API

A REST API service for sending emails via Gmail SMTP and creating Google Calendar events. This API is designed to integrate with watsonx Orchestrate as a skill/tool for AI-powered automation.

## 🚀 Quick Start

### API Endpoint
```
https://be-gmail.28fksfbqmbmw.us-south.codeengine.appdomain.cloud
```

### Available Operations

#### 1. Send Email
Send an email via Gmail SMTP.

**Endpoint:** `POST /send-email`

**Request Body:**
```json
{
  "to": "recipient@example.com",
  "subject": "Meeting Invitation",
  "body": "You are invited to our meeting"
}
```

#### 2. Create Calendar Event
Create a Google Calendar event in a specific calendar.

**Endpoint:** `POST /create-calendar-event`

**Request Body:**
```json
{
  "summary": "Procurement Meeting",
  "description": "Discuss procurement requirements",
  "start": "20260220T140000",
  "end": "20260220T150000",
  "calendar_email": "your-calendar@gmail.com",
  "timezone": "Asia/Bangkok"
}
```

**Note:** The calendar must be shared with the service account email.

#### 3. Send Email and Create Calendar Event
Combined operation that sends an email invitation and creates a calendar event.

**Endpoint:** `POST /send-email-and-calendar-event`

**Request Body:**
```json
{
  "summary": "Procurement Meeting",
  "description": "Discuss procurement requirements",
  "start": "20260220T140000",
  "end": "20260220T150000",
  "email_attendees": ["attendee1@example.com", "attendee2@example.com"],
  "timezone": "Asia/Bangkok"
}
```

## 📋 OpenAPI Specification

The complete API specification is available in OpenAPI 3.0 format:
- **File:** `openapi_v3.json`
- **Endpoint:** `https://be-gmail.28fksfbqmbmw.us-south.codeengine.appdomain.cloud/openapi.json`

### Import to watsonx Orchestrate

1. Go to watsonx Orchestrate → Skills
2. Click "Add Skill" → "Import from OpenAPI"
3. Upload `openapi_v3.json` or use the endpoint URL
4. Configure authentication (if required)
5. Test the operations

## 🔧 Deployment & Configuration

All deployment files are located in the `backup/` folder:

- `app.py` - Main Flask application
- `Dockerfile` - Container configuration
- `requirements.txt` - Python dependencies
- `build_and_push.sh` - Build and push Docker image
- `deploy_code_engine.sh` - Deploy to IBM Cloud Code Engine

### Prerequisites

1. **Gmail Account Setup:**
   - Enable 2-factor authentication
   - Generate an app-specific password at: https://myaccount.google.com/apppasswords
   - Update `backup/.env` with your email and app password

2. **Google Cloud Service Account:**
   - Create a service account in Google Cloud Console
   - Enable Google Calendar API
   - Download service account key as `backup/credentials.json`
   - Copy the same content to `backup/token.json`

3. **Share Calendar with Service Account:**
   - Open Google Calendar settings
   - Share your calendar with the service account email
   - Grant "Make changes to events" permission

4. **IBM Cloud Setup:**
   - Create an IBM Cloud account
   - Set up Code Engine project
   - Update `backup/.env` with IBM Cloud credentials

### Configuration Files

Copy the example files and fill in your credentials:

```bash
cd backup/
cp .env.example .env
cp credentials.json.example credentials.json
# Edit .env and credentials.json with your actual credentials
```

### Deploy to IBM Cloud Code Engine

```bash
cd backup/

# Build and push Docker image
bash build_and_push.sh

# Deploy to Code Engine
bash deploy_code_engine.sh
```

## 📚 API Documentation

Interactive API documentation is available at:
- **Swagger UI:** `https://be-gmail.28fksfbqmbmw.us-south.codeengine.appdomain.cloud/apidocs/`

## 🔒 Security Notes

- **Never commit credentials** to version control
- The `.gitignore` file is configured to exclude sensitive files
- Use environment variables for all credentials
- Rotate credentials regularly
- Use IBM Cloud Secrets Manager for production deployments

## 📝 Date/Time Format

All date/time values use the format: `YYYYMMDDTHHMMSS`

Examples:
- `20260220T140000` = February 20, 2026, 2:00 PM
- `20260220T150000` = February 20, 2026, 3:00 PM

## 🌍 Supported Timezones

Common timezones:
- `Asia/Bangkok` (UTC+7)
- `America/New_York` (EST/EDT)
- `Europe/London` (GMT/BST)
- `Asia/Tokyo` (JST)

Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## 🐛 Troubleshooting

### Email Sending Fails
- Verify Gmail app-specific password is correct
- Check that 2FA is enabled on Gmail account
- Ensure SMTP access is not blocked

### Calendar Event Creation Fails
- Verify Google Calendar API is enabled
- Check that calendar is shared with service account
- Ensure service account has "Make changes to events" permission
- Verify `calendar_email` parameter matches the shared calendar

### Deployment Issues
- Check IBM Cloud credentials in `.env`
- Verify Docker/Podman is installed and running
- Ensure IBM Cloud CLI is installed and logged in

## 📞 Support

For issues or questions, please contact your system administrator or refer to the deployment documentation in the `backup/` folder.

## 📄 License

This API is provided for internal use. All rights reserved.