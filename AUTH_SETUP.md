# MachinaWorks - Full Authentication & Email Notifications Setup

## Overview
The platform now includes:
✅ Complete signup/login flow with email verification
✅ Admin email notifications for all form submissions
✅ Dashboard access for authenticated users
✅ Automatic email notifications to administrators

---

## Setup Instructions

### 1. Gmail Setup for Email Notifications

#### Step 1: Enable 2-Factor Authentication
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click "Security" in the left menu
3. Enable "2-Step Verification"

#### Step 2: Generate App Password
1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Windows Computer"
3. Google will generate a 16-character password
4. Copy this password

### 2. Update Environment Variables

Add these to your `.env.local` file:

```env
# Gmail Configuration (for email notifications)
GMAIL_USER=your-email@gmail.com
GMAIL_PASSWORD=your-16-char-app-password
ADMIN_EMAIL=admin@yourdomain.com

# Supabase Auth (already configured)
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

---

## Features

### Authentication Endpoints

#### Signup
**POST** `/api/auth/signup`
```json
{
  "email": "user@example.com",
  "password": "password123",
  "fullName": "John Doe"
}
```
- Creates new user in Supabase
- Sends admin notification email
- Sends confirmation email to user

#### Login
**POST** `/api/auth/login`
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
- Authenticates user
- Returns session token

### Form Notifications

#### Consultation Form Notification
**POST** `/api/forms/notify`
```json
{
  "formData": {
    "problem": "Need AI solution for X",
    "industry": "E-commerce",
    "companySize": "SMB",
    "email": "company@example.com"
  },
  "type": "consultation"
}
```

---

## User Flow

### Signup Flow
1. User clicks "Sign In" → Taken to `/auth` page
2. User selects "Sign Up" mode
3. Fills form: Name, Email, Password
4. System creates account in Supabase
5. ✉️ Admin receives email: "New Signup: John Doe"
6. ✉️ User receives confirmation email
7. Redirected to login screen

### Login Flow
1. User goes to `/auth` page
2. Enters email and password
3. System verifies credentials
4. Redirected to `/dashboard` (authenticated)
5. Can access personal consultations

### Consultation Flow
1. User fills consultation form on homepage
2. Form submitted to AI backend
3. AI analysis returned
4. ✉️ Admin receives: "New Consultation Request" with all details
5. ✉️ User receives confirmation email
6. User can view results

---

## Admin Email Content

### New Signup Notification
```
New User Registration

Name: John Doe
Email: john@company.com
Timestamp: 2026-01-21 10:30:45 AM
User ID: abc-123-def-456
```

### New Consultation Notification
```
New Consultation Request

Problem: Need AI to optimize customer service
Industry: E-commerce
Company Size: SMB
Email: company@example.com
Timestamp: 2026-01-21 10:30:45 AM
```

---

## Testing

### Test Signup
```bash
curl -X POST http://localhost:3003/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "fullName": "Test User"
  }'
```

### Test Login
```bash
curl -X POST http://localhost:3003/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Test Notification
```bash
curl -X POST http://localhost:3003/api/forms/notify \
  -H "Content-Type: application/json" \
  -d '{
    "formData": {
      "problem": "Need AI solution",
      "industry": "E-commerce",
      "companySize": "SMB",
      "email": "company@example.com"
    },
    "type": "consultation"
  }'
```

---

## Pages

- **Auth Page**: `/auth` - Login/Signup
- **Dashboard**: `/dashboard` - User consultations (authenticated)
- **Homepage**: `/` - With consultation form
- **Case Studies**: `/case-studies`

---

## Security Notes

✅ Passwords are hashed by Supabase
✅ Email verification enabled
✅ Service role key used only on server
✅ Anon key for client-side auth
✅ Gmail app password (limited scope)

---

## Troubleshooting

### "Failed to send notification email"
- Check GMAIL_USER and GMAIL_PASSWORD in .env
- Verify Gmail 2FA is enabled
- Verify app password is correct (16 chars)

### "Email address invalid"
- Ensure email format is correct
- Check database constraints in Supabase

### "Password too weak"
- Minimum 6 characters required
- Use strong password combinations

---

## Next Steps

1. Install `nodemailer`: `npm install nodemailer`
2. Update `.env.local` with Gmail credentials
3. Test signup at `/auth`
4. Check admin email for notifications
5. Access dashboard after login

