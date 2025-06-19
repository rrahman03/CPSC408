# Imports
from db_operations import db_operations

# Import tkinter for front end
import tkinter as tk
from tkinter import *
from tkinter import messagebox

# Import csv to generate reports
import csv

# create db_ops object
db_ops = db_operations("MusicEvents.db")

# Start of LLM Code
# We had an error with tkinter not generating a new window
# We asked ChatGPT why this was happening and it suggested creating a function to clear the window
# https://chatgpt.com/c/682a5f39-29ec-8003-9c56-991decad2b2b
def clear_window():
    # Destroy each widget
    for widget in root.winfo_children():
        widget.destroy()
# End of LLM Code

# Start screen function
def startScreen():
    # Clear the current window in tkinter
    clear_window()

    # Welcome message
    tk.Label(root, text = "Welcome to the Music Events App!").pack()

    # Print buttons for user to either login or create an account
    tk.Button(root, text = "Login", command = get_account_type).pack()
    tk.Button(root, text = "Create Account", command = create_account).pack()



# Get the account type from the user
def get_account_type():
    # Clear window
    clear_window()

    # Ask User if they are an attendee or an organizer
    tk.Label(root, text = "Select Account Type:").pack()

    # Start of LLM Code
    # https://chatgpt.com/c/682a5fe1-9148-8003-a4b4-ca6f3a1df378
    # Originally when clicking the buttons, it was not directing to the correct page so we asked ChatGPT why this was happening
    # Original code: tk.Button(root, text = "Attendee", command = login("Attendee")).pack()
    # Original code: tk.Button(root, text = "Organizer", command = login("Organizer")).pack()
    # ChatGPT suggested adding lambda to defer execution until the button is clicked
    # Create attendee button
    # if clicked, will navigate to attendee login
    tk.Button(root, text = "Attendee", command = lambda: login("Attendee")).pack()

    # Create Organizer Button
    # If clicked, will navigate to organizer login
    tk.Button(root, text = "Organizer", command = lambda: login("Organizer")).pack()
    
    # End of LLM Code

# Login function
# Takes account type as a parameter
def login(account_type):
    # Clear the window
    clear_window()

    # Login page label
    tk.Label(root, text = f"{account_type} Login", font = ("", 16, "bold")).pack(pady=10)

    # Get username text entry
    tk.Label(root, text = "username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    # Get password text entry
    tk.Label(root, text = "Password").pack()
    password_entry = tk.Entry(root, show = '*')
    password_entry.pack()

    # Function to handle login operations
    def login_operations():
        # Get username and password
        username = username_entry.get()
        password = password_entry.get()

        # Login to the corresponding account type
        if account_type == "Attendee":
            # Get the account with the given username and password
            query = '''
            SELECT attendeeID
            FROM Attendee
            WHERE username = %s
            AND password = %s'''

        else:
            query = '''
            SELECT organizerID
            FROM Organizer
            WHERE username = %s
            AND password = %s'''
        
        # Run query with given username and password as parameters
        # Returns the user ID for the corresponding user
        result = db_ops.select_query_params(query, (username, password))

        # If login is successful (the username/password combination exists in the database)
        # Then allow user into application
        if result:
            messagebox.showinfo("Success", "Login Successful!")

            # If the user is an attendee, direct them to the attendee dashboard
            if account_type == "Attendee":
                # Call the attendee operations function with the current ID
                attendee_operations(result)
            else:
                # Call the organizer operations function with the current ID
                organizer_operations(result)
    
    # Login button
    # Calls login operations function
    tk.Button(root, text="Login", command=login_operations).pack(pady=10)

# Attendee operations
# Takes in parameter of Attendee ID
def attendee_operations(attendee_id):
    # Clear window
    clear_window()

    # Attendee dashboard
    tk.Label(root, text="Attendee Dashboard", font=("", 16, "bold")).pack(pady=10)

    # Options Menu
    tk.Button(root, text="Events", command =lambda: view_events(attendee_id)).pack()
    tk.Button(root, text="Artists", command =lambda: view_artists(attendee_id)).pack()
    tk.Button(root, text="Venues", command =lambda: view_venues(attendee_id)).pack()
    tk.Button(root, text="Purchase Ticket", command =lambda: purchase_ticket(attendee_id)).pack()
    tk.Button(root, text="My Tickets", command =lambda: my_tickets(attendee_id)).pack()
    tk.Button(root, text="View Events by Artist", command =lambda: events_by_artist(attendee_id)).pack()
    tk.Button(root, text="View Events by Venue", command =lambda: events_by_venue(attendee_id)).pack()
    tk.Button(root, text="Popular Artists", command=lambda: popular_artists(attendee_id)).pack()
    tk.Button(root, text="Export My Tickets (CSV)", command=lambda: export_my_tickets_to_csv(attendee_id)).pack()
    

    # Logout Button
    # Returns to start screen
    tk.Button(root, text="Logout", command = startScreen).pack(pady=20)


# Organizer operations
# Takes in parameter or Organizer ID
def organizer_operations(organizer_ID):
    # Clear window
    clear_window()

    # Organizer dahsboard
    tk.Label(root, text="Organizer Dashboard", font=("", 16, "bold")).pack(pady=10)
    
    # Options menu
    tk.Button(root, text="Update Event Info", command =lambda: update_event(organizer_ID)).pack()
    tk.Button(root, text="Update Artist Info", command =lambda: update_artist(organizer_ID)).pack()
    tk.Button(root, text="Update Venue Info", command =lambda: update_venue(organizer_ID)).pack()
    tk.Button(root, text="Delete Event", command =lambda: delete_event(organizer_ID)).pack()
    tk.Button(root, text="Event Count by Venue", command=lambda: event_count_by_venue(organizer_ID)).pack()
    tk.Button(root, text="Export Events (CSV)", command=lambda: export_events_to_csv()).pack()

    # Logout Button
    # Returns to start screen
    tk.Button(root, text="Logout", command = startScreen).pack(pady=20)


# Create a new account
def create_account():
    # Clear the window
    clear_window()
    
    # Create Account label
    tk.Label(root, text="Create Account", font = ("", 16, "bold")).pack(pady=10)

    # Select account type Label
    tk.Label(root, text="Select Account Type:").pack()

    # Create variable for account type
    # I referenced this website to read more about tk.StringVar()
    # https://stackoverflow.com/questions/69738637/tkinter-stringvar 
    account_type = tk.StringVar()

    # Create Organizer and Attendee buttons and store selection as account_type
    tk.Radiobutton(root, text="Attendee", variable=account_type, value="Attendee").pack()
    tk.Radiobutton(root, text="Organizer", variable=account_type, value="Organizer").pack()

    # Get username
    tk.Label(root, text="Username").pack()
    # Get username entry
    username_entry = tk.Entry(root)
    username_entry.pack()

    # Get password
    tk.Label(root, text="Password").pack()
    # Get password entry
    # Show * instead of letters when typing
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    # Get name
    tk.Label(root, text="Name").pack()
    # Get name entry
    name_entry = tk.Entry(root)
    name_entry.pack()

    # Get email
    tk.Label(root, text="Email").pack()
    # Get email entry
    email_entry = tk.Entry(root)
    email_entry.pack()


    # Function to enter the new user into the database
    def register_user():
        # Add changes to SQL
        # Get all values
        account = account_type.get()
        username = username_entry.get()
        password = password_entry.get()
        name = name_entry.get()
        email = email_entry.get()

        # Make sure all feilds have a value:
        # If a value is missing, show an error message and return
        if not (account and username and password and name and email):
            messagebox.showerror("Error", "Please enter a value for all items.")
            return
        
        # Check if username is taken already
        # Get the count of how many people have the given username
        if account == "Attendee":
            username_query = '''
            SELECT COUNT(*)
            FROM Attendee
            WHERE username = %s'''
        else:
            username_query = '''
            SELECT COUNT(*)
            FROM Organizer
            WHERE username = %s'''
        result = db_ops.select_query_params(username_query, (username,))

        # If there is already an account with the given username return an error message
        # If the result is greater than 0, then the username is already taken
        if result[0] > 0:
            messagebox.showerror("Error", "Username already exists! Please choose a new one.")
            return
        
        # If creating Attendee account, create a new Attendee record
        if account == "Attendee":
            # Insert into Attendee
            attendee_query = '''
                INSERT INTO Attendee (username, password, name, email)
                VALUES (%s, %s, %s, %s);
            '''
            db_ops.execute_query(attendee_query, (username, password, name, email))

            # Return a message to the user indicaing successful account creation
            messagebox.showinfo("Success","Created new Attendee account!")
            # Return to start screen
            startScreen()
        
        # If creating an Organizer account, create new Organizer record
        elif account == "Organizer":
            # Insert into Organizer
            organizer_query = '''
                INSERT INTO Organizer (username, password, name, email)
                VALUES (%s, %s, %s, %s);
            '''
            db_ops.execute_query(organizer_query, (username, password, name, email))

            # Return a message to the user indicaing successful account creation
            messagebox.showinfo("Success", "Created new Organizer account!")
            # Return to start screen
            startScreen()
        
        # If invalid account type, return error message and close
        else:
            messagebox.showerror("Error", "Invalid account type.")
            return

    # Button to create an account
    # Calls register_user function to submit the changes to the database
    tk.Button(root, text="Create Account", command=register_user).pack(pady=10)


# View Events
def view_events(attendee_id):
    # clear window
    clear_window()
    # Page label
    tk.Label(root, text="View Events", font = ("", 16, "bold")).pack(pady=10)

    # Query to get all event info
    # Select from vEventInfo view
    # Order by date
    event_query = '''
    SELECT * 
    FROM vEventInfo
    ORDER BY date ASC;
    '''
    # Execute query
    db_ops.cursor.execute(event_query)
    results = db_ops.cursor.fetchall()

    # If none, return an error message
    if not results:
        messagebox.showerror("Error", 'No events found')
        return 
    
    # Loop through results and display each event 
    for event in results:
        name, date, venue, city, state = event
        # Return each individual event with its corresponding info
        tk.Label(root, text = f"{name} | {date} | {venue} | {city}, {state}").pack()

    # Logout button
    tk.Button(root, text="Back", command=lambda: attendee_operations(attendee_id)).pack(pady=20)

# View Artists
def view_artists(attendee_id):
    # Clear window
    clear_window()
    # Page label
    tk.Label(root, text="Artists", font = ("", 16, "bold")).pack(pady=10)

    # Query to get all artists ordered by name
    # Select from vArtistInfo view
    artist_query = '''
    SELECT *
    FROM vArtistInfo
    ORDER BY name;
    '''
    # Execute query
    db_ops.cursor.execute(artist_query)
    results = db_ops.cursor.fetchall()

    # If no artists, return error message
    if not results: 
        messagebox.showerror("Error", 'No artists found')
        return
    
    # Loop through and display each artist's name and genre
    for artist in results:
        name, genre = artist
        # Return each individual artist with their corresponding info
        tk.Label(root, text = f"{name} | {genre}").pack()

    # Logout button
    tk.Button(root, text="Back", command=lambda: attendee_operations(attendee_id)).pack(pady=20)


# View Venues
def view_venues(attendee_id):
    # Clear window
    clear_window()
    # Page label
    tk.Label(root, text="Venues", font = ("", 16, "bold")).pack(pady=10)

    # Query to get venue info ordered by city
    # Select from vVenueInfo view
    # Order by city
    venue_query = '''
    SELECT *
    FROM vVenueInfo
    ORDER BY city;
    '''
    # Execute query
    db_ops.cursor.execute(venue_query)
    results = db_ops.cursor.fetchall()

    # If no venues, return error message
    if not results:
        messagebox.showerror("Error", "No venues found")
        return
    
    # Display each venue name, address, city, state, and capacity
    for venue in results:
        name, address, city, state, capacity = venue
        # Return each individual venue with its corresponding info
        tk.Label(root, text = f"{name} | {address} | {city}, {state} | {capacity}").pack()

    # Logout button
    tk.Button(root, text="Back", command=lambda: attendee_operations(attendee_id)).pack(pady=20)


# Purchase a ticket
def purchase_ticket(attendee_id):
    # Clear window
    clear_window()
    # Page label
    tk.Label(root, text="Purchase Ticket", font=("", 16, "bold")).pack(pady=10)

    # Query to get event info sorted by date
    event_query = '''
    SELECT eventID, Event.name, Event.date, Venue.name
    FROM Event
    INNER JOIN Venue ON Event.venueID = Venue.venueID
    WHERE Event.is_deleted = FALSE
    ORDER BY Event.date ASC;
    '''
    # Execute query
    db_ops.cursor.execute(event_query)
    results = db_ops.cursor.fetchall()

    # If no events, return error
    if not results:
        messagebox.showerror("Error", "No events available")
        return

    # Dropdown to select event 
    event_var = tk.StringVar(root)
    event_options = [f"{r[1]} at {r[3]} on {r[2]} (ID: {r[0]})" for r in results]
    event_var.set(event_options[0])
    tk.Label(root, text="Select Event:").pack()
    tk.OptionMenu(root, event_var, *event_options).pack()

    # Add entry fields for ticket price and tier 
    # Ticket price entry
    tk.Label(root, text="Ticket Price ($):").pack()
    price_entry = tk.Entry(root)
    price_entry.pack()

    # Tier entry
    tk.Label(root, text="Ticket Tier (e.g. GA, VIP):").pack()
    tier_entry = tk.Entry(root)
    tier_entry.pack()

    # Function to add a ticket to the database
    def submit_ticket():
        try:
            selected = event_var.get()
            event_id = int(selected.split("ID: ")[1].replace(")", ""))
            price = float(price_entry.get())
            tier = tier_entry.get().strip()

            # If no entry, return an error
            if not tier:
                messagebox.showerror("Error", "Please enter a tier.")
                return

            # Insert ticket purchase into Ticket table 
            insert_query = '''
            INSERT INTO Ticket (eventID, attendeeID, price, tier, purchaseDate)
            VALUES (%s, %s, %s, %s, NOW())
            '''
            # Execute query
            db_ops.execute_query(insert_query, (event_id, attendee_id[0], price, tier))
            # success message
            messagebox.showinfo("Success", "Ticket purchased successfully!")

        # Failure message
        except Exception as e:
            messagebox.showerror("Error", f"Failed to purchase ticket: {str(e)}")

    # Confirm pruchase with a success messages
    tk.Button(root, text="Confirm Purchase", command=submit_ticket).pack(pady=10)
    tk.Button(root, text="Back", command=lambda: attendee_operations(attendee_id)).pack(pady=10)


# View Tickets
def my_tickets(attendee_id):
    # Clear window
    clear_window()
    # Page label
    tk.Label(root, text="My Tickets", font = ("", 16, "bold")).pack(pady=10)

    # Query to get ticket info sorted by date
    myticket_query = '''
    SELECT Event.name, Event.date, Venue.name, Ticket.price, Ticket.tier
    FROM Ticket
    INNER JOIN Event ON Ticket.eventID = Event.eventID
    INNER JOIN Venue ON Event.venueID = Venue.venueID
    WHERE Ticket.attendeeID = %s
    AND Event.is_deleted = FALSE
    ORDER BY Event.date ASC;
    '''

    # Execute query
    db_ops.cursor.execute(myticket_query, (attendee_id[0],))
    results = db_ops.cursor.fetchall()

    # If no tickets found, return an error message
    if not results:
        messagebox.showinfo("Error", 'You have no purchased tickets')
        return
    
    # Display the ticket that has event name, date, and venue name
    for name, date, venue, price, tier in results:
        tk.Label(root, text=f"{name} | {date} | {venue} | ${price:.2f} | {tier}").pack()

    # Back button
    tk.Button(root, text="Back", command=lambda: attendee_operations(attendee_id)).pack(pady=20)


# Events by artist
def events_by_artist(attendee_id):
    # Clear window
    clear_window()
    # Page label
    tk.Label(root, text="View Events by Artist", font = ("", 16, "bold")).pack(pady=10)

    # Query to get artists ordered by name
    artistevent_query = '''
    SELECT artistID, name 
    FROM Artist
    ORDER BY name;
    '''
    # Execute query
    db_ops.cursor.execute(artistevent_query)
    results = db_ops.cursor.fetchall()

    # If not artists, return error
    if not results:
        messagebox.showinfo("Error", "No artists available")
        return
    
    # Dropdown setup to select an artist
    artist_var = tk.StringVar(root)
    artist_options = [f"{name} (ID: {artistID})" for artistID, name in results]
    artist_var.set(artist_options[0])

    # Get artist selection
    tk.Label(root, text="Select Artist:").pack()
    tk.OptionMenu(root, artist_var, *artist_options).pack()

    # Display
    result_frame = tk.Frame(root)
    result_frame.pack(pady=10)

    # Function to fetch and display events
    def fetch_events():

        # get selected artist
        selected = artist_var.get()
        artist_id = int(selected.split("ID: ")[1].replace(")", ""))

        # Query to get events for given artist ordered by date
        fetchEvent_query = '''
        SELECT Artist.name, Event.name, Event.date, Venue.name
        FROM Event
        INNER JOIN ArtistEvent ON Event.eventID = ArtistEvent.eventID
        INNER JOIN Venue ON Event.venueID = Venue.venueID
        INNER JOIN Artist ON ArtistEvent.artistID = Artist.artistID
        WHERE ArtistEvent.artistID = %s
        AND Event.is_deleted = FALSE
        ORDER BY Event.date;
        '''
        # Execute query
        db_ops.cursor.execute(fetchEvent_query, (artist_id,))
        event_results = db_ops.cursor.fetchall()

        # If no events, return an error
        if not event_results:
            messagebox.showerror("Error", 'No Events found for this artist')
            return
        
        # Print out events
        for artist_name, event_name, date, venue  in event_results:
            tk.Label(result_frame, text=f"{artist_name}: {event_name} | {date} | {venue}").pack()

    # Add view events button
    tk.Button(root, text="View Events", command=fetch_events).pack(pady=5)
    # Back button
    tk.Button(root, text="Back", command=lambda: attendee_operations(attendee_id)).pack(pady=10)
        


# Events by venue
def events_by_venue(attendee_id):
    # Clear window
    clear_window()
    # Page label
    tk.Label(root, text="View Events by Venue", font = ("", 16, "bold")).pack(pady=10)

    # Query to get venues ordered by city
    venue_query = '''
    SELECT venueID, name
    FROM Venue
    ORDER BY city;
    '''
    # Execute query
    db_ops.cursor.execute(venue_query)
    results = db_ops.cursor.fetchall()

    # If no venues, return an error
    if not results:
        messagebox.showerror("Error", "No venues available")
        return
    
    # Dropdown setup to select a venue
    venue_var = tk.StringVar(root)
    venue_options = [f"{name} (ID: {venueID})" for venueID, name in results]
    venue_var.set(venue_options[0])

    # Get venue selection
    tk.Label(root, text="Select Venue:").pack()
    tk.OptionMenu(root, venue_var, *venue_options).pack()

    # Display
    result_frame = tk.Frame(root)
    result_frame.pack(pady=10)

    # Function to fetch and display events
    def fetch_events():

        selected = venue_var.get()
        venue_id = int(selected.split("ID: ")[1].replace(")", ""))

        # Query to get events for given venue ordered by date
        fetchEvent_query = '''
        SELECT Venue.name, Event.name, Event.date
        FROM Event
        INNER JOIN Venue ON Event.venueID = Venue.venueID
        WHERE Venue.venueID = %s
        AND Event.is_deleted = FALSE
        ORDER BY Event.date;
        '''
        # Execute query
        db_ops.cursor.execute(fetchEvent_query, (venue_id,))
        event_results = db_ops.cursor.fetchall()

        # If no events, return an error
        if not event_results:
            messagebox.showerror("Error", 'No Events found for this artist')
            return
        
        # Print out events
        for venue_name, event_name, date  in event_results:
            tk.Label(result_frame, text=f"{venue_name}: {event_name} | {date}").pack()

    # Add view events button
    tk.Button(root, text="View Events", command=fetch_events).pack(pady=5)
    # Back button
    tk.Button(root, text="Back", command=lambda: attendee_operations(attendee_id)).pack(pady=10)


def update_event(organizer_id):
    # Clear window
    clear_window()
    # Page label
    tk.Label(root, text="Update Event Info", font = ("", 16, "bold")).pack(pady=10)

    # Query to get event info
    query = '''
    SELECT eventID, name, date 
    FROM Event 
    WHERE is_deleted = FALSE
    ORDER BY name;
    '''
    # Execute query
    db_ops.cursor.execute(query)
    results = db_ops.cursor.fetchall()

    # If no events, return error
    if not results:
        messagebox.showerror("Error", "No events available to update")
        return
    
    # Create dropdown to select event to update
    tk.Label(root, text="Select Event to Update:").pack()
    event_var = tk.StringVar(root)
    event_options = [f"{name} on {date} (ID: {eventID})" for eventID, name, date in results]
    event_var.set(event_options[0])
    tk.OptionMenu(root, event_var, *event_options).pack()

    #  Get Event name entry
    tk.Label(root, text="New Event Name:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    # Get event date entry
    tk.Label(root, text="New Event Date (YYYY-MM-DD):").pack()
    date_entry = tk.Entry(root)
    date_entry.pack()

    # Confirmation message
    # Update function
    def submit_update():
        # Get selected event, name, and date
        selected = event_var.get()
        event_id = int(selected.split("ID: ")[1].replace(")", ""))
        new_name = name_entry.get().strip()
        new_date = date_entry.get().strip()

        # If no name or date are provided, show an error
        if not new_name or not new_date:
            messagebox.showerror("Error", "Please enter both new name and date.")
            return
        
        try:
            # Query to update event with new name and date
            update_query = '''
            UPDATE Event
            SET name = %s, date = %s
            WHERE eventID = %s;
            '''
            # Execute and submit changes
            db_ops.cursor.execute(update_query, (new_name, new_date, event_id))
            db_ops.conn.commit()

            # Success Message
            messagebox.showinfo("Success", "Event updated successfully.")

            # Return to dashboard
            organizer_operations(organizer_id)

        except Exception as e:
            # If update fails, rollback and do not keep changes
            db_ops.conn.rollback()
            messagebox.showerror("Error", f"Update failed: {str(e)}")

    tk.Button(root, text="Submit Update", command=submit_update).pack(pady=10)
    tk.Button(root, text="Back", command=lambda: organizer_operations(organizer_id)).pack(pady=10)


def update_artist(organizer_ID):
    # Clear window
    clear_window()
    # Page label
    tk.Label(root, text="Update Artist Info", font = ("", 16, "bold")).pack(pady=10)

    # Query to get artist info
    query = '''
    SELECT artistID, name, genre 
    FROM Artist 
    ORDER BY name;
    '''
    # Execute query
    db_ops.cursor.execute(query)
    results = db_ops.cursor.fetchall()

    # If no artists, return error
    if not results:
        messagebox.showerror("Error", "No artists available")
        return
    
    # Dropdown to select artist to update
    tk.Label(root, text="Select Artist to Update:").pack()
    artist_var = tk.StringVar(root) 
    # Forman options
    artist_options = [f"{name} | {genre} (ID: {artistID})" for artistID, name, genre in results]
    artist_var.set(artist_options[0])
    tk.OptionMenu(root, artist_var, *artist_options).pack()

    # Add input fields to update artist info for new name and new genre
    tk.Label(root, text="New Artist Name:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    # Entry field for new artist genre
    tk.Label(root, text="New Genre:").pack()
    genre_entry = tk.Entry(root)
    genre_entry.pack()
    
    # Confirmation message
    def submit_update():
        selected = artist_var.get()
        artist_id = int(selected.split("ID: ")[1].replace(")", ""))
        new_name = name_entry.get().strip()
        new_genre = genre_entry.get().strip()

        # Makes sure that both fields are filled
        if not new_name or not new_genre:
            messagebox.showerror("Error", "Please enter both new name and genre.")
            return

        try:
            query = '''
            UPDATE Artist
            SET name = %s, genre = %s
            WHERE artistID = %s;
            '''
            # Execute update
            db_ops.cursor.execute(query, (new_name, new_genre, artist_id))
            db_ops.conn.commit()
            messagebox.showinfo("Success", "Artist updated successfully.")
            organizer_operations(organizer_ID)
        except Exception as e:
            db_ops.conn.rollback()
            messagebox.showerror("Error", f"Update failed: {str(e)}")

    # Button to submit the update
    tk.Button(root, text="Submit Update", command=submit_update).pack(pady=10)
    # Button to return to organizer operations page
    tk.Button(root, text="Back", command=lambda: organizer_operations(organizer_ID)).pack(pady=10)



def update_venue(organizer_ID):
    # Clear window
    clear_window()
    # Page label
    tk.Label(root, text="Update Venue Info", font = ("", 16, "bold")).pack(pady=10)

    # Query to get venue info
    query = '''
    SELECT venueID, name 
    FROM Venue 
    ORDER BY name;
    '''
    # Execute query
    db_ops.cursor.execute(query)
    results = db_ops.cursor.fetchall()

    # If no venues, return error
    if not results:
        messagebox.showerror("Error", "No venues available")
        return
    
    # Create dropdown to select venue
    tk.Label(root, text="Select Venue to Update:").pack()
    venue_var = tk.StringVar(root)
    venue_options = [f"{name} (ID: {venueID})" for venueID, name in results]
    venue_var.set(venue_options[0])
    tk.OptionMenu(root, venue_var, *venue_options).pack()


    # Add input fields to update venue info (address, city, state, capacity)
    tk.Label(root, text="New Address:").pack()
    address_entry = tk.Entry(root)
    address_entry.pack()

    # Get new city
    tk.Label(root, text="New City:").pack()
    city_entry = tk.Entry(root)
    city_entry.pack()

    # Get new state
    tk.Label(root, text="New State:").pack()
    state_entry = tk.Entry(root)
    state_entry.pack()

    # Get new capacity
    tk.Label(root, text="New Capacity:").pack()
    capacity_entry = tk.Entry(root)
    capacity_entry.pack()


    # Handles form submission and updates the venue
    def submit_update():
        selected = venue_var.get()
        venue_id = int(selected.split("ID: ")[1].replace(")", ""))
        address = address_entry.get().strip()
        city = city_entry.get().strip()
        state = state_entry.get().strip()

        # Validate capacity input 
        try:
            capacity = int(capacity_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Capacity must be an integer.")
            return

        # Check if fields are missing
        if not address or not city or not state:
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        try:
            query = '''
            UPDATE Venue
            SET address = %s, city = %s, state = %s, capacity = %s
            WHERE venueID = %s;
            '''
            # Execute the update with input values
            db_ops.cursor.execute(query, (address, city, state, capacity, venue_id))
            db_ops.conn.commit()
            messagebox.showinfo("Success", "Venue updated successfully.")
            organizer_operations(organizer_ID) # Return to organizer menue
        except Exception as e:
            db_ops.conn.rollback() # Roll back transaction
            messagebox.showerror("Error", f"Update failed: {str(e)}")

    # Button to submit the update
    tk.Button(root, text="Submit Update", command=submit_update).pack(pady=10)
    # Button to go back to organizer operations page
    tk.Button(root, text="Back", command=lambda: organizer_operations(organizer_ID)).pack(pady=10)



# Implement transaction
# Delete Event
# Soft deletion of given event
# Marks event as deleted rather than removing from database entirely
def delete_event(organizer_ID):
    # clear window
    clear_window()
    # Page label
    tk.Label(root, text="Delete Event", font = ("", 16, "bold")).pack(pady=10)


    # Prompt user to enter event name
    tk.Label(root, text="Enter the name of the event to delete:").pack(pady=10)
    name_entry = tk.Entry(root)
    name_entry.pack(pady=10)

    # Function to confirm event deletion
    def confirm_deletion():
    # Get the event name
        event_name = name_entry.get().strip()

        # If no entry,
        # Return an error
        if not event_name:
            messagebox.showerror("Error", "Please enter an event name.")
            return
        try:
            # Turn off autocommit
            db_ops.conn.autocommit = False

            # Search for event by name
            event_name_query = '''
            SELECT eventID
            FROM Event
            WHERE name = %s;
            '''
            db_ops.cursor.execute(event_name_query, (event_name,))
            result = db_ops.cursor.fetchone()

            # If no event is found with given name, return an error
            if not result:
                db_ops.conn.rollback()
                messagebox.showerror("Error", "No event found.")
                return

            # Get event id
            event_id = result[0]

            # Confirm event deletion
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {event_name}?")

            if confirm:
                # Soft delete: set is_deleted to TRUE
                delete_query = '''
                UPDATE Event
                SET is_deleted = TRUE
                WHERE eventID = %s;
                '''
                db_ops.cursor.execute(delete_query, (event_id,))
                db_ops.conn.commit()
                messagebox.showinfo("Success", f"{event_name} successfully deleted.")
            else:
                db_ops.conn.rollback()
                messagebox.showinfo("Cancelled", "Event deletion cancelled.")

        # Rollback if delete failed
        except Exception as e:
            db_ops.conn.rollback()
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Delete event button
    tk.Button(root, text="Delete Event", command=confirm_deletion).pack(pady=10)

    # Back button
    tk.Button(root, text="Back", command=lambda: organizer_operations(organizer_ID)).pack(pady=20)


# Function to create the views that will be utilized within the database
def create_views():

    # Create view for artist info
    artist_query = '''
    CREATE VIEW vArtistInfo AS
    SELECT name, genre 
    FROM Artist
    ORDER BY name;
    '''
    db_ops.execute_query(artist_query)

    # Create view for venue info
    venue_query = '''
    CREATE VIEW vVenueInfo AS
    SELECT name, address, city, state, capacity 
    FROM Venue
    ORDER BY city;
    '''
    db_ops.execute_query(venue_query)

    # Create view for event info
    event_query = '''
    CREATE VIEW vEventInfo AS
    SELECT Event.name AS "event_name", Event.date, Venue.name AS "venue_name", Venue.city, Venue.state
    FROM Event
    INNER JOIN Venue ON Event.venueID = Venue.venueID
    WHERE is_deleted = FALSE;
    '''
    db_ops.execute_query(event_query)


# Aggregation/group by
# Event count by venue
# Counts the number of events at each venue and orders by venue with most events first 
def event_count_by_venue(organizer_ID):
    clear_window()
    tk.Label(root, text="Event Count by Venue", font=("", 16, "bold")).pack(pady=10)

    # GROUP BY QUERY
    query = '''
    SELECT Venue.name, COUNT(Event.eventID) as num_events
    FROM Event
    JOIN Venue ON Event.venueID = Venue.venueID
    WHERE is_deleted = FALSE
    GROUP BY Venue.name
    ORDER BY num_events DESC;
    '''

    db_ops.cursor.execute(query)
    results = db_ops.cursor.fetchall()

    if not results:
        messagebox.showinfo("Info", "No event data available.")
        return 
    
    # Results 
    for venue_name, num_events in results:
        tk.Label(root, text=f"{venue_name}: {num_events} event(s)").pack()

    tk.Button(root, text="Back", command=lambda: organizer_operations(organizer_ID)).pack(pady=20)


# Feature with subquery
# Artists with two or more events
def popular_artists(attendee_id):
    clear_window()
    tk.Label(root, text="Popular Artists (2+ Events)", font=("", 16, "bold")).pack(pady=10)

    # Query with subquery
    query = '''
    SELECT name, genre
    FROM Artist
    WHERE artistID IN (
        SELECT artistID
        FROM ArtistEvent
        GROUP BY artistID
        HAVING COUNT(eventID) >= 2
    );
    '''
    # Execute query
    db_ops.cursor.execute(query)
    results = db_ops.cursor.fetchall()
    
    # If no result, show error
    if not results:
        messagebox.showerror("Error", "No artists found with 2+ events.")
        return
    
    # Display artist name and genre
    for name, genre in results:
        tk.Label(root, text=f"{name} | {genre}").pack()

    # Back button
    tk.Button(root, text="Back", command=lambda: attendee_operations(attendee_id)).pack(pady=20)



# CSV export of events
def export_events_to_csv():
    # Get all event info from view 
    query = '''
    SELECT * 
    FROM vEventInfo
    ORDER BY date ASC;
    '''
    # Execute query
    db_ops.cursor.execute(query)
    results = db_ops.cursor.fetchall()

    # If no result, show error
    if not results:
        messagebox.showerror("Error", "No events to export.")
        return
    
    # Write to CSV
    with open("events_export.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        # Header row (adjust based on your view)
        writer.writerow(["Event Name", "Date", "Venue", "City", "State"])
        writer.writerows(results)

    # Get file path
    # I referenced this link for help:
    # https://www.tutorialspoint.com/How-to-print-full-path-of-current-file-s-directory-in-Python
    import os
    file_path = os.path.abspath("events_tickets_export.csv")
    # End of reference

    # Show successful completion
    messagebox.showinfo("Success", f"Events exported to 'events_export.csv'.\n\n File Path: {file_path}")
    return

# Attendees ticket history
# Exports to a csv file
def export_my_tickets_to_csv(attendee_id):
    # Query to get ticket info for attendee
    query = '''
    SELECT Event.name, Event.date, Venue.name, Ticket.price
    FROM Ticket
    INNER JOIN Event ON Ticket.eventID = Event.eventID
    INNER JOIN Venue ON Event.venueID = Venue.venueID
    WHERE Ticket.attendeeID = %s
    AND Event.is_deleted = FALSE
    ORDER BY Event.date ASC;
    '''
    # Execute query
    db_ops.cursor.execute(query, (attendee_id[0],))
    results = db_ops.cursor.fetchall()

    # If no result, show error
    if not results:
        messagebox.showerror("Error", "You have no tickets to export.")
        return

    # Get file name
    filename = f"attendee_{attendee_id[0]}_tickets_export.csv"

    # Write to csv file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Event Name", "Date", "Venue", "Ticket Price"])
        writer.writerows(results)
    
    # Get file path
    import os
    file_path = os.path.abspath(f"attendee_{attendee_id[0]}_tickets_export.csv")
    print(f"CSV file saved at: {file_path}")

    # Notify user of successful completion
    messagebox.showinfo("Success", f"Tickets exported to '{filename}'.\n\n File Path: {file_path}")
    return


# Add a column to the event table to keep track of deleted events
# Rather than deleting from database entirely, we will mark them as deleted
def alter_event_table():
    # Add is_delted column to Events
    # Default to false
    query = '''
    ALTER TABLE Event
    ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE;
    '''
    db_ops.execute_query(query)


# Function to restore a deleted event
# Used just for testing database functionality
def restore_event(event_id):
    # Query to restore an event that was deleted
    # Sets is_deleted back to FALSE
    restore_query = '''
    UPDATE Event
    SET is_deleted = FALSE
    WHERE eventID = %s'''

    db_ops.cursor.execute(restore_query, (event_id,))
    db_ops.conn.commit()
    print('Event restored successfully')

# Create indexes
def create_index():
    # Create Index for Event name
    event_query = '''
    CREATE INDEX event_name_index ON Event(name)
    '''
    # Execute and commit
    db_ops.cursor.execute(event_query)
    db_ops.conn.commit()
    print('Event name index created.')

    # Create index for Artist name
    artist_query = '''
    CREATE INDEX artist_name_index ON Artist(name)
    '''
    # Execute and commit
    db_ops.cursor.execute(artist_query)
    db_ops.conn.commit()
    print('Artist name index created.')

    # Create index for Venue name
    venue_query = '''
    CREATE INDEX venue_name_index ON Venue(name);
    '''
    # Execute and commit
    db_ops.cursor.execute(venue_query)
    db_ops.conn.commit()
    print('Venue name index created.')


# Main Window
root = tk.Tk()
root.title("Music Events App")

# Call start screen function
startScreen()

# run main loop
root.mainloop()