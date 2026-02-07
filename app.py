#!/usr/bin/env python3
"""
DSA Problem Tracker - Production Server
Flask-based server for deployment
"""

import os
import json
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path

app = Flask(__name__, static_folder='.')

# Database configuration
DB_PATH = os.path.join(os.getcwd(), 'dsa_problems.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password, salt=None):
    """Hash password with salt"""
    if salt is None:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return pwd_hash.hex(), salt

def verify_session(token):
    """Verify session token and return user_id"""
    if not token:
        return None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_id FROM sessions 
            WHERE token = ? AND expires_at > datetime('now')
        ''', (token,))
        result = cursor.fetchone()
        conn.close()
        return result['user_id'] if result else None
    except Exception as e:
        print(f"Session verification error: {e}")
        return None

# Static file serving
@app.route('/')
def index():
    return send_from_directory('.', 'login.html')

@app.route('/<path:path>')
def serve_static(path):
    if path and os.path.exists(path):
        return send_from_directory('.', path)
    return send_from_directory('.', 'login.html')

# API: Get all companies
@app.route('/api/companies', methods=['GET'])
def get_companies():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT company FROM problems ORDER BY company')
        companies = [row['company'] for row in cursor.fetchall()]
        conn.close()
        return jsonify(companies)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API: Get all problems with filters
@app.route('/api/problems', methods=['GET'])
def get_problems():
    try:
        company = request.args.get('company', 'all')
        duration = request.args.get('duration', '5. All')
        difficulty = request.args.get('difficulty', 'all')
        search = request.args.get('search', '')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build query with filters
        query = 'SELECT * FROM problems WHERE 1=1'
        query_params = []
        
        if company != 'all':
            query += ' AND company = ?'
            query_params.append(company)
        
        if duration != '5. All':
            query += ' AND duration = ?'
            query_params.append(duration)
        
        if difficulty != 'all':
            query += ' AND difficulty = ?'
            query_params.append(difficulty)
        
        if search:
            query += ' AND title LIKE ?'
            query_params.append(f"%{search}%")
        
        query += ' ORDER BY company, difficulty, title'
        
        cursor.execute(query, query_params)
        
        # Convert rows to dictionaries
        problems = []
        for row in cursor.fetchall():
            problems.append({
                'id': row['id'],
                'company': row['company'],
                'duration': row['duration'],
                'difficulty': row['difficulty'],
                'title': row['title'],
                'frequency': row['frequency'],
                'acceptance_rate': row['acceptance_rate'],
                'link': row['link'],
                'topics': row['topics']
            })
        
        conn.close()
        return jsonify(problems)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API: Get statistics
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total problems
        cursor.execute('SELECT COUNT(*) as count FROM problems')
        stats['total'] = cursor.fetchone()['count']
        
        # By difficulty
        cursor.execute('''
            SELECT difficulty, COUNT(*) as count 
            FROM problems 
            GROUP BY difficulty
        ''')
        stats['by_difficulty'] = {row['difficulty']: row['count'] for row in cursor.fetchall()}
        
        # By company
        cursor.execute('''
            SELECT company, COUNT(*) as count 
            FROM problems 
            GROUP BY company
            ORDER BY count DESC
        ''')
        stats['by_company'] = {row['company']: row['count'] for row in cursor.fetchall()}
        
        # Total companies
        cursor.execute('SELECT COUNT(DISTINCT company) as count FROM problems')
        stats['total_companies'] = cursor.fetchone()['count']
        
        conn.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API: Check session validity
@app.route('/api/check-session', methods=['GET'])
def check_session():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_id = verify_session(token)
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return jsonify({'valid': True, 'username': user['username']})
    return jsonify({'valid': False})

# API: User registration
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validation
        if not username or len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        if not email or '@' not in email:
            return jsonify({'error': 'Invalid email address'}), 400
        
        if not password or len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Hash password
        pwd_hash, salt = hash_password(password)
        
        # Insert user
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, salt)
                VALUES (?, ?, ?, ?)
            ''', (username, email, pwd_hash, salt))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Registration successful'})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'Username or email already exists'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API: User login
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Get user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash, salt FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Verify password
        pwd_hash, _ = hash_password(password, user['salt'])
        if pwd_hash != user['password_hash']:
            conn.close()
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Create session
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=7)
        
        cursor.execute('''
            INSERT INTO sessions (user_id, token, expires_at)
            VALUES (?, ?, ?)
        ''', (user['id'], token, expires_at))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'token': token,
            'username': username
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize database on startup
@app.before_request
def initialize_database():
    """Initialize database if needed"""
    if not os.path.exists(DB_PATH):
        print("⚠️ Database not found. Please run init_database.py and init_auth.py first.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
