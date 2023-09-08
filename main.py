from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import sqlite3
from passwordManager import *

class Window:
    def __init__(self, master):
        self.master = master
        self.master.title('Password Manager')
        self.master.configure(background='grey')
        self.master.geometry('800x500')
        self.master.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure('TFrame', background='grey')
        self.style.configure('TLabel', background='grey')
        self.style.configure('TButton', background='grey')

        # Menu bar
        self.master.option_add('*tearOff', False)
        self.menubar = Menu(self.master)
        self.master.configure(menu=self.menubar)
        self.file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.file, label='File')
        self.file.add_command(label='New Database', command=self.createDb)
        self.file.add_command(label='Open...', command=self.openDb)
        self.file.add_command(label='Change Master Password', command=self.changeMasterPwd)
        self.file.add_command(label='Empty Database', command=self.cleanDatabase)

        self.frameManage = ttk.Frame(self.master)
        self.frameManage.pack(side=TOP, anchor=NW)
        # Label and entry for username
        ttk.Label(self.frameManage, text='Username', font=('Times New Roman', 12)).grid(row=0, column=0, sticky=W)
        self.entryUsername = ttk.Entry(self.frameManage, width=15, font=('Times New Roman', 12))
        self.entryUsername.grid(row=1, column=0, padx=5)
        # Label and entry for password
        ttk.Label(self.frameManage, text='Password', font=('Times New Roman', 12)).grid(row=0, column=1, sticky=W)
        self.entryPassword = ttk.Entry(self.frameManage, width=15, font=('Times New Roman', 12))
        self.entryPassword.grid(row=1, column=1, padx=5)
        # Label and entry for description
        ttk.Label(self.frameManage, text='Description', font=('Times New Roman', 12)).grid(row=0, column=2, sticky=W)
        self.entryDescription = ttk.Entry(self.frameManage, width=30, font=('Times New Roman', 12))
        self.entryDescription.grid(row=1, column=2, padx=5)
        # button to add credentials
        ttk.Button(self.frameManage, text='Add credentials', command=self.addCredentials).grid(row=1, column=3, padx=5)
        # button to auto generate pwd
        ttk.Button(self.frameManage, text='Auto generate password', command=self.generatePwd).grid(row=1, column=4, padx=5)


        self.displayTree = ttk.Treeview(self.master, column=('c1', 'c2', 'c3', 'c4'), show='headings', selectmode='browse')
        self.displayTree.column('#1', anchor=CENTER)
        self.displayTree.heading('#1', text='ID')
        self.displayTree.column('#2', anchor=CENTER)
        self.displayTree.heading('#2', text='Username')
        self.displayTree.column('#3', anchor=CENTER)
        self.displayTree.heading('#3', text='Description')
        self.displayTree.column('#4', anchor=CENTER)
        self.displayTree.heading('#4', text='Password')
        self.displayTree.bind('<ButtonRelease-1>', self.selectItem)
        self.displayTree.pack( pady=50, padx=15)
        
        # self.scrollb = ttk.Scrollbar(self.master, orient='vertical', command=self.displayTree.yview)
        # self.scrollb.pack(side='right', fill='x')
        # self.displayTree.configure(xscrollcommand= self.scrollb.set)

        
        
        

    #################################################################################################################
    ####                                          Class Functions                                                ####
    #################################################################################################################
    def addCredentials(self):
        username = self.entryUsername.get()
        self.entryUsername.delete(0, END)
        pwd = self.entryPassword.get()
        self.entryPassword.delete(0, END)
        description = self.entryDescription.get()
        self.entryDescription.delete(0, END)
        if(username == "" or pwd == ""):
            messagebox.showwarning("Lack of input", "Username or password can not be empty")
            return
        PasswordManager.addCredentials(username, pwd, description)

        self.displayTreeview()

    def createDb(self):
        selectedFolder = filedialog.askdirectory()
        if (selectedFolder == ''):
            return
        dbName = simpledialog.askstring('Database name','Enter database name', parent=self.master)
        if(dbName == None):
            return
        masterPwd = simpledialog.askstring('Master Password','Enter master password', parent=self.master, show='*')
        if(masterPwd == None):
            return

        PasswordManager.createDatabase(selectedFolder + '/' + dbName + '.db', masterPwd)

        self.displayTreeview()

    def openDb(self):
        selectedFile = filedialog.askopenfilename(initialdir=os.getcwd(), title='select a file', filetypes=(('database files','*.db'),))
        if(selectedFile == None):
            return
        userMasterPwd = simpledialog.askstring('Master Password','Enter master password', parent=self.master, show='*')
        if(userMasterPwd == None):
            return
        result = PasswordManager.openDatabase(selectedFile, userMasterPwd)
        if(result == 1):
            messagebox.showerror("Your master password is wrong!")

        self.displayTreeview()

    def changeMasterPwd(self):
        currentMasterPwd = simpledialog.askstring('Current Master Password','Enter the current master password', parent=self.master, show='*')
        if(currentMasterPwd == None):
            messagebox.showerror("You must enter the current master password")
            return
        if(not PasswordManager.controlMasterPwd(currentMasterPwd)):
           messagebox.showerror("Your master password is wrong!")
           return
        newMasterPwd = simpledialog.askstring('New Master Password','Enter the new master password', parent=self.master, show='*')
        if(newMasterPwd == None):
            messagebox.showerror("The new password cannot be empty")
            return
        PasswordManager.changeMasterPwd(newMasterPwd)

        self.displayTreeview()

    def generatePwd(self):
        content = self.entryPassword.get()
        if(content != ""):
            self.entryPassword.delete(0, END)
        pwd = PasswordManager.generatePwd()
        self.entryPassword.insert(0, pwd)

    def displayTreeview(self):
        self.displayTree.delete(*self.displayTree.get_children())
        path = PasswordManager.extractDatabasePath()
        connection = None
        try:
            connection = sqlite3.connect(path)
        except Error as e:
            print(e)
        
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, description FROM Passwords")
        entries = cursor.fetchall()
        for entry in entries:
            self.displayTree.insert('', END, values=entry)
        connection.close()

    def cleanDatabase(self):
        PasswordManager.clearDatabase()
        self.displayTreeview()

    def selectItem(self, event):
        currentItem = self.displayTree.item(self.displayTree.focus())

        path = PasswordManager.extractDatabasePath()
        connection = None
        try:
            connection = sqlite3.connect(path)
        except Error as e:
            print(e)
        
        cursor = connection.cursor()
        sqlStatement = "SELECT id, username, description, password FROM Passwords WHERE id = ?"
        id = currentItem['values'][0]
        cursor.execute(sqlStatement, (id,))
        entries = cursor.fetchall()
        decryptedPwd = Ceasar.decrypt(entries[0][3], PasswordManager.extractMasterHash())
        self.displayTree.insert('', int(id), values=(entries[0][0], entries[0][1], entries[0][2], decryptedPwd))




def main():
    root = Tk()
    pwdManager = Window(root)
    root.mainloop()

if __name__ == "__main__": main()