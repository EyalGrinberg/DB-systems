CREATE TABLE IF NOT EXISTS movies (
	id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    rate FLOAT,
    revenue BIGINT(15),
    release_date DATE,
    spoken_language varchar(100),
    runtime int,
    overview TEXT(450));  

  
CREATE TABLE IF NOT EXISTS actors (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    popularity FLOAT);  
    
CREATE TABLE IF NOT EXISTS characters (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    movie_id INT NOT NULL,
    actor_id INT,
    UNIQUE (movie_id, actor_id, name));
    
CREATE TABLE IF NOT EXISTS genres (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    UNIQUE(name)); 

CREATE TABLE IF NOT EXISTS movies_genres (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY(movie_id, genre_id)); 
    
    
ALTER TABLE movies ADD FULLTEXT(title);
ALTER TABLE actors ADD FULLTEXT(name);
ALTER TABLE characters ADD INDEX(movie_id);
ALTER TABLE characters ADD INDEX(actor_id);

ALTER TABLE characters
ADD CONSTRAINT FK_movie
FOREIGN KEY (movie_id) REFERENCES movies(id);

ALTER TABLE characters
ADD CONSTRAINT FK_actor
FOREIGN KEY (actor_id) REFERENCES actors(id);

ALTER TABLE movies_genres 
ADD CONSTRAINT FK_movies_genres_movie_id
FOREIGN KEY (movie_id) REFERENCES movies(id);

ALTER TABLE movies_genres 
ADD CONSTRAINT FK_movies_genres_genre_id
FOREIGN KEY (genre_id) REFERENCES genres(id);


ALTER TABLE movies ADD INDEX(rate);






