# Movie Database

A Flask web application for browsing and filtering movies from various film movements and genres.

## Features
- Search movies by title, director, genre, or description
- Filter by genre, film movement, year range, and rating
- Sort movies by different criteria (title, year, ratings)
- Responsive grid layout
- Netflix-inspired design

## Setup
1. Clone the repository
bash
git clone https://github.com/yourusername/movie-database.git
cd movie-database

2. Create and activate virtual environment
```
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies
```
pip install flask
```

4. Set up the database
```
python database/setup_db.py
```

5. Run the application
```
python main.py
```

6. Open http://localhost:5000 in your browser

## Project Structure
- `main.py`: Flask application and route handlers
- `database/`: Database setup and movie data
- `templates/`: HTML templates
- `static/`: CSS and JavaScript files
