import sqlite3
from pathlib import Path

# Create database directory if it doesn't exist
db_dir = Path(__file__).parent
db_dir.mkdir(exist_ok=True)

# Connect to database
conn = sqlite3.connect(db_dir / 'movies.db')
cursor = conn.cursor()

# Drop existing table to update schema
cursor.execute('DROP TABLE IF EXISTS movies')

# Create movies table with additional rating
cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    film_movement TEXT,
    year INTEGER,
    director TEXT,
    imdb_rating FLOAT,
    rotten_tomatoes_rating INTEGER,
    image_url TEXT,
    description TEXT
)
''')

# Combine all movie data into one large list
all_movies = [
    # Original movies list
    ('The Godfather', 'Crime', 'New Hollywood', 1972, 'Francis Ford Coppola', 9.2, 98, 
     'https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
     'An organized crime dynasty\'s aging patriarch transfers control to his son.'),
    ('Pulp Fiction', 'Crime', 'Independent Film', 1994, 'Quentin Tarantino', 8.9, 92,
     'https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
     'Various interconnected stories of criminals in Los Angeles.'),
    ('Goodfellas', 'Crime', 'New Hollywood', 1990, 'Martin Scorsese', 8.7, 96,
     'https://m.media-amazon.com/images/M/MV5BY2NkZjEzMDgtN2RjYy00YzM1LWI4ZmQtMjIwYjFjNmI3ZGEwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
     'The story of Henry Hill and his life in the mob.'),
    ('The Departed', 'Crime', 'Contemporary', 2006, 'Martin Scorsese', 8.5, 90,
     'https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p162564_p_v8_ag.jpg',
     'An undercover cop and a mole in the police attempt to identify each other.'),
    ('Heat', 'Crime', 'Contemporary', 1995, 'Michael Mann', 8.3, 87,
     'https://m.media-amazon.com/images/M/MV5BYjZjNTJlZGUtZTE1Ny00ZDc4LTgwYjUtMzk0NDgwYzZjYTk1XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
     'A group of professional bank robbers start to feel the heat from police.'),
    ('Casino', 'Crime', 'Contemporary', 1995, 'Martin Scorsese', 8.2, 80,
     'https://m.media-amazon.com/images/M/MV5BMTcxOWYzNDYtYmM4YS00N2NkLTk0NTAtNjg1ODgwZjAxYzI3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_.jpg',
     'A tale of greed, deception, money, power, and murder occur between two best friends.'),
    
    # Action Movies
    ('Seven Samurai', 'Action', 'Japanese New Wave', 1954, 'Akira Kurosawa', 8.6, 100,
     'https://m.media-amazon.com/images/M/MV5BZDg4MTYyYjktZGJiYy00ZGIwLWEzNTMtNTZkMjRhYTViMWE4XkEyXkFqcGc@._V1_.jpg',
     'Farmers hire seven samurai to combat bandits threatening their crops.'),
    ('Die Hard', 'Action', 'Modern Action', 1988, 'John McTiernan', 8.2, 94,
     'https://m.media-amazon.com/images/M/MV5BZjRlNDUxZjAtOGQ4OC00OTNlLTgxNmQtYTBmMDgwZmNmNjkxXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
     'An NYPD officer tries to save his wife and others taken hostage during a Christmas party.'),
    ('Mad Max: Fury Road', 'Action', 'Contemporary', 2015, 'George Miller', 8.1, 97,
     'https://m.media-amazon.com/images/M/MV5BN2EwM2I5OWMtMGQyMi00Zjg1LWJkNTctZTdjYTA4OGUwZjMyXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
     'In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler.'),
    ('The Dark Knight', 'Action', 'Contemporary', 2008, 'Christopher Nolan', 9.0, 94,
     'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg',
     'Batman raises the stakes in his war on crime.'),
    ('Inception', 'Action', 'Contemporary', 2010, 'Christopher Nolan', 8.8, 87,
     'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg',
     'A thief who steals corporate secrets through dream-sharing technology.'),
    
    # Drama Movies
    ('The Shawshank Redemption', 'Drama', 'Contemporary', 1994, 'Frank Darabont', 9.3, 91,
     'https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg',
     'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.'),
    ('12 Angry Men', 'Drama', 'Golden Age', 1957, 'Sidney Lumet', 9.0, 100,
     'https://m.media-amazon.com/images/M/MV5BMWU4N2FjNzYtNTVkNC00NzQ0LTg0MjAtYTJlMjFhNGUxZDFmXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_.jpg',
     'A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence.'),
    ('Forrest Gump', 'Drama', 'Contemporary', 1994, 'Robert Zemeckis', 8.8, 71,
     'https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg',
     'The presidencies, Vietnam, and other historical events unfold through the perspective of an Alabama man.'),
    ('The Green Mile', 'Drama', 'Contemporary', 1999, 'Frank Darabont', 8.6, 79,
     'https://m.media-amazon.com/images/M/MV5BMTUxMzQyNjA5MF5BMl5BanBnXkFtZTYwOTU2NTY3._V1_.jpg',
     'The lives of guards on Death Row are affected by one of their charges.'),
    
    # Sci-Fi Movies
    ('Blade Runner', 'Sci-Fi', 'New Hollywood', 1982, 'Ridley Scott', 8.1, 89,
     'https://m.media-amazon.com/images/M/MV5BNzQzMzJhZTEtOWM4NS00MTdhLTg0YjgtMjM4MDRkZjUwZDBlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
     'A blade runner must pursue and terminate four replicants who stole a ship in space.'),
    ('2001: A Space Odyssey', 'Sci-Fi', 'New Hollywood', 1968, 'Stanley Kubrick', 8.3, 92,
     'https://m.media-amazon.com/images/M/MV5BMmNlYzRiNDctZWNhMi00MzI4LThkZTctMTUzMmZkMmFmNThmXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
     'A space-opera spanning the dawn of man to humanity reaching the stars.'),
    ('The Matrix', 'Sci-Fi', 'Contemporary', 1999, 'Lana and Lilly Wachowski', 8.7, 88,
     'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
     'A computer programmer discovers that reality as he knows it is a simulation.'),
    ('Interstellar', 'Sci-Fi', 'Contemporary', 2014, 'Christopher Nolan', 8.6, 72,
     'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
     'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.'),
    
    # Horror Movies
    ('The Shining', 'Horror', 'Contemporary', 1980, 'Stanley Kubrick', 8.4, 85,
     'https://m.media-amazon.com/images/M/MV5BZWFlYmY2MGEtZjVkYS00YzU4LTg0YjQtYzY1ZGE3NTA5NGQxXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg',
     'A family heads to an isolated hotel for the winter where an evil presence influences the father.'),
    ('Alien', 'Horror', 'New Hollywood', 1979, 'Ridley Scott', 8.5, 98,
     'https://static.wikia.nocookie.net/alienanthology/images/e/e2/Alien_-_HD_poster.jpg',
     'The crew of a commercial spacecraft encounter a deadly alien.'),

    # More Crime Movies
    ('Once Upon a Time in America', 'Crime', 'New Hollywood', 1984, 'Sergio Leone', 8.3, 87,
     'https://m.media-amazon.com/images/M/MV5BMGFkNWI4MTMtNGQ0OC00MWVmLTk3MTktOGYxN2Y2YWVkZWE2XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
     'A former Prohibition-era Jewish gangster returns to the Lower East Side of Manhattan.'),
    ('L.A. Confidential', 'Crime', 'Neo-Noir', 1997, 'Curtis Hanson', 8.2, 99,
     'https://m.media-amazon.com/images/M/MV5BMDQ2YzEyZGItYWRhOS00MjBmLTkzMDUtMTdjYzkyMmQxZTJlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
     'As corruption grows in 1950s Los Angeles, three policemen investigate a series of murders.'),

    # More Action Movies
    ('Gladiator', 'Action', 'Contemporary', 2000, 'Ridley Scott', 8.5, 77,
     'https://m.media-amazon.com/images/M/MV5BMDliMmNhNDEtODUyOS00MjNlLTgxODEtN2U3NzIxMGVkZTA1L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
     'A former Roman General seeks revenge against the corrupt emperor who murdered his family.'),
    ('Raiders of the Lost Ark', 'Action', 'New Hollywood', 1981, 'Steven Spielberg', 8.4, 95,
     'https://m.media-amazon.com/images/M/MV5BMjA0ODEzMTc1Nl5BMl5BanBnXkFtZTcwODM2MjAxNA@@._V1_.jpg',
     'Archaeologist Indiana Jones races against time to retrieve the lost Ark of the Covenant.'),

    # More Drama Movies
    ('Schindler\'s List', 'Drama', 'Contemporary', 1993, 'Steven Spielberg', 9.0, 98,
     'https://m.media-amazon.com/images/M/MV5BNDE4OTMxMTctNmRhYy00NWE2LTg3YzItYTk3M2UwOTU5Njg4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
     'A businessman saves the lives of over a thousand Jewish refugees during the Holocaust.'),
    ('The Godfather: Part II', 'Drama', 'New Hollywood', 1974, 'Francis Ford Coppola', 9.0, 96,
     'https://m.media-amazon.com/images/M/MV5BMWMwMGQzZTItY2JlNC00OWZiLWIyMDctNDk2ZDQ2YjRjMWQ0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
     'The early life and career of Vito Corleone in 1920s New York City.'),

    # More Sci-Fi Movies
    ('Arrival', 'Sci-Fi', 'Contemporary', 2016, 'Denis Villeneuve', 7.9, 94,
     'https://m.media-amazon.com/images/M/MV5BMTExMzU0ODcxNDheQTJeQWpwZ15BbWU4MDE1OTI4MzAy._V1_.jpg',
     'A linguist works with the military to communicate with alien lifeforms.'),
    ('Children of Men', 'Sci-Fi', 'Contemporary', 2006, 'Alfonso Cuarón', 7.9, 92,
     'https://m.media-amazon.com/images/M/MV5BMTQ5NTI2NTI4NF5BMl5BanBnXkFtZTcwNjk2NDA2OQ@@._V1_.jpg',
     'In a future where humanity has become infertile, a former activist agrees to help transport a miraculously pregnant woman.'),

    # More Horror Movies
    ('The Thing', 'Horror', 'Contemporary', 1982, 'John Carpenter', 8.2, 84,
     'https://m.media-amazon.com/images/M/MV5BNGViZWZmM2EtNGYzZi00ZDAyLTk3ODMtNzIyZTBjN2Y1NmM1XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_.jpg',
     'A research team in Antarctica is hunted by a shape-shifting alien.'),
    ('Get Out', 'Horror', 'Contemporary', 2017, 'Jordan Peele', 7.8, 98,
     'https://m.media-amazon.com/images/M/MV5BMjUxMDQwNjcyNl5BMl5BanBnXkFtZTgwNzcwMzc0MTI@._V1_.jpg',
     'A young African-American visits his white girlfriend\'s parents for the weekend.'),

    # Western Movies (New Genre)
    ('The Good, the Bad and the Ugly', 'Western', 'Spaghetti Western', 1966, 'Sergio Leone', 8.8, 97,
     'https://m.media-amazon.com/images/M/MV5BNjJlYmNkZGItM2NhYy00MjlmLTk5NmQtNjg1NmM2ODU4OTMwXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_.jpg',
     'Three gunslingers compete to find a fortune in buried Confederate gold.'),
    ('Unforgiven', 'Western', 'Contemporary', 1992, 'Clint Eastwood', 8.2, 96,
     'https://m.media-amazon.com/images/M/MV5BODM3YWY4NmQtN2Y3Ni00OTg0LWFhZGQtZWE3ZWY4MTJlOWU4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
     'Retired Old West gunslinger William Munny reluctantly takes on one last job.'),

    # French New Wave (Nouvelle Vague)
    ('The 400 Blows', 'Drama', 'French New Wave', 1959, 'François Truffaut', 8.1, 99,
     'https://m.media-amazon.com/images/M/MV5BYTQ4MjA4NmYtYjRhNi00MTEwLTg0NjgtNjk3ODJlZGU4NjRkL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
     'A young boy, neglected by his parents, turns to petty crime.'),
    ('Breathless', 'Crime', 'French New Wave', 1960, 'Jean-Luc Godard', 7.8, 97,
     'https://images.squarespace-cdn.com/content/v1/5a7dcf69d7bdce185884a6b5/1543981224090-MZKDEARXPXXMMC62YMTQ/image-asset.jpeg',
     'A small-time thief steals a car and murders a policeman.'),
    ('Cléo from 5 to 7', 'Drama', 'French New Wave', 1962, 'Agnès Varda', 8.0, 97,
     'https://assets.mubicdn.net/images/notebook/post_images/22635/images-w1400.jpg',
     'A singer wanders around Paris while awaiting results of a biopsy test.'),

    # Italian Neorealism
    ('Bicycle Thieves', 'Drama', 'Italian Neorealism', 1948, 'Vittorio De Sica', 8.3, 99,
     'https://m.media-amazon.com/images/M/MV5BNmI1ODdjODctMDlmMC00ZWViLWI5MzYtYzRhNDdjYmM3MzFjXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
     'A man and his son search for a stolen bicycle vital for his job.'),
    ('Rome, Open City', 'Drama', 'Italian Neorealism', 1945, 'Roberto Rossellini', 8.1, 98,
     'https://m.media-amazon.com/images/M/MV5BZWU1NzJlYjAtZWJlMi00NzdkLWJmMjktYTY2M2E0NGQyNjEwXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg',
     'During Nazi occupation of Rome, a resistance leader seeks help from the Church.'),
    ('La Strada', 'Drama', 'Italian Neorealism', 1954, 'Federico Fellini', 8.0, 97,
     'https://m.media-amazon.com/images/M/MV5BMWQ0M2Q5NDAtMDg0ZC00YmM1LWI3YjktNDIxOTFiOTIzYzQ2XkEyXkFqcGc@._V1_.jpg',
     'A traveling strongman buys a simple-minded woman to assist his act.'),

    # German Expressionism & New German Cinema
    ('Metropolis', 'Sci-Fi', 'German Expressionism', 1927, 'Fritz Lang', 8.3, 97,
     'https://m.media-amazon.com/images/M/MV5BMTg5YWIyMWUtZDY5My00Zjc1LTljOTctYmI0MWRmY2M2NmRkXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
     'In a futuristic city, a worker mediates between the planners and the workers.'),
    ('The Cabinet of Dr. Caligari', 'Horror', 'German Expressionism', 1920, 'Robert Wiene', 8.0, 99,
     'https://m.media-amazon.com/images/M/MV5BNWJiNGJiMTEtMGM3OC00ZWNlLTgwZTgtMzdhNTRiZjk5MTQ1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
     'Hypnotist Dr. Caligari uses a somnambulist to commit murders.'),
    ('Wings of Desire', 'Fantasy', 'New German Cinema', 1987, 'Wim Wenders', 8.0, 98,
     'https://m.media-amazon.com/images/M/MV5BMTkwNmIxN2UtM2E4YS00MTYyLTgxZDYtZGMyMDU1ODZmYmRmXkEyXkFqcGc@._V1_.jpg',
     'An angel falls in love with a mortal in Berlin.'),

    # Japanese New Wave
    ('Woman in the Dunes', 'Drama', 'Japanese New Wave', 1964, 'Hiroshi Teshigahara', 8.4, 100,
     'https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p7490_p_v8_aa.jpg',
     'An entomologist is trapped with a widow in a sand quarry.'),
    ('Harakiri', 'Drama', 'Japanese New Wave', 1962, 'Masaki Kobayashi', 8.6, 100,
     'https://m.media-amazon.com/images/M/MV5BYjBmYTQ1NjItZWU5MS00YjI0LTg2OTYtYmFkN2JkMmNiNWVkXkEyXkFqcGdeQXVyMTMxMTY0OTQ@._V1_.jpg',
     'A samurai requests to commit ritual suicide at a feudal lord\'s palace.'),
    ('Tokyo Story', 'Drama', 'Japanese Cinema', 1953, 'Yasujirō Ozu', 8.7, 100,
     'https://m.media-amazon.com/images/M/MV5BYWQ4ZTRiODktNjAzZC00Nzg1LTk1YWQtNDFmNDI0NmZiNGIwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
     'An elderly couple visits their children in Tokyo, but are received coldly.'),

    # Soviet Cinema
    ('Stalker', 'Sci-Fi', 'Soviet Cinema', 1979, 'Andrei Tarkovsky', 8.2, 100,
     'https://m.media-amazon.com/images/M/MV5BMDIzMDRiYjgtM2U1Yy00MjlhLTliODMtM2E5NDI5Njc3YmZkXkEyXkFqcGc@._V1_.jpg',
     'A guide leads two men through an area known as the Zone to find a room that grants wishes.'),
    ('Battleship Potemkin', 'Drama', 'Soviet Montage', 1925, 'Sergei Eisenstein', 8.0, 100,
     'https://m.media-amazon.com/images/M/MV5BMTEyMTQzMjQ0MTJeQTJeQWpwZ15BbWU4MDcyMjg4OTEx._V1_.jpg',
     'A dramatized version of a famous 1905 mutiny in the Black Sea.'),

    # Czech New Wave
    ('Closely Watched Trains', 'Comedy', 'Czech New Wave', 1966, 'Jiří Menzel', 7.9, 100,
     'https://goldenglobes.com/wp-content/uploads/2023/10/closely_watched_trains_czechoslovakia.jpg',
     'A young man works as a train dispatcher during the Nazi occupation.'),
    ('Daisies', 'Comedy', 'Czech New Wave', 1966, 'Věra Chytilová', 7.8, 100,
     'https://s3.amazonaws.com/criterion-production/films/843772bdb4b9cb50d11e1f2a53203ed7/ZdvtQ87q4Sq692yE4pbIhruZXeGlOc_large.jpg',
     'Two young women engage in pranks and rebellion against a materialistic society.'),

    # Contemporary Classics (1990-2023)
    ('Parasite', 'Drama', 'Contemporary', 2019, 'Bong Joon-ho', 8.5, 98,
     'https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_.jpg',
     'A poor family schemes to become employed by a wealthy family.'),
    ('Everything Everywhere All at Once', 'Action', 'Contemporary', 2022, 'Daniels', 7.9, 95,
     'https://m.media-amazon.com/images/M/MV5BYTdiOTIyZTQtNmQ1OS00NjZlLWIyMTgtYzk5Y2M3ZDVmMDk1XkEyXkFqcGdeQXVyMTAzMDg4NzU0._V1_.jpg',
     'An aging Chinese immigrant is swept up in an insane adventure.'),
    ('The Silence of the Lambs', 'Thriller', 'Contemporary', 1991, 'Jonathan Demme', 8.6, 95,
     'https://m.media-amazon.com/images/M/MV5BNjNhZTk0ZmEtNjJhMi00YzFlLWE1MmEtYzM1M2ZmMGMwMTU4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
     'A young FBI cadet must receive the help of an incarcerated cannibal killer.'),
    ('Fight Club', 'Drama', 'Contemporary', 1999, 'David Fincher', 8.8, 79,
     'https://m.media-amazon.com/images/M/MV5BNDIzNDU0YzEtYzE5Ni00ZjlkLTk5ZjgtNjM3NWE4YzA3Nzk3XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_.jpg',
     'An insomniac office worker and a devil-may-care soapmaker form an underground fight club.'),
    ('The Usual Suspects', 'Crime', 'Contemporary', 1995, 'Bryan Singer', 8.5, 89,
     'https://m.media-amazon.com/images/M/MV5BYTViNjMyNmUtNDFkNC00ZDRlLThmMDUtZDU2YWE4NGI2ZjVmXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
     'A sole survivor tells of the twisty events leading up to a horrific gun battle on a boat.')
]

# Single executemany call for all movies
cursor.executemany('''
INSERT OR IGNORE INTO movies (title, genre, film_movement, year, director, imdb_rating, rotten_tomatoes_rating, image_url, description)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', all_movies)

# Commit changes and close connection only at the end
conn.commit()
conn.close() 