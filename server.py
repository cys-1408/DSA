#!/usr/bin/env python3
"""
DSA Problem Tracker - Local Server
Serves the web application and provides database-backed API endpoints
"""

import os
import json
import sqlite3
import traceback
import hashlib
import secrets
from datetime import datetime, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class DSAServerHandler(SimpleHTTPRequestHandler):
    def get_db_connection(self):
        """Get database connection"""
        db_path = os.path.join(os.getcwd(), 'dsa_problems.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def send_json_response(self, data):
        """Helper to send JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_json_error(self, code, message):
        """Helper to send JSON error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'error': message}).encode('utf-8'))
    
    def hash_password(self, password, salt=None):
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return pwd_hash.hex(), salt
    
    def verify_session(self, token):
        """Verify session token and return user_id"""
        if not token:
            return None
        
        try:
            conn = self.get_db_connection()
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
    
    def read_post_data(self):
        """Read and parse POST data"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))
    
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # API: Get all companies
        if path == '/api/companies':
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT DISTINCT company FROM problems ORDER BY company')
                companies = [row['company'] for row in cursor.fetchall()]
                conn.close()
                
                self.send_json_response(companies)
            except Exception as e:
                print(f"Error in /api/companies: {e}")
                traceback.print_exc()
                self.send_error(500, f"Database error: {str(e)}")
            return
        
        # API: Get all problems with filters
        elif path == '/api/problems':
            try:
                params = parse_qs(parsed_url.query)
                
                conn = self.get_db_connection()
                cursor = conn.cursor()
                
                # Build query with filters
                query = 'SELECT * FROM problems WHERE 1=1'
                query_params = []
                
                if 'company' in params and params['company'][0] != 'all':
                    query += ' AND company = ?'
                    query_params.append(params['company'][0])
                
                if 'duration' in params and params['duration'][0] != '5. All':
                    query += ' AND duration = ?'
                    query_params.append(params['duration'][0])
                
                if 'difficulty' in params and params['difficulty'][0] != 'all':
                    query += ' AND difficulty = ?'
                    query_params.append(params['difficulty'][0])
                
                if 'search' in params and params['search'][0]:
                    query += ' AND title LIKE ?'
                    query_params.append(f"%{params['search'][0]}%")
                
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
                
                self.send_json_response(problems)
            except Exception as e:
                print(f"Error in /api/problems: {e}")
                traceback.print_exc()
                self.send_error(500, f"Database error: {str(e)}")
            return
        
        # API: Get statistics
        elif path == '/api/stats':
            try:
                conn = self.get_db_connection()
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
                
                self.send_json_response(stats)
            except Exception as e:
                print(f"Error in /api/stats: {e}")
                traceback.print_exc()
                self.send_error(500, f"Database error: {str(e)}")
            return
        
        # API: Check session validity
        elif path == '/api/check-session':
            token = self.headers.get('Authorization', '').replace('Bearer ', '')
            user_id = self.verify_session(token)
            if user_id:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
                user = cursor.fetchone()
                conn.close()
                self.send_json_response({'valid': True, 'username': user['username']})
            else:
                self.send_json_response({'valid': False})
            return
        
        # Serve static files
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # API: User registration
        if path == '/api/register':
            try:
                data = self.read_post_data()
                username = data.get('username', '').strip()
                email = data.get('email', '').strip()
                password = data.get('password', '')
                
                # Validation
                if not username or len(username) < 3:
                    self.send_json_error(400, 'Username must be at least 3 characters')
                    return
                
                if not email or '@' not in email:
                    self.send_json_error(400, 'Invalid email address')
                    return
                
                if not password or len(password) < 6:
                    self.send_json_error(400, 'Password must be at least 6 characters')
                    return
                
                # Hash password
                pwd_hash, salt = self.hash_password(password)
                
                # Insert user
                conn = self.get_db_connection()
                cursor = conn.cursor()
                
                try:
                    cursor.execute('''
                        INSERT INTO users (username, email, password_hash, salt)
                        VALUES (?, ?, ?, ?)
                    ''', (username, email, pwd_hash, salt))
                    conn.commit()
                    conn.close()
                    
                    self.send_json_response({'success': True, 'message': 'Registration successful'})
                except sqlite3.IntegrityError:
                    conn.close()
                    self.send_json_error(400, 'Username or email already exists')
                    
            except Exception as e:
                print(f"Error in /api/register: {e}")
                traceback.print_exc()
                self.send_json_error(500, f"Registration error: {str(e)}")
            return
        
        # API: User login
        elif path == '/api/login':
            try:
                data = self.read_post_data()
                username = data.get('username', '').strip()
                password = data.get('password', '')
                
                if not username or not password:
                    self.send_json_error(400, 'Username and password are required')
                    return
                
                # Get user
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT id, password_hash, salt FROM users WHERE username = ?', (username,))
                user = cursor.fetchone()
                
                if not user:
                    conn.close()
                    self.send_json_error(401, 'Invalid username or password')
                    return
                
                # Verify password
                pwd_hash, _ = self.hash_password(password, user['salt'])
                if pwd_hash != user['password_hash']:
                    conn.close()
                    self.send_json_error(401, 'Invalid username or password')
                    return
                
                # Create session
                token = secrets.token_urlsafe(32)
                expires_at = datetime.now() + timedelta(days=7)
                
                cursor.execute('''
                    INSERT INTO sessions (user_id, token, expires_at)
                    VALUES (?, ?, ?)
                ''', (user['id'], token, expires_at))
                conn.commit()
                conn.close()
                
                self.send_json_response({
                    'success': True,
                    'token': token,
                    'username': username
                })
                
            except Exception as e:
                print(f"Error in /api/login: {e}")
                traceback.print_exc()
                self.send_json_error(500, f"Login error: {str(e)}")
            return
        
        # Method not allowed for other POST requests
        self.send_error(405, "Method Not Allowed")
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

def run_server(port=8000):
    # Check if database exists
    db_path = os.path.join(os.getcwd(), 'dsa_problems.db')
    if not os.path.exists(db_path):
        print("=" * 70)
        print("❌ Database not found!")
        print("=" * 70)
        print(f"Looking for: {db_path}")
        print("Please run the database initialization script first:")
        print("  python init_database.py")
        print("=" * 70)
        return
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, DSAServerHandler)
    
    print("=" * 70)
    print("🚀 DSA Problem Tracker Server (Database Mode)")
    print("=" * 70)
    print(f"✅ Server running at: http://localhost:{port}")
    print(f"📂 Serving from: {os.getcwd()}")
    print(f"💾 Using database: dsa_problems.db")
    print(f"🌐 Open http://localhost:{port} in your browser")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 70)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        httpd.shutdown()

if __name__ == '__main__':
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
    run_server()
