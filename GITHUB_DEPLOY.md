# 🚀 Deploy via GitHub - Complete Guide

## Why GitHub + Railway/Render?

- ✅ Free code hosting on GitHub
- ✅ Automatic deployments when you push code
- ✅ Full backend support (Python, database, authentication)
- ✅ Easy rollbacks and version control
- ✅ Professional workflow

---

## 📦 Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `dsa-problem-tracker`
3. Keep it **Public** (required for free deployment)
4. **Don't** initialize with README (we already have files)
5. Click "Create repository"

### Step 2: Push Code to GitHub

Open PowerShell in your project folder and run:

```powershell
# Initialize git (if not done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - DSA Problem Tracker with authentication"

# Add your GitHub repository (replace with YOUR username)
git remote add origin https://github.com/YOUR_USERNAME/dsa-problem-tracker.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username!

### Step 3: Deploy to Railway (From GitHub)

#### 3a. Connect Railway to GitHub

1. Go to https://railway.app/
2. Sign up/Login (use "Login with GitHub" for easy setup)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Authorize Railway to access your repositories
6. Select `dsa-problem-tracker`

#### 3b. Configure Build Settings

Railway will auto-detect Python, but verify:

1. In Railway Dashboard → Your Project → Settings
2. **Build Command** (optional - Railway auto-detects):
   ```
   pip install -r requirements.txt
   ```
3. **Start Command** (should auto-detect from Procfile):
   ```
   gunicorn app:app
   ```

#### 3c. Initialize Database

After first deployment, run these commands in Railway:

```bash
railway run python init_database.py
railway run python init_auth.py
```

Or via Railway CLI:
```bash
railway login
railway link
railway run python init_database.py
railway run python init_auth.py
```

### Step 4: Deploy to Render (Alternative)

#### 4a. Connect Render to GitHub

1. Go to https://dashboard.render.com/
2. Sign up/Login (use "Login with GitHub")
3. Click "New +" → "Web Service"
4. Click "Connect GitHub"
5. Select `dsa-problem-tracker`

#### 4b. Configure Settings

Fill in these settings:

- **Name**: `dsa-problem-tracker`
- **Environment**: `Python 3`
- **Build Command**:
  ```
  pip install -r requirements.txt && python init_database.py && python init_auth.py
  ```
- **Start Command**:
  ```
  gunicorn app:app
  ```
- **Plan**: Free

Click "Create Web Service" and wait 2-3 minutes for deployment.

---

## 🔄 Automatic Deployments

Once connected, every time you push to GitHub, your app auto-redeploys! 🎉

### Update Your App

```powershell
# Make changes to your code
# ...

# Commit and push
git add .
git commit -m "Update: description of changes"
git push

# Railway/Render automatically redeploys!
```

---

## 🌐 Your Live URLs

After deployment, you'll get URLs like:

- **Railway**: `https://dsa-problem-tracker.railway.app`
- **Render**: `https://dsa-problem-tracker.onrender.com`

---

## 📋 Quick Commands Summary

```powershell
# First time setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/dsa-problem-tracker.git
git push -u origin main

# Future updates
git add .
git commit -m "Your update message"
git push
```

---

## ⚡ One-Command Deploy Script

Run this to automate the GitHub push:

```powershell
.\deploy.bat
```

Then select option 3 to push to GitHub.

---

## 🔧 Troubleshooting

### "Git not found"
Install Git: https://git-scm.com/download/win

### "Permission denied"
You need to authenticate with GitHub:
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### "Database not found" after deployment
Run these in Railway/Render CLI:
```bash
railway run python init_database.py
railway run python init_auth.py
```

### Changes not appearing
- Check if Railway/Render shows successful deployment
- Clear browser cache
- Check deployment logs for errors

---

## 🎯 Recommended Workflow

1. **Develop Locally**
   ```powershell
   python app.py
   ```

2. **Test Changes**
   Visit http://localhost:8000

3. **Push to GitHub**
   ```powershell
   git add .
   git commit -m "Feature: your changes"
   git push
   ```

4. **Auto-Deploy**
   Railway/Render deploys automatically in 2-3 minutes

5. **Verify Live**
   Check your live URL

---

## 📊 What Gets Deployed

✅ All HTML/CSS/JavaScript files
✅ Python Flask server (app.py)
✅ SQLite database (auto-initialized)
✅ Authentication system
✅ All 18,668 problems from 469 companies

---

## 💡 Pro Tips

1. **Branch Protection**: Create a `dev` branch for testing
   ```powershell
   git checkout -b dev
   # Make changes
   git push origin dev
   ```

2. **Environment Variables**: Store secrets in Railway/Render dashboard (not in code)

3. **Database Backups**: Download database regularly from Railway/Render

4. **Custom Domain**: Both platforms support custom domains in settings

---

## 🚀 Start Deploying Now!

1. Create GitHub repo: https://github.com/new
2. Run deploy script: `.\deploy.bat` (option 3)
3. Connect Railway: https://railway.app/
4. Done! Share your live URL! 🎉

---

## 📞 Support Links

- [Railway Documentation](https://docs.railway.app/)
- [Render Documentation](https://render.com/docs)
- [GitHub Guides](https://guides.github.com/)
