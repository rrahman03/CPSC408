import sqlite3
import csv
from helper import helper

class db_operations():
    # constructor with connection path to DB
    def __init__(self, conn_path):
        self.connection = sqlite3.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("connection made..")

    # function to simply execute a DDL or DML query.
    # commits query, returns no results. 
    # best used for insert/update/delete queries with no parameters
    def modify_query(self, query): 
        self.cursor.execute(query)
        self.connection.commit()

    # function to simply execute a DDL or DML query with parameters
    # commits query, returns no results. 
    # best used for insert/update/delete queries with named placeholders
    def modify_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()

    # function to simply execute a DQL query
    # does not commit, returns results
    # best used for select queries with no parameters
    def select_query(self, query):
        result = self.cursor.execute(query)
        return result.fetchall()
    
    # function to simply execute a DQL query with parameters
    # does not commit, returns results
    # best used for select queries with named placeholders
    def select_query_params(self, query, dictionary):
        result = self.cursor.execute(query, dictionary)
        return result.fetchall()

    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with no parameters
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with named placeholders
    def single_record_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchone()[0]
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with no parameters
    def single_attribute(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        results.remove(None)
        return results
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with named placeholders
    def single_attribute_params(self, query, dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results
    
    # function for bulk inserting records
    # best used for inserting many records with parameters
    def bulk_insert(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()
    
    # function that creates table songs in our database
    def create_songs_table(self):
        query = '''
        CREATE TABLE songs(
            songID VARCHAR(22) NOT NULL PRIMARY KEY,
            Name VARCHAR(20),
            Artist VARCHAR(20),
            Album VARCHAR(20),
            ReleaseDate DATETIME,
            Genre VARCHAR(20),
            Explicit BOOLEAN,
            Duration DOUBLE,
            Energy DOUBLE,
            Danceability DOUBLE,
            Acousticness DOUBLE,
            Liveness DOUBLE,
            Loudness DOUBLE
        );
        '''
        # self.cursor.execute(query)
        # print('Table Created')
        self.cursor.execute("DROP TABLE IF EXISTS songs;")
        self.cursor.execute(query)

    # function that returns if table has records
    def is_songs_empty(self):
        #query to get count of songs in table
        query = '''
        SELECT COUNT(*)
        FROM songs;
        '''
        #run query and return value
        result = self.single_record(query)
        return result == 0

    # function to populate songs table given some path
    # to a CSV containing records
    def populate_songs_table(self, filepath):
        if self.is_songs_empty():
            data = helper.data_cleaner(filepath)
            attribute_count = len(data[0])
            placeholders = ("?,"*attribute_count)[:-1]
            query = "INSERT INTO songs VALUES("+placeholders+")"
            self.bulk_insert(query, data)

    # destructor that closes connection with DB
    def destructor(self):
        self.cursor.close()
        self.connection.close()

    # new song info
    def get_song_by_name(self, name):
        query = '''
        SELECT *
        FROM songs
        WHERE Name = ?;
        '''
        self.cursor.execute(query, (name,))
        return self.cursor.fetchall()

    def update_song_attribute(self, song_id, field, value):
        query = f'''
        UPDATE songs
        SET {field} = ?
        WHERE songID = ?;
        '''
        self.cursor.execute(query, (value, song_id))
        self.connection.commit()

    #ADDED
    #checks if song with given name and artist exists
    def song_exists(self, name, artist):
        query = '''
        SELECT 1 FROM songs
        WHERE Name = ? AND Artist = ?;
        '''
        self.cursor.execute(query, (name, artist))
        return self.cursor.fetchone() is not None

    #ADDED
    #inserts a single song
    def insert_song(self, song_tuple):
        placeholders = ("?," * len(song_tuple))[:-1]
        query = f"INSERT INTO songs VALUES({placeholders})"
        self.cursor.execute(query, song_tuple)
        self.connection.commit()

    #ADDED
    #bulk insert and checks for duplicates using song_exists
    def bulk_insert(self, file_path):
        import csv
        data = helper.data_cleaner(file_path)
        for row in data:
            name = row[1]      #name column
            artist = row[2]    #artist column
            if not self.song_exists(name, artist):
                self.insert_song(row)

    
    #deletes a song from the songs table by its ID
    def delete_song_by_id(self, song_id):
        query = "DELETE FROM Songs WHERE songID = :id"
        self.modify_query_params(query, {"id": song_id})
    
    def close_connection(self):
        self.connection.close()