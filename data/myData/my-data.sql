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
-- TODO: add  {pl_image VARCHAR(100), }
Create TABLE IF NOT EXISTS playlists(
    pl_name VARCHAR(55) NOT NULL,
    pl_followers INT(15) NOT NULL DEFAULT 0,
    pl_duration INT(15) NOT NULL DEFAULT 0,
    pl_num_tracks INT(15) NOT NULL DEFAULT 0,
    pl_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    pl_num_artists INT(15) DEFAULT 0 NOT NULL,
    pl_num_albums INT(15) DEFAULT 0 NOT NULL,
    pl_edits INT(15)  DEFAULT 0 NOT NULL,
    pl_id INT PRIMARY KEY NOT NULL,
    pl_description VARCHAR(200),
    pl_owner VARCHAR(25),
    pl_owner_url VARCHAR(100)
);

-- drop table if exists tracks; 
CREATE TABLE IF NOT EXISTS tracks(
    artist_name VARCHAR(100) NOT NULL,
    track_uri VARCHAR(50) PRIMARY KEY NOT NULL,
    artist_uri VARCHAR(65) NOT NULL,
    track_name VARCHAR(60) NOT NULL,
    album_uri VARCHAR(65) NOT NULL,
    duration_ms INT(25) NOT NULL,
    album_name VARCHAR(60) NOT NULL
);


-- drop table if exists playlist_Contents;
CREATE TABLE IF NOT EXISTS playlist_Contents(
    playlist_id INT NOT NULL,
    track_uri VARCHAR(50) NOT NULL,
    FOREIGN KEY (playlist_id) REFERENCES playlists(pl_id) ON DELETE CASCADE,
    FOREIGN KEY (track_uri) REFERENCES tracks(track_uri) ON DELETE CASCADE,
    PRIMARY KEY (playlist_id, track_uri)
);

SET GLOBAL local_infile = false;
commit;