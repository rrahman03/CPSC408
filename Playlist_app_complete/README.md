Raneem Rahman 
CPSC 408 
03/31/2025
rrahman@chapman.edu


LLM:
(1)
the code below was originally:

self.cursor.execute(query)
    print('Table Created')

this threw an error, I asked Chat GPT and it told me I needed another it was an operational error
link: https://chatgpt.com/share/67eb1d4c-0bac-8011-9c35-b007ee15c1de

self.cursor.execute("DROP TABLE IF EXISTS songs;")
self.cursor.execute(query)

#end of LLM code

(2)
in db_operations, the code was originally:
def bulk_insert_with_check(self, file_path):
        import csv
        data = helper.data_cleaner(file_path) 
        for row in data:
            name = row[1]      #name column
            artist = row[2]    #artist column
            if not self.song_exists(name, artist):
                self.insert_song(row)

is asked if there was an error because the new songs were not
being inserted from the updated csv. it told me to add a print 
to double check
link: https://chatgpt.com/share/67eb1db8-0270-8011-acab-250e11e83df9 

if not self.song_exists(name, artist):
    print(f"Inserting: {name} by {artist}")
    self.insert_song(row)
else:
    print(f"Skipped duplicate: {name} by {artist}")

#end of LLM code

the new csv file wasn't actually being uploaded so I asked Chat GPT what
the error was and it told me I needed the bulk_insert_with_check method
link: https://chatgpt.com/share/67eb1c81-29b4-8011-a411-443c2056322d

if choice.lower() == "yes":
    file_path = input("Enter the path to the CSV file: ")
    db_ops.bulk_insert_with_check(file_path)
else:
    print("Skipping new song load.")

#end of LLM code

(3)
the code was originally:
category = {
    1: "name",
    2: "album",
    3: "artist",
    4: "release_date", 
    5: "explicit"
}

it threw an error saying that the column Release_Date didn't exist.
I asked Chat GPT what the error was and it told me I needed to update the column name in my code
link: https://chatgpt.com/share/67eb1c0b-5ac0-8011-b9e2-4e86c0b02a71

category = {
    1: "Name",
    2: "Album",
    3: "Artist",
    4: "releaseDate"
    5: "Explicit"
}

#end of LLM

(4)
the code was originally:
def insert_song(self, song_tuple):
        placeholders = ("?," * len(song_tuple))[:-1]
        query = "INSERT INTO songs VALUES({placeholders})" 
        self.cursor.execute(query, song_tuple)
        self.connection.commit()

I asked Chat GPT if I needed an f string here because my values weren't actually inserting
link: https://chatgpt.com/share/67eb232c-15e0-8011-a4fd-5d851ef62b39

def insert_song(self, song_tuple):
    placeholders = ("?," * len(song_tuple))[:-1]
    query = f"INSERT INTO songs VALUES({placeholders})"
    self.cursor.execute(query, song_tuple)
    self.connection.commit()

#end of LLM


References used:
https://stackoverflow.com/questions/52400408/import-csv-file-into-python 
https://stackoverflow.com/questions/2615566/how-to-delete-from-a-table-where-id-is-in-a-list-of-ids 
https://stackoverflow.com/questions/46784322/provide-column-and-row-names-for-data-frame-in-1-line
https://www.geeksforgeeks.org/bulk-insert-in-sql-server/ 
https://stackoverflow.com/questions/7171041/what-does-it-mean-select-1-from-table 
https://www.geeksforgeeks.org/formatted-string-literals-f-strings-python/ 