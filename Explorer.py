import os
class Explorer:
    _currentPath = []
    _folders = []
    _files = []

    def __init__(self, letter):
        self._currentPath.append(letter + ':\\')
        self.getFolders()
        self.getFiles()
        print("Init model")

    def getFolders(self):
        self._folders.clear()

        for (dirpath, dirnames, filenames) in os.walk("".join(self._currentPath)):
            self._folders.extend(dirnames)
            break
        return self._folders

    def getFiles(self):
        self._files.clear()
        for (dirpath, dirnames, filenames) in os.walk("".join(self._currentPath)):
            self._files.extend(filenames)
            break
        return self._files

    def stepInto(self, level):
        self._currentPath.append(level + "\\")

    def stepBack(self):
        del self._currentPath[-1]

    def getPath(self):
        return "".join(self._currentPath)

    def setPath(self, path):
        self._currentPath = path