# DROP TABLES

songplay_table_drop = "DROP table IF EXISTS songplays"
user_table_drop = "DROP table IF EXISTS users"
song_table_drop = "DROP table IF EXISTS songs"
artist_table_drop = "DROP table IF EXISTS artists"
time_table_drop = "DROP table IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
                            CREATE TABLE IF NOT EXISTS songplays
                            (songplay_id int PRIMARY KEY,start_time timestamp,user_id int,level text,song_id int,artist_id int,session_id int,location text,user_agent text);
""")

user_table_create = ("""
                        CREATE TABLE IF NOT EXISTS users
                        (user_id int PRIMARY KEY,first_name text,last_name text,gender text,level text)
""")

song_table_create = ("""
                        CREATE TABLE IF NOT EXISTS songs
                        (song_id text PRIMARY KEY,title text,artist_id text,year int,duration numeric)
""")

artist_table_create = ("""
                        CREATE TABLE IF NOT EXISTS artists
                        (artist_id text PRIMARY KEY,name text,location text,latitude numeric,longtitue numeric)
""")

time_table_create = ("""
                        CREATE TABLE IF NOT EXISTS time
                        (start_time timestamp,hour int,day int,week int,month int,year int,weekday int)
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
                        INSERT INTO songs (song_id,title,artist_id,year,duration)
                        VALUES (%s,%s,%s,%s,%s)
""")

artist_table_insert = ("""
                        INSERT INTO artists (artist_id,name,location,latitude,longtitue)
                        VALUES (%s,%s,%s,%s,%s)
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create,
                        song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop,
                      song_table_drop, artist_table_drop, time_table_drop]
