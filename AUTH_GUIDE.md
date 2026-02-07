# 🔐 DSA Problem Tracker - Authentication Guide

## Overview
Your DSA Problem Tracker now includes a secure authentication system with user registration, login, and session management.

## Features

### ✨ New Authentication Features
- **User Registration**: Create a new account with username, email, and password
- **Secure Login**: Password hashing with PBKDF2-HMAC-SHA256
- **Session Management**: 7-day session tokens stored securely
- **Protected Routes**: All pages require authentication to access
- **User Display**: Shows logged-in username in the header
- **Easy Logout**: Quick logout button available on all pages

## How to Use

### First Time Setup
1. **Initialize Database** (if not done already):
   ```bash
   python init_database.py
   ```

2. **Initialize Authentication Tables**:
   ```bash
   python init_auth.py
   ```

3. **Start the Server**:
   ```bash
   python server.py
   ```

4. **Open in Browser**:
   Navigate to `http://localhost:8000/login.html`

### Creating an Account
1. Click the "Register" tab on the login page
2. Enter your desired username (minimum 3 characters)
3. Enter your email address
4. Create a password (minimum 6 characters)
5. Confirm your password
6. Click "Register"
7. After successful registration, you'll be redirected to the login tab

### Logging In
1. Enter your username
2. Enter your password
3. Click "Login"
4. You'll be automatically redirected to the company selection page

### Using the Application
- Once logged in, you can:
  - Browse all 469 companies
  - Track problems for each company
  - Mark problems as Solved (✓), Tried (~), or Unsolved (✗)
  - Filter problems by duration, difficulty, and status
  - Export your progress as JSON
  - Your progress is saved automatically

### Logging Out
- Click the "Logout" button in the top-right corner of any page
- Confirm the logout action
- You'll be redirected to the login page

## Security Features

### Password Security
- Passwords are hashed using PBKDF2-HMAC-SHA256
- Each password uses a unique random salt
- 100,000 iterations for enhanced security
- Passwords are never stored in plain text

### Session Management
- Session tokens are 32-byte URL-safe random strings
- Sessions expire after 7 days
- Tokens are stored in localStorage for persistence
- Session validation on every page load

### Data Protection
- SQLite database with proper foreign key constraints
- User data isolated by user_id
- Automatic cleanup of expired sessions
- Input validation on all forms

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sessions Table
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### User Progress Table
```sql
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    problem_id INTEGER NOT NULL,
    company TEXT NOT NULL,
    status TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, problem_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);
```

## API Endpoints

### Authentication Endpoints
- `POST /api/register` - Register a new user
- `POST /api/login` - Login with credentials
- `GET /api/check-session` - Verify session token validity

### Application Endpoints
- `GET /api/companies` - Get all companies
- `GET /api/problems` - Get problems with filters
- `GET /api/stats` - Get statistics

## Troubleshooting

### Can't Access Application
- Make sure you're logged in
- Check if your session has expired (sessions last 7 days)
- Try logging out and logging back in

### Registration Fails
- Username must be at least 3 characters
- Email must be valid
- Password must be at least 6 characters
- Username and email must be unique

### Login Fails
- Verify your username and password are correct
- Usernames are case-sensitive
- Make sure the server is running

### Server Won't Start
```bash
# Check if database exists
ls dsa_problems.db

# Reinitialize authentication tables
python init_auth.py

# Restart server
python server.py
```

## File Structure
```
DSA/
├── login.html              # Login and registration page
├── index.html              # Company selection page (protected)
├── problems.html           # Problem viewer page (protected)
├── server.py               # Server with authentication
├── init_auth.py            # Authentication database setup
├── init_database.py        # Main database setup
├── dsa_problems.db         # SQLite database
└── data/                   # CSV files by company
```

## Tips
- 💡 Keep your session active by accessing the app within 7 days
- 💡 Use a strong password even for local development
- 💡 Each user has their own independent progress tracking
- 💡 Your data is stored locally in the SQLite database
- 💡 Export your progress regularly as backup

## Support
If you encounter any issues, check:
1. Is the server running? (`python server.py`)
2. Are all database tables initialized? (`python init_auth.py`)
3. Are you accessing the correct URL? (`http://localhost:8000/login.html`)
