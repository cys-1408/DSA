#!/usr/bin/env python3
"""
Free Deploy Helper Script
Helps you deploy to Render or PythonAnywhere for FREE
"""

import os
import subprocess
import webbrowser

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def run_command(cmd):
    """Run shell command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_git():
    """Check if git is installed"""
    success, _ = run_command("git --version")
    return success

def check_git_config():
    """Check if git is configured"""
    success, output = run_command("git config --global user.name")
    return success and output.strip() != ""

def main():
    print_header("🆓 FREE Deployment Helper - DSA Problem Tracker")
    
    # Check Git
    print("📋 Checking prerequisites...")
    if not check_git():
        print("❌ Git not found! Please install Git first:")
        print("   https://git-scm.com/download/win")
        return
    print("✅ Git is installed")
    
    # Check Git configuration
    if not check_git_config():
        print("\n⚠️  Git not configured. Let's set it up:")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        run_command(f'git config --global user.name "{name}"')
        run_command(f'git config --global user.email "{email}"')
        print("✅ Git configured")
    else:
        print("✅ Git is configured")
    
    # Check Git status
    if os.path.exists(".git"):
        print("✅ Git repository initialized")
        
        # Check if files are staged
        success, output = run_command("git status --porcelain")
        if output.strip():
            print("📦 Staging files...")
            run_command("git add .")
            print("✅ Files staged")
        
        # Create commit
        print("💾 Creating commit...")
        success, _ = run_command('git commit -m "Deploy DSA Problem Tracker"')
        if success:
            print("✅ Commit created")
        else:
            print("ℹ️  No changes to commit (already committed)")
    else:
        print("❌ Git not initialized! Run: git init")
        return
    
    print_header("Choose Your FREE Deployment Platform")
    
    print("1. ⭐ Render.com (RECOMMENDED)")
    print("   - Easiest deployment")
    print("   - No configuration needed")
    print("   - Auto-deploys from GitHub")
    print("   - 750 free hours/month")
    print("   - No credit card required")
    print()
    print("2. 🐍 PythonAnywhere")
    print("   - Always-on free tier")
    print("   - No sleep timer")
    print("   - Perfect for Python")
    print("   - No credit card required")
    print()
    print("3. 📚 View deployment guide")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        print_header("🚀 Deploying to Render")
        
        print("📝 Step 1: Push to GitHub")
        print("\nDo you have a GitHub repository created?")
        has_repo = input("(yes/no): ").strip().lower()
        
        if has_repo == "yes":
            repo_url = input("Enter your GitHub repository URL: ").strip()
            
            # Check if remote exists
            success, _ = run_command("git remote get-url origin")
            if not success:
                print("Adding GitHub remote...")
                run_command(f"git remote add origin {repo_url}")
            
            print("\n📤 Pushing to GitHub...")
            success, output = run_command("git push -u origin main")
            if success:
                print("✅ Code pushed to GitHub!")
            else:
                print("⚠️  Push failed. Try: git push -u origin main --force")
        else:
            print("\n📋 First, create a GitHub repository:")
            print("1. Go to https://github.com/new")
            print("2. Repository name: dsa-problem-tracker")
            print("3. Make it PUBLIC")
            print("4. Don't initialize with README")
            print("5. Copy the repository URL")
            print("\nPress Enter to open GitHub...")
            input()
            webbrowser.open("https://github.com/new")
            
            print("\nAfter creating the repo, run these commands:")
            print('git remote add origin YOUR_GITHUB_URL')
            print('git push -u origin main')
            print("\nThen re-run this script and choose option 1")
            return
        
        print("\n📝 Step 2: Deploy on Render")
        print("\n1. Open Render dashboard")
        print("2. Click 'New +' → 'Web Service'")
        print("3. Connect your GitHub repo")
        print("4. Use these settings:")
        print()
        print("   Build Command:")
        print("   pip install -r requirements.txt && python init_database.py && python init_auth.py")
        print()
        print("   Start Command:")
        print("   gunicorn app:app")
        print()
        print("Press Enter to open Render dashboard...")
        input()
        webbrowser.open("https://dashboard.render.com/")
        
    elif choice == "2":
        print_header("🐍 Deploying to PythonAnywhere")
        
        print("📚 Follow these steps:")
        print()
        print("1. Sign up: https://www.pythonanywhere.com/registration/register/beginner/")
        print("2. Open Bash console")
        print("3. Clone your repo:")
        print("   git clone YOUR_GITHUB_URL")
        print("   cd dsa-problem-tracker")
        print()
        print("4. Install dependencies:")
        print("   pip3.10 install --user -r requirements.txt")
        print("   python3.10 init_database.py")
        print("   python3.10 init_auth.py")
        print()
        print("5. Create Web App (see FREE_DEPLOY.md for WSGI config)")
        print()
        print("Press Enter to open PythonAnywhere...")
        input()
        webbrowser.open("https://www.pythonanywhere.com/registration/register/beginner/")
        
    elif choice == "3":
        print_header("📚 Opening Deployment Guide")
        if os.path.exists("FREE_DEPLOY.md"):
            webbrowser.open("FREE_DEPLOY.md")
            print("✅ Guide opened in your browser")
        else:
            print("❌ FREE_DEPLOY.md not found")
    else:
        print("❌ Invalid choice")
    
    print_header("✅ Next Steps")
    print("📖 Full guide: FREE_DEPLOY.md")
    print("🚀 Your app is ready to deploy!")
    print("💡 Both platforms are 100% FREE - no credit card needed!")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("Please check FREE_DEPLOY.md for manual deployment steps")
