-- RunOn Startup of container to import data on build
use db1;

-- drop table if exists tweetData;
-- Create TABLE tweetData(
--     user VARCHAR(25) NOT NULL,
--     fullname VARCHAR(60) NOT NULL,
--     tweet_id INT(25) PRIMARY KEY,
--     timestampp VARCHAR(25) NOT NULL,
--     urll VARCHAR(100) NOT NULL,
--     likes INT(15) NOT NULL,
--     replies INT(15) NOT NULL,
--     retweets INT(15) NOT NULL,
--     content VARCHAR(200) NOT NULL,
--     html VARCHAR(200) NOT NULL
-- );

-- SET GLOBAL local_infile = true;

-- LOAD DATA LOCAL INFILE '/myData/realDonaldTrump.csv'
--     INTO TABLE tweetData
--     FIELDS TERMINATED BY ','
--     OPTIONALLY ENCLOSED BY '"'
--     LINES TERMINATED BY '\n'
--     IGNORE 1 LINES
--     (user, fullname, tweet_id, timestampp,urll, likes, replies, retweets, content, html);

-- Create Tables; 
-- drop table if exists playlists;
Create TABLE IF NOT EXISTS playlists(
    pl_id VARCHAR(25) PRIMARY KEY NOT NULL,
    pl_name VARCHAR(55) NOT NULL,
    pl_description VARCHAR(200) NOT NULL,
    pl_image VARCHAR(100) NOT NULL,
    pl_followers INT(15) NOT NULL,
    pl_owner VARCHAR(25) NOT NULL,
    pl_owner_id VARCHAR(25) NOT NULL,
    pl_owner_url VARCHAR(100) NOT NULL
);

-- drop table if exists tracks; 
CREATE TABLE IF NOT EXISTS tracks(
    t_id INT PRIMARY KEY NOT NULL,
    t_name VARCHAR(60) NOT NULL,
    t_artists VARCHAR(100) NOT NULL,
    t_album VARCHAR(60) NOT NULL,
    t_album_art VARCHAR(100) NOT NULL,
    t_duration VARCHAR(25) NOT NULL
);

-- drop table if exists playlist_Contents;
CREATE TABLE IF NOT EXISTS playlist_Contents(
    playlist_id VARCHAR(25) NOT NULL,
    track_id INT NOT NULL,
    FOREIGN KEY (playlist_id) REFERENCES playlists(pl_id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES tracks(t_id) ON DELETE CASCADE
);

-- Insert Data into tables from json files



commit;
SET GLOBAL local_infile = false;
