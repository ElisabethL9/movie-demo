from flask import Flask, render_template, request
import sqlite3
from pathlib import Path

app = Flask(__name__)

def get_db_connection():
    db_path = Path(__file__).parent / 'database' / 'movies.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    # Get year range from database first
    year_range = conn.execute('''
        SELECT MIN(year) as min_year, MAX(year) as max_year 
        FROM movies
    ''').fetchone()
    
    # Get filter and sort parameters
    search_query = request.args.get('search', '').strip()
    genre_filter = request.args.get('genre', 'all')
    movement_filter = request.args.get('movement', 'all')
    year_min = request.args.get('year_min', str(year_range['min_year']))
    year_max = request.args.get('year_max', str(year_range['max_year']))
    rating_min = request.args.get('rating_min', '0')
    sort_by = request.args.get('sort', 'imdb_rating')  # Default sort by IMDb rating
    sort_order = request.args.get('order', 'desc')  # Default order is descending

    # Define valid sort columns to prevent SQL injection
    valid_sort_columns = {
        'title': 'title',
        'year': 'year',
        'director': 'director',
        'imdb_rating': 'imdb_rating',
        'rotten_tomatoes_rating': 'rotten_tomatoes_rating'
    }

    # Use default if invalid sort column is provided
    sort_column = valid_sort_columns.get(sort_by, 'imdb_rating')
    order_direction = 'DESC' if sort_order.lower() == 'desc' else 'ASC'
    
    # Base query
    query = '''
        SELECT * FROM movies 
        WHERE year BETWEEN ? AND ?
        AND imdb_rating >= ?
    '''
    params = [year_min, year_max, rating_min]

    # Add genre filter
    if genre_filter != 'all':
        query += ' AND genre = ?'
        params.append(genre_filter)

    # Add movement filter
    if movement_filter != 'all':
        query += ' AND film_movement = ?'
        params.append(movement_filter)

    # Add search filter
    if search_query:
        query += ''' 
            AND (
                title LIKE ? 
                OR director LIKE ? 
                OR genre LIKE ?
                OR film_movement LIKE ?
                OR description LIKE ?
            )
        '''
        search_pattern = f'%{search_query}%'
        params.extend([search_pattern] * 5)

    # Add sorting
    query += f' ORDER BY {sort_column} {order_direction}'

    # Execute query
    movies = conn.execute(query, params).fetchall()

    # Get all genres and movements for filters
    genres = conn.execute('SELECT DISTINCT genre FROM movies ORDER BY genre').fetchall()
    movements = conn.execute('SELECT DISTINCT film_movement FROM movies ORDER BY film_movement').fetchall()
    
    conn.close()

    return render_template('index.html',
                         movies=movies,
                         genres=genres,
                         movements=movements,
                         year_range=year_range,
                         search_query=search_query,
                         genre_filter=genre_filter,
                         movement_filter=movement_filter,
                         year_min=year_min,
                         year_max=year_max,
                         rating_min=rating_min,
                         sort_by=sort_by,
                         sort_order=sort_order)

if __name__ == '__main__':
    app.run(debug=True)
