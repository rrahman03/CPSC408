#imports
from db_operations import db_operations
from helper import helper

#global variables
db_ops = db_operations("playlist.db")

#function to search songs by artists
def startScreen():

    print("Welcome to your playlist!")

    #[1. New Data Update]
    #ask user if they want to load new songs 
    print("Would you like to load new songs into the database? (yes/no)")
    choice = input()
    if choice.lower() == "yes":
        file_path = input("Enter the path to the CSV file: ")
        db_ops.bulk_insert(file_path)
    else:
        print("Skipping new song load.")


    #creates song table
    #db_ops.create_songs_table()
    db_ops.populate_songs_table("songs.csv")


#show user menu options
def options():
    print('''\nSelect from the following menu options: 
    1. Find songs by artist
    2. Find songs by genre
    3. Find songs by feature
    4. Update song info
    5. Delete a song
    6. Exit''')
    return helper.get_choice([1, 2, 3, 4, 5, 6])


#search for songs by artist
def search_by_artist():
    #get list of all artists in table
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist: ")
    artists = db_ops.single_attribute(query)

    #show all artists, create dictionary of options, and let user choose
    choices = {}
    for i in range(len(artists)):
        print(i, artists[i])
        choices[i] = artists[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Artist =:artist ORDER BY RANDOM()
    '''
    dictionary = {"artist":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#search songs by genre
def search_by_genre():
    #get list of genres
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist:")
    genres = db_ops.single_attribute(query)

    #show genres in table and create dictionary
    choices = {}
    for i in range(len(genres)):
        print(i, genres[i])
        choices[i] = genres[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Genre =:genre ORDER BY RANDOM()
    '''
    dictionary = {"genre":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#search songs table by features
def search_by_feature():
    #features we want to search by
    features = ['Danceability', 'Liveness', 'Loudness']
    choices = {}

    #show features in table and create dictionary
    choices = {}
    for i in range(len(features)):
        print(i, features[i])
        choices[i] = features[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #what order does the user want this returned in?
    print("Do you want results sorted in asc or desc order?")
    order = input("ASC or DESC: ")

    #print results
    query = "SELECT DISTINCT name FROM songs ORDER BY "+choices[index]+" "+order
    dictionary = {}
    if num != 0:
        query +=" LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#update song info 
def update_song_info():
    #[2. Song Update]
    song_name = input("Enter the name of the song you want to update: ")
    song = db_ops.get_song_by_name(song_name)
    if not song:
        print("Song not found.")
        return
    
    #display current song info
    print("Current Song Info:")
    categories = ['SongID', 'Name', 'Artist', 'Album', 'ReleaseDate', 'Explicit']
    for i in range(len(categories)):
        print(f"{i}: {categories[i]} = {song[0][i]}") #indexed values

    category = {
        1: "Name",
        2: "Artist",
        3: "Album",
        4: "ReleaseDate",
        5: "Explicit"
    }

    print("Which attribute would you like to update?")
    index = helper.get_choice(category.keys()) #get user's choice of field
    new_value = input(f"Enter new value for {category[index]}: ") #get new value

    db_ops.update_song_attribute(song_id=song[0][0], field=category[index], value=new_value)
    print("Song updated successfully!")



# delete song
def delete_song():
    #[3. Song Deletion]
    song_name = input("Enter the name of the song you want to delete: ")
    song = db_ops.get_song_by_name(song_name)
    if not song:
        print("Song not found.")
        return
    
    song_id = song[0][0] #tuple
    db_ops.delete_song_by_id(song_id) #delete song using SongID in WHERE clause

    print(f"Deleted '{song_name}' from playlist.")
    

#main method
startScreen()

#program loop
while True:
    user_choice = options()
    if user_choice == 1:
        search_by_artist()
    if user_choice == 2:
        search_by_genre()
    if user_choice == 3:
        search_by_feature()
    if user_choice == 4:
        update_song_info()
    if user_choice == 5:
        delete_song()
    if user_choice == 6:
        print("Goodbye!")
        break

db_ops.destructor()