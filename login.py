# from tkinter import *   # Provides tools to create the GUI elements.
# from tkinter import messagebox
# from PIL import ImageTk   #python image library import jpg image
#
# def login():
#   if usernameEntry.get()=='' or passwordEntry.get()=='':
#        messagebox.showerror('Error','Please fill the required fields')
#   elif usernameEntry.get()=='Isha' and passwordEntry.get()=='13':
#           messagebox.showinfo('Success','welcome')
#           window.destroy()      #to destroy the login window
#           import sms
#
#   else:
#        messagebox.showerror('Error', 'Please Enter correct credentials')
#
# window=Tk()                     # tk class and window id object of class
#
# window.geometry('1280x800+0+0')                #to add width and height to window
# window.title('Login system of employee Management System')
#
# window.resizable(False,False)
#
# backgroundImage=ImageTk.PhotoImage(file='bg.jpg')        #put image in jpg
#
# bgLabel=Label(window,image=backgroundImage)
# bgLabel.place(x=0,y=0)          #to place our image on window
#
# loginFrame=Frame(window,bg='white')      #to create login frame
# loginFrame.place(x=400,y=150)
#
# logoImage=PhotoImage(file='logo.png')         #if it is in png then there is no need to use ImageTk
#
# logoLabel=Label(loginFrame,image=logoImage)
# logoLabel.grid(row=0,column=0,columnspan=2,pady=10)
# usernameImage=PhotoImage(file='user.png')
# usernameLabel=Label(loginFrame,image=usernameImage,text='Username',compound=LEFT,font=('times new roman',20,'bold'),bg='white')
# usernameLabel.grid(row=1,column=0,pady=10,padx=20)
#
# usernameEntry=Entry(loginFrame,font=('times new roman',20,'bold'),bd=5)
# usernameEntry.grid(row=1,column=1,pady=10,padx=20)
#
#
# passwordImage=PhotoImage(file='password.png')
# passwordLabel=Label(loginFrame,image=passwordImage,text='Password',compound=LEFT,font=('times new roman',20,'bold'),bg='white')
# passwordLabel.grid(row=2,column=0,pady=10,padx=20)
#
# passwordEntry=Entry(loginFrame,font=('times new roman',20,'bold'),bd=5)
# passwordEntry.grid(row=2,column=1,pady=10,padx=20)
# loginButton=Button(loginFrame,text='Login',font=('times new roman',15,'bold'),width=15,fg='white',bg='cornflowerblue',activebackground='cornflowerblue',
#                                  activeforeground='white',cursor='hand2',command=login)
# loginButton.grid(row=3,column=1,pady=10)
# window.mainloop()

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import sqlite3  # Import the SQLite module


# Function to create the SQLite database and users table
def create_db():
    conn = sqlite3.connect('users.db')  # Connect to the SQLite database
    cursor = conn.cursor()

    # Create a table if it doesn't exist already
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Insert a sample user (Only for testing, remove in production)
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('Isha', '13'))

    conn.commit()
    conn.close()


# Function to validate the login credentials
def login():
    username = usernameEntry.get()
    password = passwordEntry.get()

    if username == '' or password == '':
        messagebox.showerror('Error', 'Please fill the required fields')
    else:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Query to check if the username and password match
        # query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        # cursor.execute(query)    #### SQL Injection

        query="select * from users where username=? and password=?"
        cursor.execute(query ,(username,password))

        result = cursor.fetchone()

        if result:
            messagebox.showinfo('Success', 'Welcome')
            window.destroy()  # Destroy the login window
            import sms  # Replace with the actual module to be imported after successful login
        else:
            messagebox.showerror('Error', 'Please enter correct credentials')

        conn.close()


# Create the database and table
create_db()

# Tkinter GUI Setup
window = Tk()
window.geometry('1280x800+0+0')
window.title('Login System of Employee Management System')
window.resizable(False, False)

backgroundImage = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(window, image=backgroundImage)
bgLabel.place(x=0, y=0)

loginFrame = Frame(window, bg='white')
loginFrame.place(x=400, y=150)

logoImage = PhotoImage(file='logo.png')
logoLabel = Label(loginFrame, image=logoImage)
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

usernameImage = PhotoImage(file='user.png')
usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='white')
usernameLabel.grid(row=1, column=0, pady=10, padx=20)

usernameEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5)
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

passwordImage = PhotoImage(file='password.png')
passwordLabel = Label(loginFrame, image=passwordImage, text='Password', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='white')
passwordLabel.grid(row=2, column=0, pady=10, padx=20)

passwordEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5,
                      )  # Mask the password with asterisks show='*'
passwordEntry.grid(row=2, column=1, pady=10, padx=20)

loginButton = Button(loginFrame, text='Login', font=('times new roman', 15, 'bold'), width=15, fg='white',
                     bg='cornflowerblue',
                     activebackground='cornflowerblue', activeforeground='white', cursor='hand2', command=login)
loginButton.grid(row=3, column=1, pady=10)

window.mainloop()
