# 🎯 DSA Problem Tracker - Premium Edition (Database-Backed)

A beautiful, feature-rich web application to track your DSA (Data Structures & Algorithms) problem-solving progress across top tech companies. Now with **SQLite database backend** for lightning-fast performance and **intuitive two-page interface**!

## ✨ Features

### 🏢 Company Selection Page
- **Grid View**: All 469 companies displayed in a beautiful card grid
- **Smart Search**: Instantly filter companies by name
- **Statistics Dashboard**: See total companies, problems, and averages
- **Problem Counts**: Each company card shows total problems available

### 📚 Problems Viewer Page
- **Company-Specific View**: Focus on one company at a time
- **Advanced Filters**: Filter by Duration, Difficulty, Status, and Search
- **Progress Tracking**: Visual progress bar and detailed statistics
- **Status Management**: Mark problems as Solved ✓, Tried ~, or Not Started ✗
- **Direct Links**: One-click button to problem pages
- **Export Progress**: Backup your progress for each company
- **Real-time Stats**: See solved, tried, and unsolved counts

### ⏰ Time-Based Filters
- Thirty Days
- Three Months
- Six Months
- More Than Six Months
- All Time

### 💾 Smart Storage
- **Local Storage**: Your progress auto-saves per company
- **Export/Import**: Backup and restore progress anytime
- **Database Backend**: Lightning-fast data retrieval

## 🚀 Quick Start

### Prerequisites

- Python 3.x (already installed on most systems)
- A modern web browser (Chrome, Firefox, Edge, Safari)

### Initial Setup (First Time Only)

1. **Navigate to the project directory**:
   ```powershell
   cd "c:\Users\C. Tinesh Karthick\Music\Project\DSA"
   ```

2. **Initialize the database** (extracts all CSV data into SQLite):
   ```powershell
   python init_database.py
   ```
   
   This will:
   - Create `dsa_problems.db`
   - Extract all problems from CSV files
   - Show statistics about imported data
   - Takes ~30-60 seconds depending on your data size

### Running the Application

1. **Start the server**:
   ```powershell
   python server.py
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```

3. **Start tracking!** 🎉

### Stopping the Server

Press `Ctrl+C` in the terminal to stop the server.

## 📖 How to Use

### Step 1: Select a Company
1. Open `http://localhost:8000` in your browser
2. Browse the grid of 469 companies
3. Use the search bar to find specific companies
4. Click on any company card to view their problems

### Step 2: Work on Problems
1. You'll see all problems for that company
2. Use filters to refine your view:
   - **Duration**: Focus on recent or frequent problems
   - **Difficulty**: Start with Easy, progress to Hard
   - **Status**: Filter by Solved/Tried/Not Started
   - **Search**: Find specific problem titles

### Step 3: Track Your Progress
For each problem, you can:
- **✓ Mark as Solved**: You've completed it successfully
- **~ Mark as Tried**: You've attempted but not finished
- **✗ Mark as Not Started**: Haven't attempted yet

Your progress is automatically saved per company!

### Statistics Dashboard
- **Total Problems**: All problems for this company
- **Solved**: Problems you've marked as solved
- **Tried**: Problems you've attempted
- **Not Started**: Problems waiting for you
- **Progress Bar**: Visual percentage of completion

### Backup & Restore

- **Export Progress**: Download your progress as a JSON file
- **Import Progress**: Restore progress from a previously exported file

## 📁 Data Structure

The application expects the following folder structure:

```
data/
├── Company Name 1/
│   ├── 1. Thirty Days.csv
│   ├── 2. Three Months.csv
│   ├── 3. Six Months.csv
│   ├── 4. More Than Six Months.csv
│   └── 5. All.csv
├── Company Name 2/
│   └── ...
└── ...
```

### CSV Format

Each CSV file should have these columns:
- **Difficulty**: Easy, Medium, or Hard
- **Title**: Problem title
- **Frequency**: How often the problem appears
- **Acceptance Rate**: Success rate percentage
- **Link**: URL to the problem

## 🎨 Features Showcase

### Premium UI
- Modern dark theme with gradient effects
- Smooth animations and transitions
- Responsive design for all screen sizes
- Hover effects and visual feedback

### Smart Filtering
- Combine multiple filters
- Real-time search
- Filter by problem status
- Easy reset functionality

### Progress Tracking
- Visual progress bar
- Detailed statistics
- Persistent storage
- Export/import capabilities

## 🔧 Troubleshooting

### Database Not Found Error

If you see "Database not found", run:
```powershell
python init_database.py
```

### Updating Data

If you add new CSV files or update existing ones:
```powershell
python init_database.py
```
Choose 'y' when asked to recreate the database.

### Port Already in Use

If port 8000 is busy, you can modify `server.py` and change the port:
```python
run_server(port=8080)  # Use a different port
```

### No Problems Showing

Make sure:
1. Database is initialized: `python init_database.py`
2. Check browser console for errors (F12 → Console tab)
3. Try clearing browser cache and reload

### Progress Not Saving

- Ensure your browser allows localStorage
- Check browser console for errors (F12 → Console tab)
- Try clearing browser cache and reload

## 📁 Database Schema

The SQLite database (`dsa_problems.db`) contains:

**Problems Table:**
- `id`: Primary key
- `company`: Company name
- `duration`: Time period
- `difficulty`: Easy, Medium, or Hard
- `title`: Problem title
- `frequency`: How often the problem appears
- `acceptance_rate`: Success rate (0.0 to 1.0)
- `link`: URL to the problem
- `topics`: Problem topics/tags
- `created_at`: Import timestamp

**Indexes** for fast queries on: company, duration, difficulty, title

## 🌟 Tips

1. **Regular Backups**: Export your progress regularly using the Export button
2. **Focused Practice**: Use duration filters to focus on frequently asked questions
3. **Company Targeting**: Prepare for specific companies using the company filter
4. **Difficulty Progression**: Start with Easy, move to Medium, then tackle Hard problems
5. **Track Everything**: Even mark problems you've tried but not solved - it helps track your journey!

## 📊 Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python HTTP Server with SQLite
- **Database**: SQLite3 (serverless, no configuration needed)
- **Storage**: Browser localStorage for progress tracking
- **Design**: Custom CSS with modern design principles

## 🎯 Architecture

Browser
   ↓
┌─────────────────────────┐
│   index.html            │  ← Company selection grid
│   (Landing Page)         │     469 companies displayed
└────────┬────────────────┘
         │ Click company
┌────────▼────────────────┐
│   problems.html         │  ← Problems viewer
│   (Company Problems)    │     Filters, tracking, stats
└────────┬────────────────┘
         │ API Calls
┌────────▼────────────────┐
│   Python Server         │  ← HTTP + SQLite
│   (server.py)           │     /api/companies
└────────┬────────────────┘     /api/problems
         │                      /api/stats
┌────────▼────────────────┐
│   SQLite Database       │  ← 18,668 problems
│   (dsa_problems.db)     │     469 companies
└─────────────────────────┘     Fast queries
```

**Benefits:**
- ⚡ **Lightning Fast**: Database queries in milliseconds
- 🎯 **Focused UX**: One company at a time, no overwhelming lists
- 💾 **Efficient Storage**: Progress saved per company
- 🔍 **Better Filtering**: Database indexes for instant results
- 📊 **Smart Stats**: Real-time progress tracking per compan
- 📈 **Scalable**: Can handle thousands of problems efficiently

## 📝 License

This project is open source and available for personal use.

## 🤝 Contributing

Feel free to enhance the application with new features or improvements!

---

**Made with ❤️ for DSA enthusiasts**

Happy Coding! 🚀
