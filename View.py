from tkinter import *
import psutil


class View(Tk):
    currentDisk = "C:\\"
    def __init__(self, model, controller):

        def showSystemInfo():
            info = Tk()
            info.title("About your system")
            info.geometry("300x150")
            info.resizable(0, 0)

            labels = ["Current disk: ", "Disk usage: "]
            values = []
            values.append(self.currentDisk)
            values.append(str(psutil.disk_usage(self.currentDisk).percent) + "%")
            for i in range (0, len(labels)):
                lbl = Label(info, text = labels[i])
                lbl.grid(row=i, column = 1, padx = 10, pady = 10)

            for i in range (0, len(values)):
                lbl = Label(info, text = values[i])
                lbl.grid(row=i, column = 2, padx = 10, pady = 10)

            info.mainloop()

        # Window block
        Tk.__init__(self)
        root = self
        root.geometry("500x500")
        root.title("FireManage: Your Files Are On Fire")
        root.resizable(0, 0)

        # Menu
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings")
        menubar.add_cascade(label="About system", command=showSystemInfo)

        self.config(menu=menubar)
        # MVC
        self.model = model
        self.controller = controller

        # Info dicts
        self.szCount = dict()
        self.fldCount = dict()
        self.flsCount = dict()

        # Current fields
        self.currentPathSize = StringVar()
        self.currentPath = StringVar()
        self.currentFoldersCount = StringVar()
        self.currentFilesCount = StringVar()
        self.currentFileName = ""

        # List Boxes
        self.foldersBox = Listbox(root, selectmode='browse', width=80, height=12)
        self.foldersBox.grid(row=3, column=1, padx=10, pady=(0, 0), columnspan=3)

        self.filesBox = Listbox(root, selectmode='browse', width=80, height=12)
        self.filesBox.grid(row=5, column=1, padx=10, pady=(0, 10), columnspan=3)

        # Elements
        btn = Button(self, text="Folders", width=68, height=1, command=controller.sortFolders)
        btn.grid(row=2, column=1, columnspan=3)

        btn = Button(self, text="Files", width=68, height=1, command=controller.sortFiles)
        btn.grid(row=4, column=1, columnspan=3)

        # Top frame
        self.frame = Frame(self, width=1000, height=20)
        self.frame.grid(row=1, column=1, columnspan=8)

        # Current path
        self.path = Label(self.frame, textvariable=self.currentPath, width = 30)
        self.path.place(x=10, y=0)

        self.filesCountlbl = Label(self.frame, text="files: ")
        self.filesCountlbl.place(x=230, y=0)
        self.filesCount = Label(self.frame, textvariable=self.currentFilesCount, justify=RIGHT)
        self.filesCount.place(x=260, y=0)

        self.foldersCountlbl = Label(self.frame, text="folders: ")
        self.foldersCountlbl.place(x=315, y=0)
        self.foldersCount = Label(self.frame, textvariable=self.currentFoldersCount, justify=RIGHT)
        self.foldersCount.place(x=360, y=0)
        self.txt = Label(self.frame, text="size: ")
        self.txt.place(x=407, y=0)
        self.lbl = Label(self.frame, textvariable=self.currentPathSize, justify=RIGHT)
        self.lbl.place(x=437, y=0)

        # Bottom frame
        self.fileFrame = Frame(self, width=1000, height=20)
        self.fileFrame.grid(row=6, column=1, columnspan=8)
        self.fileName = Text(self.fileFrame, height=1, width=60, wrap=WORD)
        self.fileName.place(x=10, y=0)

        # Binding
        self.foldersBox.bind('<Double-1>', lambda x: controller.moveInto(self.foldersBox.selection_get()))
        self.foldersBox.bind('<Return>', lambda x: controller.moveInto(self.foldersBox.selection_get()))
        self.foldersBox.bind('<BackSpace>', lambda x: controller.moveOut())
        self.foldersBox.bind('<<ListboxSelect>>', lambda x: self.printFileName("Выберите файл..."))
        self.filesBox.bind('<<ListboxSelect>>', lambda x: self.printFileName(self.filesBox.selection_get()))
        self.fileName.bind('<Return>',
                           lambda x: controller.renameFile(self.currentFileName, self.fileName.get('1.0', END)))
        # self.path.bind('<Return>', lambda x: controller.moveInto(self.path.get()))

        self.filesBox.bind('<Delete>', lambda x: controller.deleteFile(self.currentFileName))
        print("Start view")
        self.controller.setView(self)

    def printFileName(self, name):
        self.currentFileName = name
        self.fileName.delete('1.0', END)
        self.fileName.insert(END, name)
