Brooke England, Raneem Rahman
2429052, 2391103
brengland@chapman.edu, rrahman@chapman.edu
CPSC 408-01
Final Project

INTRUCTIONS:
- Start the program with python3 musicApp.py
- A new window will pop up with the application
- Create an account as an Attendee or an Organizer 
- Sign in with your previous login information 
- As an Attendee, you can log in and explore events, artists, venues, etc
- As an Organizer, you can log in and view venue capacity and schedule your artists/events
- Note: The csv files for tickets and events will appear in your current directory.
A file path will be displayed. Go to your files to view and open the csv file

References:
1. The following soruce was used to learn how to use Tkinter for our front end in python
https://www.geeksforgeeks.org/python-gui-tkinter/


2. Source: Chatgpt https://chatgpt.com/c/682a5f39-29ec-8003-9c56-991decad2b2b
Prompt: Why is tkinter not clearing the current window after clicking a button?

Based on the response we created a clear_window function to be called to clear the tkinter window
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


5. The following source was used for user text entry via Tkinter
https://www.geeksforgeeks.org/python-tkinter-entry-widget/


6. The following was used for creating a message box in tkinter
https://docs.python.org/3/library/tkinter.messagebox.html

- Used messagebox.showerror() to notify user when they made an error such as missing values:
tkinter.messagebox.showerror(title=None, message=None, **options)
Creates and displays an error message box with the specified title and message.

- Used messagebox.showinfo() to notify user when task has been completed:
tkinter.messagebox.showinfo(title=None, message=None, **options)
Creates and displays an information message box with the specified title and message.


7. Chatgpt https://chatgpt.com/c/682a5fe1-9148-8003-a4b4-ca6f3a1df378
The following was used to debug an error in the get_account_type function
Prompt: Why am I being directed striaght to the organizer login and not showing option buttons?
    #Ask User if they are an attendee or an organizer
    tk.Label(root, text = "Select Account Type:").pack()

    # Create attendee button
    # if clicked, will navigate to attendee login
    tk.Button(root, text = "Attendee", command = login("Attendee")).pack()

    # Create Organizer Button
    # If clicked, will navigate to organizer login
    tk.Button(root, text = "Organizer", command = login("Organizer")).pack()

Response:
command = login("Attendee")
…it calls the function right away and assigns the result (usually None) as the command.

To fix it, use a lambda to defer the call:
tk.Label(root, text="Select Account Type:").pack()

    # Use lambda to pass parameters correctly
    tk.Button(root, text="Attendee", command=lambda: login("Attendee")).pack()
    tk.Button(root, text="Organizer", command=lambda: login("Organizer")).pack()


8. The following was used to learn how to print a file path for our csv output
https://www.tutorialspoint.com/How-to-print-full-path-of-current-file-s-directory-in-Python


9. Used to help implement soft deletion logic
https://stackoverflow.com/questions/5020568/soft-delete-best-practices-php-mysql



10. Used this t help implement the importing of a CSV file
https://www.geeksforgeeks.org/writing-csv-files-in-python/

11. I had a question about strings in Tkinter so I used this to look at examples. I used StringVar when creating the drop down to select events
https://stackoverflow.com/questions/69738637/tkinter-stringvar 

12. I just used this to read more about f-strings in python, there wasn't a specific line I applied this on
https://www.geeksforgeeks.org/formatted-string-literals-f-strings-python/ 

13. Referenced this to learn how to implement OptionMenu Widget in Tkinter
https://www.geeksforgeeks.org/tkinter-optionmenu-widget/

14. Referenced this for Tkinter pack() method
https://www.tutorialspoint.com/python/tk_pack.htm 

15. Refrenced to read up on exception as e
https://rollbar.com/blog/what-is-except-exception-as-e-in-python/

16. Referenced to read the defference between except and exception as e
https://stackoverflow.com/questions/18982610difference-between-except-and-except-exception-as-e

17. Referenced this to read about the commit() and rollback() methods
https://www.geeksforgeeks.org/commit-rollback-operation-in-python/

18. Looked up ways to present the output of a program 
https://docs.python.org/3/tutorial/inputoutput.html

19. Referenced this for Tkinter button commands
https://www.tutorialspoint.com/tkinter-button-commands-with-lambda-in-python 

20. Referenced to better understand how the Tkinter buttons work
https://stackoverflow.com/questions/70406400/understanding-python-lambda-behavior-with-tkinter-button 