import os
import shutil
import json

class SingletonClass:
    __instance = None

    @classmethod
    def get(self):
        if self.__instance == None:
            self.__instance = self()
        return self.__instance
    
class FileExplorer:

    def __init__(self):
        self.__targetDir = None
        self.__extList = []
        self.__fileList = []
        self.__filteredFileList = []
        self.__dirList = []

    # 멤버 변수 관련 기본 함수 : get, set, print, clear

    ## Set
    def __setExtList(self, inExtList):
        for ext in inExtList:
            names = list(filter(None, ext.split('.')))
            self.__extList.append(names)
    
    ## Get
    def getDirList(self):
        return self.__dirList
    
    def getFileList(self):
        return self.__fileList
    
    def getFilteredFileList(self):
        if self.__filteredFileList:
            return self.__filteredFileList
        else:
            return self.getFileList()
    
    ## Print
    def printList(self, list):
        for path in list:
            print(self.getName(path))

    def printTargetDir(self):
        self.printHighlight("Target Directory for searching:")
        print(self.__targetDir)
        print()
    
    def printExtList(self):
        self.printHighlight("Extension list for filtering files:")
        if self.__extList:
            for ext in self.__extList:
                print('.' + '.'.join(ext))
        else:
            print("All")
        print()
    
    def printDirList(self):
        self.printHighlight("Directory List:")
        self.printList(self.getDirList())
        print()
    
    def printFileList(self):
        self.printHighlight("File List:")
        self.printList(self.getFileList())
        print()
    
    def printFilteredFileList(self):
        self.printHighlight("Filtered File List:")
        self.printList(self.getFilteredFileList())
        print()

    def printAll(self):
        self.printTargetDir()
        self.printExtList()
        self.printDirList()
        self.printFileList()
        self.printFilteredFileList()
    
    ## Clear
    def clear(self):
        self.__targetDir = None
        self.__extList = []
        self.__fileList = []
        self.__filteredFileList = []
        self.__dirList = []

    # 주요 기능 관련 함수
    def search(self, inExtList = [], inTargetDir = os.path.curdir, bSearchAll = True):
        self.clear()

        self.__setExtList(inExtList)
        self.__targetDir = inTargetDir

        self.__search(self.__targetDir, bSearchAll)
        self.__filter()

    def __search(self, inTargetDir, bSearchAll = True): # 하위 폴더 및 파일 리스트 작성
        searchList = os.listdir(inTargetDir)
        for name in searchList:
            fullPath = os.path.join(inTargetDir, name)
            if os.path.isdir(fullPath):
                self.__dirList.append(fullPath)
                if bSearchAll:
                    self.__search(fullPath)
            else:
                self.__fileList.append(fullPath)

    def __filter(self):
        if self.__extList:
            for file in self.__fileList:
               if self.__checkExtList(file, self.__extList):
                   self.__filteredFileList.append(file)

    # 유틸리티
    def __checkExt(self, filePath, inExt):
        names = list(filter(None, filePath.split('.')))
        for i in range(len(inExt)):
            if names[-(i+1)] != inExt[-(i+1)]:
                return False
        return True
    
    def __checkExtList(self, filePath, inExtList):
        for ext in inExtList:
            if self.__checkExt(filePath, ext):
                return True
        
        return False
    
    def getName(self, path):
        return os.path.basename(os.path.normpath(path))
    
    def getDirName(self, path):
        return os.path.dirname(os.path.normpath(path))
    
    def printHighlight(self, text):
        print('\033[33m', end="")
        print(text)
        print('\033[0m', end="")

class ModuleFinder:
    def __init__(self):
        self.__targetDir = None
        self.__rootDirName = None
        self.__rootDir = None
        self.__modules = {}

    def getRootDir(self):
        return self.__rootDir

    def getModules(self):
        return self.__modules
    
    def printModules(self):
        FE = FileExplorer()
        for module, fileList in self.__modules.items():
            FE.printHighlight(module)
            FE.printList(fileList)
            print()

    def search(self, inTargetDir = os.path.curdir, inRootDirName = "Modules"):
        self.__targetDir = inTargetDir
        self.__rootDirName = inRootDirName

        # Search for "Modules" Folder
        FE = FileExplorer()
        FE.search(inTargetDir=self.__targetDir)
        for dir in FE.getDirList():
            if FE.getName(dir) == self.__rootDirName:
                self.__rootDir = dir
                break

        # Get all module's directories
        FE.search(inTargetDir=self.__rootDir, bSearchAll=False)
        moduleDirList = FE.getDirList()

        # Search the file list of each module
        extList = [
            ".h",
            ".cpp",
            ".Build.cs"
        ]
        for moduleDir in moduleDirList:
            FE.search(extList, moduleDir)
            self.__modules[FE.getName(moduleDir)] = FE.getFilteredFileList()

class NameManager():
    def __init__(self):
        self.__path = None
        self.__pathList = []
        self.__newPathList = []
        self.__oldName = None
        self.__newName = None

    def setNames(self, oldName, newName):
        self._clearPath()
        self.__oldName = oldName
        self.__newName = newName

    def getNewPathList(self):
        return self.__newPathList
    
    def clear(self):
        self._clearPath()
        self._clearName()

    def _clearPath(self):
        self.__path = None
        self.__pathList = []
        self.__newPathList = []

    def _clearName(self):
        self.__oldName = None
        self.__newName = None

    def rename(self, path):
        self.__path = path

        if os.path.isdir(path):
            self._renameFolder()
        else:
            self._renameFile()

    def renameWithList(self, pathList):
        self.__pathList = pathList
        for path in self.__pathList:
            self.rename(path)

    def _renamePath(self):
        FE = FileExplorer()
        sourceName = FE.getName(self.__path)
        targetName = sourceName.replace(self.__oldName, self.__newName)

        if sourceName != targetName:      
            dirName = FE.getDirName(self.__path)
            source = os.path.join(dirName, sourceName)
            target = os.path.join(dirName, targetName)
            os.rename(source, target)
            self.__newPathList.append(target)

    def _renameFile(self):
        self._replaceTextInFile()
        self._renamePath()

    def _renameFolder(self):
        self._renamePath()

    def _replaceTextInFile(self):
        with open(self.__path, 'r+', encoding='UTF8') as file:
            # Replace oldText to newText
            lineList = file.readlines()
            for line in lineList:
                if self.__oldName in line:
                    lineList[lineList.index(line)] = line.replace(self.__oldName, self.__newName)
            
            # Save to file
            file.seek(0)
            file.writelines(lineList)
            file.truncate()
            file.close()

class Generator:
    def _generate(self, templateDir, targetDir, templateName, targetName):
        source = os.path.join(templateDir, templateName)
        target = os.path.join(targetDir, targetName)
        self._copyFolder(source, target)

    def _copyFolder(self, source, target):
        if(os.path.isdir(target)):
            return

        if(os.path.isdir(source)):
            shutil.copytree(source, target)

class PluginGenerator(Generator):
    def __init__(self, templateDir, templateName, pluginDir, pluginName, moduleDescriptors, pluginDescriptor):
        self.__templateDir = templateDir
        self.__templateName = templateName
        self.__pluginDir = pluginDir
        self.__pluginName = pluginName
        self.__moduleDescriptors = moduleDescriptors

        self.__pluginDescriptor = pluginDescriptor
        self.__pluginDescriptor['FriendlyName'] = self.__pluginName
        for descriptor in self.__moduleDescriptors:
            module = {}
            module['Name'] = descriptor['moduleName'].replace("PLUGIN_NAME", self.__pluginName)
            if 'type' in descriptor:
                module['Type'] = descriptor['type']
            else:
                module['Type'] = "Runtime"
            
            if 'loadingPhase' in descriptor:
                module['LoadingPhase'] = descriptor['loadingPhase']
            else:
                module['LoadingPhase'] = "Default"
            self.__pluginDescriptor['Modules'].append(module)

        self.__moduleDir = os.path.join(self.__pluginDir, self.__pluginName)

    def generate(self):
        # Generate Plugin Template
        self._generate(self.__templateDir, self.__pluginDir, self.__templateName, self.__pluginName)
        self.__generateModule()

        MF = ModuleFinder()
        MF.search(self.__moduleDir, "Source")
        
        NM = NameManager()

        for module, fileList in MF.getModules().items():
            # PLUGIN_NAMEGAMEPLAYTAGS_API > TestGAMEPLAYTAGS_API
            NM.setNames("PLUGIN_NAME", self.__pluginName)
            NM.renameWithList(fileList)
            newPathList = NM.getNewPathList()

            # TestGAMEPLAYTAGS_API > TESTGAMEPLAYTAGS_API
            API = "_API"
            moduleName = module.upper().replace("PLUGIN_NAME", self.__pluginName)
            NM.setNames(moduleName + API, moduleName.upper() + API)
            NM.renameWithList(newPathList)

            # Rename Module Folder Name
            NM.setNames("PLUGIN_NAME", self.__pluginName)
            NM.rename(os.path.join(MF.getRootDir(), module))

        # .uplugin
        self.__generateUplugin()


    def __generateModule(self):
        # Find all module templates
        MF = ModuleFinder()
        MF.search()
        modules = MF.getModules()
        rootDir = MF.getRootDir()

        MG = ModuleGenerator()

        for descriptor in self.__moduleDescriptors:
            MG.generate(rootDir, os.path.join(self.__moduleDir, "Source"), descriptor['templateName'], descriptor['moduleName'])

    def __generateUplugin(self):
        with open(os.path.join(self.__pluginDir, self.__pluginName, self.__pluginName + ".uplugin"), "w", ) as file:
            json.dump(self.__pluginDescriptor, file, indent=4)

class ModuleGenerator(Generator):
    def __init__(self):
        self.__macroName = "MODULE_NAME"
        self.__templateName = None
        self.__newName = None
        self.__extList = [
            ".h",
            ".cpp",
            ".Build.cs"
        ]

    def generate(self, templateDir, moduleDir, templateName, moduleName):
        self._generate(templateDir, moduleDir, templateName, moduleName)

        FE = FileExplorer()
        FE.search(self.__extList, os.path.join(moduleDir, moduleName))

        # MODULE_NAME_API > Test_API
        # MODULE_NAME_API > Test_API
        NM = NameManager()
        NM.setNames(self.__macroName, moduleName)
        NM.renameWithList(FE.getFilteredFileList())
        newPathList = NM.getNewPathList()

        # MODULE_NAME_API > TEST_API
        # PLUGIN_NAMEGameplayTags_API > PLUGIN_NAMEGAMEPLAYTAGS_API
        API = "_API"
        NM.setNames(moduleName + API, moduleName.upper() + API)
        NM.renameWithList(newPathList)

