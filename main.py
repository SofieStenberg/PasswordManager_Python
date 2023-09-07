from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
from passwordManager import *

class Window:
    def __init__(self, master):
        self.master = master
        self.master.title('Password Manager')
        self.master.configure(background='grey')
        self.master.geometry('1000x800')
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
        self.file.add_command(label='New database', command=self.createDb)
        self.file.add_command(label='Open...', command=self.openDb)
        self.file.add_command(label='Change Master Password', command=self.changeMasterPwd)
        # self.file.add_command(label='Generate password', command=self.generatePwd)

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

        

        
        

    #################################################################################################################
    ####                                          Class Functions                                                ####
    #################################################################################################################
    def addCredentials(self):
        # userInput = messagebox.askyesno(title='Generate password?', message='Do you want to autogenerate a password?')
        # pwd = ""
        # if(userInput):
        #     pwd = PasswordManager.generatePwd()

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

    def createDb(self):
        self.selectedFolder = filedialog.askdirectory()
        if (self.selectedFolder == ''):
            return
        self.dbName = simpledialog.askstring('Database name','Enter database name', parent=self.master)
        if(self.dbName == None):
            return
        self.masterPwd = simpledialog.askstring('Master Password','Enter master password', parent=self.master, show='*')
        if(self.masterPwd == None):
            return

        PasswordManager.createDatabase(self.selectedFolder + '/' + self.dbName + '.db', self.masterPwd)

    def openDb(self):
        self.selectedFile = filedialog.askopenfilename(initialdir=os.getcwd(), title='select a file', filetypes=(('database files','*.db'),))
        if(self.selectedFile == None):
            return
        self.userMasterPwd = simpledialog.askstring('Master Password','Enter master password', parent=self.master, show='*')
        if(self.masterPwd == None):
            return
        result = PasswordManager.openDatabase(self.selectedFile, self.userMasterPwd)
        if(result == 1):
            messagebox.showerror("Your master password is wrong!")

    def changeMasterPwd(self):
        pass

    def generatePwd(self):
        content = self.entryPassword.get()
        if(content != ""):
            self.entryPassword.delete(0, END)
        pwd = PasswordManager.generatePwd()
        self.entryPassword.insert(0, pwd)


def main():
    root = Tk()
    pwdManager = Window(root)
    root.mainloop()

if __name__ == "__main__": main()