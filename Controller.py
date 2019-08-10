from threading import Thread
from tkinter import *
from tkinter import messagebox
import time
import os

class Size(Thread):

    def __init__(self, model, view):
        Thread.__init__(self)
        self.model = model
        self.view = view

    def run(self):
            fld = 0
            bytes = 0
            fls = 0
            path = self.model.getPath()
            self.view.flsCount[path] = 0
            for dirpath, dirnames, filenames in os.walk(path):
                fld += 1
                size = str(bytes / 1024 / 1024 / 1024)
                if (size.find("e-") != -1):
                    size = "0.0"
                result = size.split(".")[0] + "." + str(size.split(".")[1])[:2] + " Гб"
                self.view.szCount[path] = result
                self.view.fldCount[path] = fld - 1
                if (path == self.model.getPath()):
                    self.view.currentPathSize.set(self.view.szCount.get(path))
                    self.view.currentFoldersCount.set(self.view.fldCount.get(path))
                    self.view.currentFilesCount.set(self.view.flsCount.get(path))
                    self.view.update()
                    time.sleep(0.02)
                fp = ""
                for f in filenames:
                    fls += 1
                    self.view.flsCount[path] = fls - 1
                    fp = os.path.join(dirpath, f)
                    try:
                        bytes += os.path.getsize(fp)
                    except:
                        print("Обнаружен битый файл: " + fp)
            self.view.update()

class Controller:

    def __init__(self, model):
        self._selectionIndex = 0
        self._sortingFiles = False
        self._sortingFolders = False
        self.model = model
        print("Init controller")

    def setViewCategory(self):
        self.view.currentPath.set(self.model.getPath())

    def setView(self, view):
        self.view = view
        self.setViewCategory()
        self.updateFolders()
        self.updateFiles()
        self.calculateFolderSize()

    def moveInto(self, path):
        self.selectionIndex = self.model.getFolders().index(self.view.foldersBox.selection_get())
        self.model.stepInto(path)
        self.setViewCategory()
        self.updateFolders()
        self.updateFiles()
        self.calculateFolderSize()


    def moveOut(self):
        self.model.stepBack()
        self.setViewCategory()
        self.updateFolders()
        self.updateFiles()
        self.calculateFolderSize()
        self.view.foldersBox.selection_set(self.selectionIndex)

    def calculateFolderSize(self):
        path = self.model.getPath()
        if (not self.view.szCount.keys().__contains__(path)):
            self.view.szCount[path] = StringVar()
            self.view.szCount[path] = StringVar()
            self.view.fldCount[path] = StringVar()
            size = Size(self.model, self.view)
            size.start()
        self.view.currentPathSize.set(self.view.szCount.get(self.model.getPath()))
        self.view.currentFoldersCount.set(self.view.fldCount.get(path))
        self.view.currentFilesCount.set(self.view.flsCount.get(path))

    def updateFolders(self):
        self.view.foldersBox.delete(0, END)
        folders = self.model.getFolders()
        if(self._sortingFolders == True):
            folders = reversed(folders)
        for fd in folders:
            self.view.foldersBox.insert(END, fd)
        self.view.printFileName("")

    def updateFiles(self):
        self.view.filesBox.delete(0, END)
        files = self.model.getFiles()
        if(self._sortingFiles == True):
            files = reversed(files)
        for fd in files:
            self.view.filesBox.insert(END, fd)

    def sortFolders(self):
        self._sortingFolders = not self._sortingFolders
        self.updateFolders()

    def sortFiles(self):
        self._sortingFiles = not self._sortingFiles
        self.updateFiles()

    def renameFile(self, previousName, nextName):
        nextName = re.sub(r"\n", "", nextName)
        try:
            os.rename(self.model.getPath() + previousName, self.model.getPath() + nextName)
        except:
            messagebox.showinfo("Ошибка", "Файл с именем " + nextName + " уже существует!")
        self.updateFiles()
        self.view.printFileName("")

    def deleteFile(self, fileName):
        delete = messagebox.askyesno("Удалить", "Действительно удалить файл " + fileName + "?")
        if (delete == True):
            os.remove(self.model.getPath() + fileName)
        self.updateFiles()