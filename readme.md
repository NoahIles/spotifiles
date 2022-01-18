# CINS-465 Web Dev Final Project 
12-19-2021
A Dockerized Django web project implemented with GCP, spotipy, uses the spotify M.P.D.   

# Design 

## Priority A.T.M. 
* ~~Admin interface/user~~
```zsh
    # Need to run migrations before you can create a superuser for the admin interface
    python3 manage.py migrate
    python3 manage.py craetesuperuser
```
* Database interface 
    + Debate between mysql and postgresql 

## Features 
* Nice looking playlist viewer 
* Actually interface with spotify remote api to play songs from the playlists. 
* Some simple Keyword Search 
* Interface for things spotify doesnt really show easily, 
    + Top Tracks, Artists, Playlists (recently, mid-term, long-term)
    + Spotify Song Overlap???? 
* Using PostGre or Mysql as a database backend. 

## Stretch Goals 
* ANNOY Search 
* Use spotify Web-API to get a specific users Data
* Data overlap between two users. 
* Scope-Subset-Selector for search 
    + ALlow the user to have more impact on what is being searched. 
    + Search Specific Users Generated content
    + Search specific Geographic area's Content 
        - States Top 50 Songs 
* Kubernetes? implemented with kind? 