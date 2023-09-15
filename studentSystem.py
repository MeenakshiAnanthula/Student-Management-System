
from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import pymysql
import pandas 

#functionality

def field_data(title, button_text,command):
    global idEntry,nameEntry,mobileEntry,emailEntry,addressEntry,genderEntry,dobEntry, displayWindow

    displayWindow=Toplevel()
    displayWindow.resizable(False, False)
    displayWindow.grab_set() #will not allow to click on other buttons while this window is open
    displayWindow.title(title)
    
    #add the entry fields
    idLabel=Label(displayWindow, text='Id', font=('times new roman',20, 'bold'))
    idLabel.grid(row=0,column=0,padx=30,pady=15, sticky=W)
    idEntry=Entry(displayWindow, font=('roman',15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, padx=10,pady=15)

    nameLabel=Label(displayWindow, text='Name', font=('times new roman',20, 'bold'))
    nameLabel.grid(row=1,column=0,padx=30,pady=15, sticky=W)
    nameEntry=Entry(displayWindow, font=('roman',15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, padx=10,pady=15)
    
    mobileLabel=Label(displayWindow, text='Mobile No.', font=('times new roman',20, 'bold'))
    mobileLabel.grid(row=2,column=0,padx=30,pady=15, sticky=W)
    mobileEntry=Entry(displayWindow, font=('roman',15, 'bold'), width=24)
    mobileEntry.grid(row=2, column=1, padx=10,pady=15)

    emailLabel=Label(displayWindow, text='Email', font=('times new roman',20, 'bold'))
    emailLabel.grid(row=3,column=0,padx=30,pady=15, sticky=W)
    emailEntry=Entry(displayWindow, font=('roman',15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, padx=10,pady=15)

    addressLabel=Label(displayWindow, text='Address', font=('times new roman',20, 'bold'))
    addressLabel.grid(row=4,column=0,padx=30,pady=15, sticky=W)
    addressEntry=Entry(displayWindow, font=('roman',15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, padx=10,pady=15)

    genderLabel=Label(displayWindow, text='Gender', font=('times new roman',20, 'bold'))
    genderLabel.grid(row=5,column=0,padx=30,pady=15, sticky=W)
    genderEntry=Entry(displayWindow, font=('roman',15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, padx=10,pady=15)

    dobLabel=Label(displayWindow, text='Date of Birth', font=('times new roman',20, 'bold'))
    dobLabel.grid(row=6,column=0,padx=30,pady=15, sticky=W)
    dobEntry=Entry(displayWindow, font=('roman',15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, padx=10,pady=15)

    studentButton=ttk.Button(displayWindow, text=button_text, command=command)
    studentButton.grid(row=7, columnspan=2, pady=15)

    if title=='Update Student':
        indexing=studentTreeview.focus()
        content=studentTreeview.item(indexing)
        print(indexing)
        print(content)
        listdata=content['values']
        idEntry.insert(0,listdata[0])
        nameEntry.insert(0,listdata[1])
        mobileEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])


def clock(): 
    global date, currentTime

    #To display date and time
    date=time.strftime('%d/%m/%Y')
    currentTime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date:{date}\nTime:{currentTime}')
    datetimeLabel.after(1000, clock) #to update the time every second

displayText=''
count=0

def slider(): #To display each letter one by one on a slider
    global displayText,count
    if count==len(s):
        count=0
        displayText=''
    displayText=displayText+s[count]
    sliderTextLabel.config(text=displayText)
    count+=1
    sliderTextLabel.after(300, slider)

def iexit():
    result=messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass
def export_data():
    fileurl=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studentTreeview.get_children()
    newlist=[]
    for index in indexing:
        content=studentTreeview.item(index)
        datalist=content['values']
        newlist.append(datalist)

        #using pandas dataframe we can print data in tabular form
    table=pandas.DataFrame(newlist,columns=['ID','Name','Mobile','Email', 'Address','Gender','D.O.B','Added Date','Added Time'])
    if fileurl!='':
        table.to_csv(fileurl,index=False)
        messagebox.showinfo('Success','Data is saved successfully')


def show_student():
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTreeview.delete(*studentTreeview.get_children())
    for data in fetched_data:
        studentTreeview.insert('',END, values=data)



def update_data():

    query='update student set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s where id=%s'
    mycursor.execute(query,(nameEntry.get(),mobileEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(),dobEntry.get(),date,currentTime,idEntry.get()))
    sqlConnection.commit()
    messagebox.showinfo('Success',f'Id: {idEntry.get()} is modified successfully',parent=displayWindow)
    displayWindow.destroy()

    show_student()

    

def delete_student():
    #select the row and store in indexing
    indexing=studentTreeview.focus()
    print(indexing)
    content=studentTreeview.item(indexing) #dictionary is returned, data is stored in values key
    print(content)
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,content_id)
    sqlConnection.commit()
    messagebox.showinfo('Deleted',f'Id: {content_id} is deleted successfully')

    #display updated records
    studentTreeview.delete(*studentTreeview.get_children())
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        studentTreeview.insert('',END, values=data)


def search_data():
    query='select * from student where id=%s or name=%s or email=%s or mobile=%s or gender=%s or address=%s or dob=%s'
    mycursor.execute(query,(idEntry.get(),nameEntry.get(),emailEntry.get(),
                            mobileEntry.get(),genderEntry.get(),addressEntry.get(), dobEntry.get()))
    studentTreeview.delete(*studentTreeview.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        studentTreeview.insert('',END,values=data)


def add_data():

    if (idEntry.get()=='' or nameEntry.get()=='' or mobileEntry.get()=='' or emailEntry.get()==''
        or addressEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()==''):
        messagebox.showerror('Error', 'All fields are required!', parent=displayWindow)
    
    else:
        
        try:
            query='insert into student values(%s, %s, %s, %s, %s, %s, %s, %s,%s)'
            mycursor.execute(query, (idEntry.get(),nameEntry.get(), mobileEntry.get(), emailEntry.get(),
                                    addressEntry.get(), genderEntry.get(), dobEntry.get(),
                                    date, currentTime) )
            sqlConnection.commit()
            
            result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clear the form?',parent=displayWindow)
            #clear all the fields
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                mobileEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error','ID cannot be duplicated', parent=displayWindow)
            return

        query='select * from student'
        mycursor.execute(query)
        fetchedData=mycursor.fetchall()
        studentTreeview.delete(*studentTreeview.get_children())
        for data in fetchedData:
            dataList=list(data)
            studentTreeview.insert('',END,values=dataList)
    
   

def connect_database():
    
    #connecting to database
    def connect():
        global mycursor,sqlConnection
        try:
            sqlConnection=pymysql.connect(host='localhost',user='root',password='Vihaan@5848')
            #sqlConnection=pymysql.connect(host=hostEntry.get(),user=usernameEntry.get(),password=passwordEntry.get())
            mycursor=sqlConnection.cursor()
            
        except:
            messagebox.showerror('Error', 'Invalid Details',parent=connectWindow)
            return
        
        try:
            query='create database studentmanagementsystem'
            mycursor.execute(query)
            query='use studentmanagementsystem'
            mycursor.execute(query)
            query='create table student(id int not null primary key,name varchar(30),mobile varchar(10),email varchar(30),'\
                    'address varchar(100),gender varchar(10),dob varchar(20),date varchar(50),time varchar(50))'
            mycursor.execute(query)
        except:
            query='use studentmanagementsystem'
            mycursor.execute(query)
        
        messagebox.showinfo('Success','Database Connection is Successful',parent=connectWindow)
        connectWindow.destroy()
        
        addStudentButton.config(state=NORMAL)
        searchStudentButton.config(state=NORMAL)
        updateStudentButton.config(state=NORMAL)
        deleteStudentButton.config(state=NORMAL)
        showStudentButton.config(state=NORMAL)
        exportDataButton.config(state=NORMAL)
            
    
    
    connectWindow=Toplevel()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)

    #create fields
    hostnameLabel=Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0,padx=20)

    hostEntry=Entry(connectWindow, font=('roman', 15, 'bold'), bd=2) #bd=border
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel=Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0,padx=20)

    usernameEntry=Entry(connectWindow, font=('roman', 15, 'bold'), bd=2) #bd=border
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel=Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0,padx=20)

    passwordEntry=Entry(connectWindow, font=('roman', 15, 'bold'), bd=2) #bd=border
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=3, columnspan=2) #columnspan=2 takes 2col-spaces, appears at center

#UI part
root=ttkthemes.ThemedTk()

root.get_themes()
root.set_theme('radiance')

root.geometry('1174x680+0+0')
root.resizable(False,False)

root.title('Student Management System')

datetimeLabel=Label(root, font=('times new roman',18,'bold'))
datetimeLabel.place(x=5, y=5)
clock()

#Slider Text creation
s='Student Management System'
sliderTextLabel=Label(root,font=('arial',28,'italic bold'), width=30)
sliderTextLabel.place(x=200,y=0)
slider()

#connect to database button
connectButton=ttk.Button(root, text='Connect Database',command=connect_database)
connectButton.place(x=980, y=0)

#create left frame

leftFrame=Frame(root)
leftFrame.place(x=50,y=80, width=300, height=600)

logo_image=PhotoImage(file='students.png')
logo_Label=Label(leftFrame, image=logo_image)
logo_Label.grid(row=0,column=0)

#Add buttons

addStudentButton=ttk.Button(leftFrame,text='Add Student',width=25,state=DISABLED,command=lambda:field_data('Add Student','Add', add_data))
addStudentButton.grid(row=1, column=0, pady=20)

searchStudentButton=ttk.Button(leftFrame,text='Search Student',width=25,state=DISABLED,command=lambda: field_data('Search Student', 'Search', search_data))
searchStudentButton.grid(row=2, column=0, pady=20)

deleteStudentButton=ttk.Button(leftFrame,text='Delete Student',width=25,state=DISABLED,command=delete_student)
deleteStudentButton.grid(row=3, column=0, pady=20)

updateStudentButton=ttk.Button(leftFrame,text='Update Student',width=25,state=DISABLED,command=lambda: field_data('Update Student','Update', update_data))
updateStudentButton.grid(row=4, column=0, pady=20)

showStudentButton=ttk.Button(leftFrame,text='Show Student',width=25,state=DISABLED,command=show_student)
showStudentButton.grid(row=5, column=0, pady=20)


exportDataButton=ttk.Button(leftFrame,text='Export Data',width=25,state=DISABLED,command=export_data)
exportDataButton.grid(row=6, column=0, pady=20)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7, column=0, pady=20)

#create right frame
rightFrame=Frame(root)
rightFrame.place(x=350,y=80, width=820, height=600)

#create scrollbar
scrollBarX=Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame, orient=VERTICAL)

studentTreeview=ttk.Treeview(rightFrame, columns=('ID','Name','Mobile No', 'Email', 'Address',
                                  'Gender', 'D.O.B', 'Added Date','Added Time'),
                                  xscrollcommand=scrollBarX.set,
                                  yscrollcommand=scrollBarY.set)

#config the scrollbar with studentTreeview
scrollBarX.config(command=studentTreeview.xview)
scrollBarY.config(command=studentTreeview.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)
studentTreeview.pack(fill=BOTH,expand=1) #to place data use pack to just place data

studentTreeview.heading('ID', text='ID')
studentTreeview.heading('Name', text='Name')
studentTreeview.heading('Mobile No', text='Mobile No')
studentTreeview.heading('Email', text='Email')
studentTreeview.heading('Address', text='Address')
studentTreeview.heading('Gender', text='Gender')
studentTreeview.heading('D.O.B', text='D.O.B')
studentTreeview.heading('Added Date', text='Added Date')
studentTreeview.heading('Added Time', text='Added Time')

studentTreeview.column('ID', width=50,anchor=CENTER)
studentTreeview.column('Name', width=300,anchor=CENTER)
studentTreeview.column('Mobile No', width=200,anchor=CENTER)
studentTreeview.column('Email', width=300,anchor=CENTER)
studentTreeview.column('Address', width=300,anchor=CENTER)
studentTreeview.column('Gender', width=100,anchor=CENTER)
studentTreeview.column('D.O.B', width=200,anchor=CENTER)
studentTreeview.column('Added Date', width=200,anchor=CENTER)
studentTreeview.column('Added Time', width=200,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), 
                background='white', fieldbackground='white')
style.configure('Treeview.Heading', font=('arial', 14, 'bold'))

studentTreeview.config(show='headings')

root.mainloop()