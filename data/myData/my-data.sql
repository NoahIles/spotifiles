-- RunOn Startup of container to import data on build
use db1;

-- $Create Tables; 
-- drop table if exists playlists;
-- TODO: add  {pl_image VARCHAR(100), }
Create TABLE IF NOT EXISTS playlists(
    _name VARCHAR(55) NOT NULL,
    num_followers INT(15) NOT NULL DEFAULT 0,
    duration_ms INT(15) NOT NULL DEFAULT 0,
    num_tracks INT(15) NOT NULL DEFAULT 0,
    modified_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    num_artists INT(15) DEFAULT 0 NOT NULL,
    num_albums INT(15) DEFAULT 0 NOT NULL,
    num_edits INT(15)  DEFAULT 0 NOT NULL,
    pid INT PRIMARY KEY NOT NULL,
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
    PRIMARY KEY (playlist_id, track_uri)
);
    -- Foreign keys will be added later on
    -- FOREIGN KEY (track_uri) REFERENCES tracks(track_uri) ON DELETE CASCADE,
    -- FOREIGN KEY (playlist_id) REFERENCES playlists(pl_id) ON DELETE CASCADE,

CREATE unique INDEX IF NOT EXISTS idx_playlist_Contents_playlist_id ON playlist_Contents(playlist_id, track_uri);
CREATE unique INDEX IF NOT EXISTS idx_playlist on playlists(pid);
CREATE unique INDEX IF NOT EXISTS idx_tracks on tracks(track_uri);

SET GLOBAL local_infile = false;
commit;