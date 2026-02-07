# 🚀 DSA Problem Tracker - Deployment Guide

## Deployed Files Overview

Your application is now ready for deployment with the following production files:

- **app.py** - Production Flask server (replaces server.py)
- **requirements.txt** - Python dependencies
- **Procfile** - Deployment startup command
- **runtime.txt** - Python version specification
- **.gitignore** - Files to exclude from git

## 📦 Railway Deployment (Recommended - Free Tier)

### Prerequisites
1. Create a [Railway](https://railway.app) account (free)
2. Install [Git](https://git-scm.com/) if not already installed

### Step 1: Initialize Git Repository
```bash
cd "c:\Users\C. Tinesh Karthick\Music\Project\DSA"
git init
git add .
git commit -m "Initial commit - DSA Problem Tracker"
```

### Step 2: Initialize Database (Before Deploying)
```bash
python init_database.py
python init_auth.py
```

### Step 3: Deploy to Railway

#### Option A: Deploy via GitHub (Recommended)
1. Create a new repository on [GitHub](https://github.com)
2. Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git branch -M main
   git push -u origin main
   ```
3. Go to [Railway Dashboard](https://railway.app/dashboard)
4. Click "New Project" → "Deploy from GitHub repo"
5. Select your repository
6. Railway will automatically detect Python and deploy!

#### Option B: Deploy via Railway CLI
1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```
2. Login:
   ```bash
   railway login
   ```
3. Initialize and deploy:
   ```bash
   railway init
   railway up
   ```

### Step 4: Configure Railway
1. Your app will be live at: `https://YOUR-APP.railway.app`
2. The database will persist on Railway's storage

### Important: Database Initialization on Railway
Since Railway starts fresh, you need to initialize the database once deployed:

1. Go to Railway Dashboard → Your Project → Settings
2. Add these build commands in Railway settings:
   - **Build Command**: `pip install -r requirements.txt && python init_database.py && python init_auth.py`
   - **Start Command**: `gunicorn app:app`

Or manually via Railway CLI:
```bash
railway run python init_database.py
railway run python init_auth.py
```

---

## 🎨 Render Deployment (Alternative - Free Tier)

### Step 1: Push to GitHub (Same as Railway Step 1 & 2)

### Step 2: Deploy to Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: dsa-problem-tracker
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python init_database.py && python init_auth.py`
   - **Start Command**: `gunicorn app:app`
5. Click "Create Web Service"

### Step 3: Access Your App
Your app will be live at: `https://YOUR-APP.onrender.com`

---

## 🐳 Docker Deployment (For VPS/Self-Hosting)

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize database
RUN python init_database.py && python init_auth.py

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Build and Run
```bash
docker build -t dsa-tracker .
docker run -p 8000:8000 -v $(pwd)/dsa_problems.db:/app/dsa_problems.db dsa-tracker
```

---

## ⚙️ Configuration Notes

### Database Persistence
- SQLite database (`dsa_problems.db`) must persist between deployments
- Railway: Automatically handles volume persistence
- Render: Use Render Disks for persistence
- Docker: Use volume mounting (shown above)

### Environment Variables (Optional)
Create `.env` file for configuration:
```env
PORT=8000
DB_PATH=./dsa_problems.db
```

---

## 🧪 Local Testing Before Deployment

Test the production server locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Run production server
gunicorn app:app --bind 0.0.0.0:8000
```

Then visit: `http://localhost:8000`

---

## 📊 Post-Deployment Checklist

- ✅ Database initialized (18,668+ problems)
- ✅ Authentication tables created
- ✅ Can register a new user
- ✅ Can login with credentials
- ✅ Can browse companies
- ✅ Can track problem progress
- ✅ Sessions persist after page reload

---

## 🔧 Troubleshooting

### Database Not Found Error
```bash
# Manually initialize on Railway/Render
railway run python init_database.py
railway run python init_auth.py
```

### Port Issues
- Railway: Uses `PORT` environment variable automatically
- Render: Uses `PORT` environment variable automatically
- If deploying elsewhere, ensure port 8000 is accessible

### CSS/JS Not Loading
- Check that all HTML files reference relative paths
- Ensure static files are in the same directory as app.py

### Build Fails
- Check Python version matches runtime.txt
- Verify all dependencies in requirements.txt
- Check Railway/Render build logs for errors

---

## 🎯 Quick Deployment Commands

### Railway (Fastest)
```bash
git init
git add .
git commit -m "Deploy DSA Tracker"
railway init
railway up
```

### Render (Via GitHub)
```bash
git init
git add .
git commit -m "Deploy DSA Tracker"
git push origin main
# Then connect on Render Dashboard
```

---

## 📱 Access Your Deployed App

After deployment, your app will be accessible at:
- **Railway**: `https://YOUR-PROJECT.railway.app`
- **Render**: `https://YOUR-APP.onrender.com`

Share this URL with anyone to access your DSA Problem Tracker! 🎉

---

## 💡 Pro Tips

1. **Free Tier Limitations**:
   - Railway: 500 hours/month free
   - Render: 750 hours/month free
   
2. **Keep It Running**:
   - Both platforms may sleep after inactivity
   - First request may take 10-30 seconds to wake up
   
3. **Backup Your Database**:
   - Download `dsa_problems.db` regularly from Railway/Render
   - Store backup safely

4. **Custom Domain** (Optional):
   - Both Railway and Render support custom domains
   - Add in project settings after deployment

---

Need help? Check the platform documentation:
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
