# 🚀 Quick Deploy Guide

## Your app is ready to deploy! Here's the fastest way:

### Option 1: Railway (Easiest - 5 minutes)

1. **Install Railway CLI** (if not installed):
   ```bash
   npm install -g @railway/cli
   ```

2. **Run the deploy script**:
   ```bash
   deploy.bat
   ```
   
   Or manually:
   ```bash
   git init
   git add .
   git commit -m "Deploy DSA Tracker"
   railway login
   railway init
   railway up
   ```

3. **Your app is live!** Railway will give you a URL like:
   `https://your-app.railway.app`

---

### Option 2: Render (Free tier, good alternative)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Deploy DSA Tracker"
   git remote add origin YOUR_GITHUB_URL
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Build Command**: `pip install -r requirements.txt && python init_database.py && python init_auth.py`
     - **Start Command**: `gunicorn app:app`

3. **Your app is live!** Render will give you a URL.

---

## ✅ What's been prepared:

- ✅ **app.py** - Production Flask server
- ✅ **requirements.txt** - All dependencies listed
- ✅ **Procfile** - Deployment configuration
- ✅ **runtime.txt** - Python version
- ✅ **.gitignore** - Excluded unnecessary files
- ✅ **deploy.bat** - Automated deployment script

---

## 📝 Important Notes:

1. **Database**: Your SQLite database (18,668 problems) will be deployed automatically
2. **Authentication**: All users and sessions work on the deployed app
3. **Free Tier**: Both Railway and Render offer free hosting
4. **First Load**: May take 10-30 seconds on free tier after inactivity

---

## 🔧 Test Locally First (Optional):

```bash
# Install dependencies
pip install -r requirements.txt

# Run production server
python app.py
```

Visit: http://localhost:8000

---

## 🆘 Need Help?

Check **DEPLOYMENT.md** for detailed instructions and troubleshooting.

---

## 🎯 Fastest Deploy (One Command):

```bash
deploy.bat
```

That's it! The script handles everything. 🎉
