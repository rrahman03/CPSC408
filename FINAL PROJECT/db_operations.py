#import MySQL
import mysql.connector
class db_operations:
    def __init__(self, db_name):
        #Make Connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="CPSC408!",
            auth_plugin='mysql_native_password',
            database="MusicEvents")
        
        #create cursor object
        self.cursor = self.conn.cursor()
        print("Connection made")

        #Print out connection to verify and close
        #print(self.conn)
        #self.conn.close()

    # create attendee table
    def create_attendee_table(self):
        # query to create table Attendee
        query = '''
        CREATE TABLE Attendee(
            attendeeID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(100) NOT NULL,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(320) NOT NULL
        );
        '''
        # execute query
        self.cursor.execute(query)
        #commit modification made to database
        self.conn.commit()
        print('Attendee Table Successfully Created')

    # create organizer table
    def create_organizer_table(self):
        # query to create table Organizer
        query = '''
        CREATE TABLE Organizer(
            organizerID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(100) NOT NULL,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(320) NOT NULL
        );
        '''
        # execute query
        self.cursor.execute(query)
        #commit modification made to database
        self.conn.commit()
        print('Organizer Table Successfully Created')

    # create artist table
    def create_artist_table(self):
        # query to create table Artist
        query = '''
        CREATE TABLE Artist(
            artistID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            genre VARCHAR(100) NOT NULL
        );
        '''
        # execute query
        self.cursor.execute(query)
        #commit modification made to database
        self.conn.commit()
        print('Artist Table Successfully Created')

    # create venue table
    def create_venue_table(self):
        # query to create table Venue
        query = '''
        CREATE TABLE Venue(
            venueID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            address VARCHAR(200) NOT NULL,
            city VARCHAR(50) NOT NULL,
            state VARCHAR(50) NOT NULL,
            capacity INT NOT NULL
        );
        '''
        # execute query
        self.cursor.execute(query)
        #commit modification made to database
        self.conn.commit()
        print('Venue Table Successfully Created')

    # create event table
    def create_event_table(self):
        # query to create table Event
        query = '''
        CREATE TABLE Event(
            eventID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            date DATETIME NOT NULL,
            venueID INT NOT NULL,
            FOREIGN KEY (venueID) REFERENCES Venue (venueID)
        );
        '''
        # execute query
        self.cursor.execute(query)
        #commit modification made to database
        self.conn.commit()
        print('Event Table Successfully Created')

    # create ticket table
    def create_ticket_table(self):
        # query to create table Ticket
        query = '''
        CREATE TABLE Ticket(
            ticketID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            price DECIMAL(10,2) NOT NULL,
            tier VARCHAR(20) NOT NULL,
            purchaseDate DATE NOT NULL,
            eventID INT NOT NULL,
            FOREIGN KEY (eventID) REFERENCES Event (eventID),
            attendeeID INT NOT NULL,
            FOREIGN KEY (attendeeID) REFERENCES Attendee (attendeeID)
        );
        '''
        # execute query
        self.cursor.execute(query)
        #commit modification made to database
        self.conn.commit()
        print('Ticket Table Successfully Created')

    # create OrganizerEvent table
    def create_OrganizerEvent_table(self):
        # query to create table OrganizerEvent
        query = '''
        CREATE TABLE OrganizerEvent(
            organizerID INT NOT NULL,
            eventID INT NOT NULL,
            PRIMARY KEY (organizerID, eventID),
            FOREIGN KEY (eventID) REFERENCES Event (eventID),
            FOREIGN KEY (organizerID) REFERENCES Organizer (organizerID)
        );
        '''
        # execute query
        self.cursor.execute(query)
        #commit modification made to database
        self.conn.commit()
        print('OrganizerEvent Table Successfully Created')

    # create ArtistEvent table
    def create_ArtistEvent_table(self):
        # query to create table ArtistEvent
        query = '''
        CREATE TABLE ArtistEvent(
            artistID INT NOT NULL,
            eventID INT NOT NULL,
            PRIMARY KEY (artistID, eventID),
            FOREIGN KEY (eventID) REFERENCES Event (eventID),
            FOREIGN KEY (artistID) REFERENCES Artist (artistID)
        );
        '''
        # execute query
        self.cursor.execute(query)
        #commit modification made to database
        self.conn.commit()
        print('ArtistEvent Table Successfully Created')  

# Function to execute a query with parameters
    def execute_query(self, query, params=()):
        # executes a query 
        self.cursor.execute(query, params)
        self.conn.commit()

# function for running a select query with parameters
    def select_query_params(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()