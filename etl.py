import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description: This function is responsible for reading files as
    json, preparing them according to database schema and ingesting
    them to database
    Arguments:
        cur: the cursor object.
        filepath: log data or song data file path.

    Returns:
        None
    """
    # open song file
    df = df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data = song_data.values[0]
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df[['artist_id', 'artist_name',
                      'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = artist_data.values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: This function is responsible for reading files as
    json object,preparing it according to database schema and inserting it
    to database

    Arguments:
        cur: the cursor object.
        filepath: log data or song data file path.

    Returns:
        None
    """
    # open log file
    df = df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = pd.Series(t.dt.time), pd.Series(t.dt.hour), pd.Series(t.dt.day), pd.Series(
        t.dt.weekofyear), pd.Series(t.dt.month), pd.Series(t.dt.year), pd.Series(t.dt.weekday)
    column_labels = ('timestamp', 'hour', 'day',
                     'week_of_day', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(data={column_labels[0]: time_data[0].values, column_labels[1]: time_data[1], column_labels[2]: time_data[2],
                           column_labels[3]: time_data[3], column_labels[4]: time_data[4], column_labels[5]: time_data[5], column_labels[6]: time_data[6]})
    time_df['timestamp'] = t
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid,
                         artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description: This function is responsible for listing the files in a directory,
    and then executing the ingest process for each file according to the function
    that performs the transformation to save it to the database.

    Arguments:
        cur: the cursor object.
        conn: connection to the database.
        filepath: log data or song data file path.
        func: function that transforms the data and inserts it into the database.

    Returns:
        None
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=postgres password=postgres")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
