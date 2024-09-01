from tkinter import *     # help us to create graphical user interface
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql    #Used to interact with MySQL databases.
import pandas         # For data manipulation and export to CSV.


def iexit():
    result = messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = employeeTable.get_children()
    newlist = []
    for index in indexing:
        content = employeeTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pandas.DataFrame(newlist,columns=['Id', 'Name', 'Role', 'Mobile_No', 'Email', 'Status'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success','Data is saved successfully')


def toplevel_data(title,button_text,command):
    global idEntry,nameEntry,roleEntry,mobileEntry,emailEntry,statusEntry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(0,0)
    idLabel = Label(screen, text='Id', font=('times new roman', 13, 'bold'),fg='red')
    idLabel.grid(row=0, column=0, padx=30, pady=15)
    idEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 13, 'bold'),fg='red')
    nameLabel.grid(row=1, column=0, padx=30, pady=15)
    nameEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    roleLabel = Label(screen, text='Role', font=('times new roman', 13, 'bold'), fg='red')
    roleLabel.grid(row=2, column=0, padx=30, pady=15)
    roleEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    roleEntry.grid(row=2, column=1, pady=15, padx=10)

    mobileLabel = Label(screen, text='Mobile_No', font=('times new roman', 13, 'bold'),fg='red')
    mobileLabel.grid(row=3, column=0, padx=30, pady=15)
    mobileEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    mobileEntry.grid(row=3, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 13, 'bold'), fg='red')
    emailLabel.grid(row=4, column=0, padx=30, pady=15)
    emailEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    emailEntry.grid(row=4, column=1, pady=15, padx=10)

    statusLabel = Label(screen, text='Status', font=('times new roman', 13, 'bold'), fg='red')
    statusLabel.grid(row=5, column=0, padx=30, pady=15)
    statusEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    statusEntry.grid(row=5, column=1, pady=15, padx=10)

    employee_button = ttk.Button(screen, text=button_text, command=command)
    employee_button.grid(row=7, columnspan=2, pady=15)



    if title=='Update employee':
        indexing = employeeTable.focus()

        content = employeeTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        roleEntry.insert(0, listdata[2])
        mobileEntry.insert(0, listdata[3])
        emailEntry.insert(0, listdata[4])
        statusEntry.insert(0, listdata[5])





def update_data():
    query = 'update employee set name=%s, role=%s, mobile_no=%s, email=%s, status=%s where id=%s'
    mycursor.execute(query, (nameEntry.get(), roleEntry.get(), mobileEntry.get(), emailEntry.get(), statusEntry.get(), idEntry.get()))
    con.commit()
    messagebox.showinfo('Success', f'Id {idEntry.get()} is modified successfully', parent=screen)
    screen.destroy()
    show_employee()







def show_employee():
    query = 'select * from employee'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    employeeTable.delete(*employeeTable.get_children())
    for data in fetched_data:
        employeeTable.insert('', END, values=data)



def delete_employee():
    indexing=employeeTable.focus()
    print(indexing)
    content=employeeTable.item(indexing)
    content_id=content['values'][0]
    query='delete from employee where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f' Id  {content_id} is deleted successfully')
    query='select * from employee'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    employeeTable.delete(*employeeTable.get_children())
    for data in fetched_data:
        employeeTable.insert('', END, values=data)




def search_data():
    query='select *from employee where id=%s or name=%s'
    mycursor.execute(query,(idEntry.get(),nameEntry.get()))
    employeeTable.delete(*employeeTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        employeeTable.insert('', END, values=data)






def add_data():
    if idEntry.get() == '' or nameEntry.get() == '' or roleEntry.get() == '' or mobileEntry.get() == '' or emailEntry.get() == '' or statusEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required', parent=screen)
    else:
        try:
            query = 'insert into employee values(%s, %s, %s, %s, %s, %s)'
            mycursor.execute(query, (idEntry.get(), nameEntry.get(), roleEntry.get(), mobileEntry.get(), emailEntry.get(), statusEntry.get()))
            con.commit()
            result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clean the form?', parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                roleEntry.delete(0, END)
                mobileEntry.delete(0, END)
                emailEntry.delete(0, END)
                statusEntry.delete(0, END)
            else:
                pass
            show_employee()
        except:
            messagebox.showerror('Error', 'Id cannot be repeated', parent=screen)





def connect_database():
    def connect():
        global mycursor, con
        try:
            con=pymysql.connect(host=hostEntry.get(), user=UsernameEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()      # variable to excute command
            messagebox.showinfo('Success','Database Connection is successfully',parent=connectWindow)

        except:
            messagebox.showerror('Error','Invalid Details',parent=connectWindow)
            return
        try:
            query='create database employeemanagementsystem'
            mycursor.execute(query)
            query='use employeemanagementsystem'
            mycursor.execute(query)
            query='create table employee(Id int not null primary key,Name varchar(30),Role varchar(12), Mobile_No varchar(10),Email varchar(12),Status varchar(30))'
            mycursor.execute(query)
        except:
            query = 'use employeemanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection is successfully', parent=connectWindow)
        connectWindow.destroy()        # to discoonect connect window
        addemployeeButton.config(state=NORMAL)
        searchemployeeButton.config(state=NORMAL)
        deleteemployeeButton.config(state=NORMAL)
        updateemployeeButton.config(state=NORMAL)
        showemployeeButton.config(state=NORMAL)
        exportemployeeButton.config(state=NORMAL)
        exitButton.config(state=NORMAL)


    connectWindow = Toplevel()
    connectWindow.grab_set()     # graph set is used to first close the top window then only it will able to close another window
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Databse Connection')
    connectWindow.resizable(0,0)

    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',23,  'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=(' roman',13,' bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    UsernameLabel = Label(connectWindow, text='User name', font=('arial', 23, ' bold'))
    UsernameLabel.grid(row=1, column=0,padx=20)

    UsernameEntry = Entry(connectWindow, font=(' roman', 13, ' bold'), bd=2)
    UsernameEntry.grid(row=1, column=1, padx=40,pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 23, ' bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=(' roman', 13, ' bold'), bd=2)       # show='*'
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='Connect',command=connect)
    connectButton.grid(row=3,columnspan=2)


count=0
text=''
def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)
def clock():
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f' Date:{date}\nTime:{currenttime}')
    datetimeLabel.after(1000,clock)
root=ttkthemes.ThemedTk()

root.get_themes()

root.set_theme('elegance')
root.geometry('1174x680+0+0')
root.resizable(0,0)
root.title('employee Management System')

datetimeLabel=Label(root,font=('times new roman',18,'bold'))    #to
datetimeLabel.place(x=5,y=5)
clock()
s='employee Management System'
sliderLabel=Label(root,font=('times new roman',23,'italic bold'),width=30)
sliderLabel.place(x=200,y=0)
slider()

connectButton=ttk.Button(root,text='Connect database',command=connect_database)   #ttk to apply theme
connectButton.place(x=980,y=0)
leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

logo_image=PhotoImage(file='student.png')
logo_Label=Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)


addemployeeButton=ttk.Button(leftFrame,text='Add employee',width=25,state=DISABLED,command=lambda :toplevel_data('Add employee','Add ',add_data))
addemployeeButton.grid(row=1,column=0,pady=20)

searchemployeeButton=ttk.Button(leftFrame,text='Search employee',width=25,state=DISABLED,command=lambda :toplevel_data('Search employee','Search',search_data))
searchemployeeButton.grid(row=2,column=0,pady=20)

deleteemployeeButton=ttk.Button(leftFrame,text='Delete employee',width=25,state=DISABLED,command=delete_employee)
deleteemployeeButton.grid(row=3,column=0,pady=20)

updateemployeeButton=ttk.Button(leftFrame,text='Update employee',width=25,state=DISABLED,command=lambda :toplevel_data('Update employee','Update',update_data))
updateemployeeButton.grid(row=4,column=0,pady=20)

showemployeeButton=ttk.Button(leftFrame,text='Show employee',width=25,state=DISABLED,command=show_employee)
showemployeeButton.grid(row=5,column=0,pady=20)

exportemployeeButton=ttk.Button(leftFrame,text='Export Data',width=25,state=DISABLED,command=export_data)
exportemployeeButton.grid(row=6,column=0,pady=20)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=20)

rightFrame=Frame(root)
rightFrame.place(x=350,y=80,width=820,height=600)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

employeeTable=ttk.Treeview(rightFrame,columns=('Id','Name','Role','Mobile_No','Email','Status'),
                          xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)    #scrollbar to see all colum in rightframe
scrollBarX.config(command=employeeTable.xview)
scrollBarY.config(command=employeeTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)
employeeTable.pack(fill=BOTH,expand=1)

employeeTable.heading('Id',text='Id')
employeeTable.heading('Name',text='Name')
employeeTable.heading('Role',text='Role')
employeeTable.heading('Mobile_No',text='Mobile_No')
employeeTable.heading('Email',text='Email')
employeeTable.heading('Status',text='Status')

employeeTable.column('Id',width=200,anchor=CENTER)
employeeTable.column('Name',width=200,anchor=CENTER)
employeeTable.column('Role',width=200,anchor=CENTER)
employeeTable.column('Mobile_No',width=200,anchor=CENTER)
employeeTable.column('Email',width=200,anchor=CENTER)
employeeTable.column('Status',width=200,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview',rowheight=40,font=('arial',10,'bold'),background='white',fieldbackground='white')
style.configure('Treeview.Heading',font=('arial',10,'bold'))
employeeTable.config(show='headings')

root.mainloop()