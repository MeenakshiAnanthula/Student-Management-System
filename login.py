from tkinter import *
from PIL import ImageTk
from tkinter import messagebox

def login():
    if usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error','Fields cannot be empty')
    elif usernameEntry.get()=='Meenakshi' and passwordEntry.get()=='1234':
        messagebox.showinfo('Success', 'Welcome '+usernameEntry.get())
        window.destroy()
        import studentSystem
        
    else:
        messagebox.showerror('Error', 'Please enter correct credentials')
        
        





#for creating GUI Tk() class is useful
window=Tk() #create object for Tk class

window.geometry('1280x700+0+0') #set widthxheight of the window, set co-ords where the window should open

window.title('Login into Student Management System')

backgroundImage=ImageTk.PhotoImage(file='background.jpg') #getting image--only for jpg use imageTk

#create label and add image
bgLabel=Label(window,image=backgroundImage)

#place label on the screen
bgLabel.place(x=0,y=0)

#create frame inside window and add logo, form
loginFrame=Frame(window, bg='white')

#place login frame on window
loginFrame.place(x=400, y=150)

logoImage=PhotoImage(file='studentlogo.png')

logoLabel=Label(loginFrame, image=logoImage)

#place label on screen
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

usernameImage=PhotoImage(file='user.png')

usernameLabel=Label(loginFrame, image=usernameImage, text='Username', compound=LEFT,
                    font=('times new roman',20, 'bold'), bg='white')
usernameLabel.grid(row=1,column=0, pady=10, padx=20)

usernameEntry=Entry(loginFrame, font=('times new roman',20, 'bold'), bd=5, fg='blue4')

usernameEntry.grid(row=1, column=1, pady=10, padx=20)

passwordImage=PhotoImage(file='password.png')

passwordLabel=Label(loginFrame, image=passwordImage, text='Password', compound=LEFT,
                    font=('times new roman',20, 'bold'), bg='white')
passwordLabel.grid(row=2,column=0, pady=10, padx=20)

passwordEntry=Entry(loginFrame, font=('times new roman',20, 'bold'), bd=5, fg='blue4')

passwordEntry.grid(row=2, column=1, pady=10, padx=20)

loginButton=Button(loginFrame, text="Login",font=('times new roman',16, 'bold'), width=15,
                   fg='white',bg='cornflowerblue', activebackground='cornflowerblue',
                   activeforeground='white', cursor='hand2', command=login) #fg is font color
loginButton.grid(row=3, column=1)

window.resizable(False, False)

window.mainloop() #mainloop method keeps the window on loop so we can see it continuously
