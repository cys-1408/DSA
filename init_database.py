#!/usr/bin/env python3
"""
Database Initialization Script
Extracts all problems from CSV files and stores them in SQLite database
"""

import os
import sys
import csv
import sqlite3
from pathlib import Path

def create_database():
    """Create the database schema"""
    conn = sqlite3.connect('dsa_problems.db')
    cursor = conn.cursor()
    
    # Create problems table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            duration TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            title TEXT NOT NULL,
            frequency REAL,
            acceptance_rate REAL,
            link TEXT NOT NULL,
            topics TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(company, duration, title)
        )
    ''')
    
    # Create indexes for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_company ON problems(company)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_duration ON problems(duration)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_difficulty ON problems(difficulty)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON problems(title)')
    
    conn.commit()
    return conn

def normalize_difficulty(difficulty):
    """Normalize difficulty values"""
    if not difficulty:
        return 'Unknown'
    difficulty = difficulty.strip().upper()
    if difficulty in ['EASY', 'E']:
        return 'Easy'
    elif difficulty in ['MEDIUM', 'M']:
        return 'Medium'
    elif difficulty in ['HARD', 'H']:
        return 'Hard'
    return difficulty.capitalize()

def parse_csv_file(filepath):
    """Parse a single CSV file and return list of problems"""
    problems = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read the CSV
            reader = csv.DictReader(f)
            
            for row in reader:
                # Extract and clean data
                difficulty = normalize_difficulty(row.get('Difficulty', ''))
                title = row.get('Title', '').strip()
                frequency = row.get('Frequency', '')
                acceptance_rate = row.get('Acceptance Rate', '')
                link = row.get('Link', '').strip()
                topics = row.get('Topics', '').strip()
                
                # Convert frequency to float
                try:
                    frequency = float(frequency) if frequency else None
                except ValueError:
                    frequency = None
                
                # Convert acceptance rate to float
                try:
                    acceptance_rate = float(acceptance_rate) if acceptance_rate else None
                except ValueError:
                    acceptance_rate = None
                
                if title and link:  # Only add if we have essential data
                    problems.append({
                        'difficulty': difficulty,
                        'title': title,
                        'frequency': frequency,
                        'acceptance_rate': acceptance_rate,
                        'link': link,
                        'topics': topics
                    })
    
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    
    return problems

def import_all_data(conn):
    """Import all CSV data into the database"""
    cursor = conn.cursor()
    data_path = Path('data')
    
    if not data_path.exists():
        print("Error: 'data' folder not found!")
        return 0
    
    durations = [
        '1. Thirty Days',
        '2. Three Months',
        '3. Six Months',
        '4. More Than Six Months',
        '5. All'
    ]
    
    total_imported = 0
    total_skipped = 0
    companies_processed = 0
    
    # Get all company folders
    companies = [d for d in data_path.iterdir() if d.is_dir()]
    companies.sort()
    
    print(f"\nFound {len(companies)} companies")
    print("=" * 70)
    
    for company_path in companies:
        company_name = company_path.name
        company_imported = 0
        
        for duration in durations:
            csv_file = company_path / f"{duration}.csv"
            
            if csv_file.exists():
                problems = parse_csv_file(csv_file)
                
                for problem in problems:
                    try:
                        cursor.execute('''
                            INSERT OR IGNORE INTO problems 
                            (company, duration, difficulty, title, frequency, acceptance_rate, link, topics)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            company_name,
                            duration,
                            problem['difficulty'],
                            problem['title'],
                            problem['frequency'],
                            problem['acceptance_rate'],
                            problem['link'],
                            problem['topics']
                        ))
                        
                        if cursor.rowcount > 0:
                            company_imported += 1
                            total_imported += 1
                        else:
                            total_skipped += 1
                    
                    except sqlite3.IntegrityError:
                        total_skipped += 1
        
        if company_imported > 0:
            companies_processed += 1
            print(f"✓ {company_name}: {company_imported} problems imported")
    
    conn.commit()
    
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"   Companies processed: {companies_processed}")
    print(f"   Total problems imported: {total_imported}")
    print(f"   Duplicates skipped: {total_skipped}")
    
    return total_imported

def get_database_stats(conn):
    """Display database statistics"""
    cursor = conn.cursor()
    
    print("\n" + "=" * 70)
    print("📈 Database Statistics")
    print("=" * 70)
    
    # Total problems
    cursor.execute('SELECT COUNT(*) FROM problems')
    total = cursor.fetchone()[0]
    print(f"Total problems: {total}")
    
    # Problems by difficulty
    cursor.execute('''
        SELECT difficulty, COUNT(*) 
        FROM problems 
        GROUP BY difficulty 
        ORDER BY COUNT(*) DESC
    ''')
    print("\nBy Difficulty:")
    for difficulty, count in cursor.fetchall():
        print(f"  {difficulty}: {count}")
    
    # Problems by company (top 10)
    cursor.execute('''
        SELECT company, COUNT(*) as cnt 
        FROM problems 
        GROUP BY company 
        ORDER BY cnt DESC 
        LIMIT 10
    ''')
    print("\nTop 10 Companies:")
    for company, count in cursor.fetchall():
        print(f"  {company}: {count}")
    
    # Total companies
    cursor.execute('SELECT COUNT(DISTINCT company) FROM problems')
    companies = cursor.fetchone()[0]
    print(f"\nTotal companies: {companies}")
    
    print("=" * 70)

def main():
    print("=" * 70)
    print("🚀 DSA Problems Database Initialization")
    print("=" * 70)
    
    # Check if database exists
    db_exists = os.path.exists('dsa_problems.db')
    if db_exists:
        # Check if running in interactive terminal
        if sys.stdin.isatty():
            # Interactive mode - ask user
            response = input("\n⚠️  Database already exists. Recreate? (y/N): ").strip().lower()
            if response == 'y':
                os.remove('dsa_problems.db')
                print("✓ Old database removed")
            else:
                print("✓ Using existing database")
                return  # Exit if not recreating
        else:
            # Non-interactive mode (CI/CD, Render, etc.) - use existing database
            print("\n✓ Database already exists, using existing database")
            print("   (Running in non-interactive mode)")
            return  # Exit without recreating
    
    # Create database and schema
    print("\n📦 Creating database schema...")
    conn = create_database()
    print("✓ Database schema created")
    
    # Import data
    print("\n📥 Importing data from CSV files...")
    imported = import_all_data(conn)
    
    if imported > 0:
        # Show statistics
        get_database_stats(conn)
        print("\n✅ Database initialized successfully!")
        print("🎉 You can now run the server with: python server.py")
    else:
        print("\n❌ No data was imported. Please check your CSV files.")
    
    conn.close()

if __name__ == '__main__':
    main()
