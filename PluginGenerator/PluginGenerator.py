import shutil
import os

import e4lib

# 사용자 설정
templateName = "PluginTemplate"
newModuleName = "NewModule"
newPluginName = "NewPlugin"

# 폴더 구조
upluginExt = ".uplugin"

# 시스템 설정
currentDir = os.getcwd()
duplicatedPath = os.path.join(currentDir, newPluginName)
templatePath = os.path.join(currentDir, templateName)
# newModulePath = os.path.join(currentDir, newModuleName)
# newPluginPath = os.path.join(currentDir, newPluginName)

class SingletonClass:
    __instance = None

    @classmethod
    def get(self):
        if self.__instance == None:
            self.__instance = self()
        return self.__instance
    
class ModuleGenerator(SingletonClass):
    
    @classmethod
    def test(self):
        pass
    
class PluginGenerator(SingletonClass):
    
    @classmethod
    def generate(self):
        self.__duplicateTemplate()
         
    @classmethod   
    def __duplicateTemplate(self):
        if(os.path.isdir(templatePath)):
            # Copy with renaming folder
            shutil.copytree(templatePath, duplicatedPath)
            
    @classmethod
    def __rename(self):
        oldUpluginPath = os.path.join(duplicatedPath, templateName + upluginExt)
        newUpluginPath = os.path.join(duplicatedPath, newPluginName + upluginExt)
        
        if(os.path.isfile(oldUpluginPath)):
            os.rename(oldUpluginPath, newUpluginPath)
        
    @classmethod
    def test(self):
        self.__rename()

PG = PluginGenerator.get()
# PG.generate()
print(PG.test())