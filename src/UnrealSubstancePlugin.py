import tkinter.filedialog                                                               # allows for communication between files to convey information
from unreal import ToolMenuContext, ToolMenus, uclass, ufunction, ToolMenuEntryScript   # importing various necessary elements of unreal code to perform the plugin's purpose
import os                                                                               # importing the native operating system
import sys                                                                              # importing system
import importlib                                                                        # importing Python import capabilities
import tkinter                                                                          # importing window creation/deletion/manipulation tools

srcPath = os.path.dirname(os.path.abspath(__file__))                                    # defining the srcPath
if srcPath not in sys.path:                                                             # if the srcPath is not in the system file path,
    sys.path.append(srcPath)                                                            # then add it to the system file path

import UnrealUtilities                                                                  # importing tools from Unreal Engine script
importlib.reload(UnrealUtilities)                                                       # reloading the tools every time the code is executed

@uclass()                                                                               # defining an execution function (decorator)
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):                                # defining the class (inherits parent class)
    @ufunction(override=True)                                                           # creating a new implementation of inherited method when function is called
    def execute(self, context: ToolMenuContext) -> None:                                # defining execution parameters
        UnrealUtilities.UnrealUtility().FindOrBuildBaseMaterial()                       # calling on UnrealUtilities.py to execute the associated function

@uclass()                                                                               # defining an execution function (decorator)
class LoadMeshEntryScript(ToolMenuEntryScript):                                         # defining the class (inherits parent class) 
    @ufunction(override=True)                                                           # creating a new implementation of inherited method when function is called
    def execute(self, context) -> None:                                                 # defining execution parameters
        window = tkinter.Tk()                                                           # creating a new widget
        window.withdraw()                                                               # redrawing the widget
        importDir = tkinter.filedialog.askdirectory()                                   # asking for & returning the directory of the selected file folder
        window.destroy()                                                                # destroying the widget
        UnrealUtilities.UnrealUtility().ImportFromDir(importDir)                        # calling on UnrealUtilities.py to execute the associated function

class UnrealSubstancePlugin:                                                            # defining the class
    def __init__(self):                                                                 # establishing variables to be used across the class
        self.submenuName = "UnrealSubstancePlugin"                                      # the name for the submenu as the program refers to it
        self.submenuLabel = "Unreal Substance Plugin"                                   # the display name for the submenu heading
        self.CreateMenu()                                                               # executing the function to create the necessary menu(s)

    def CreateMenu(self):                                                               # defining the function
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")                    # calling on Unreal Engine's top dropdown menu

        existing = ToolMenus.get().find_menu(f"LevelEditor.MainMenu.{self.submenuName}")    # figuring out whether the submenu's to be created already exist
        if existing:                                                                        # if the above condition is satisfied (one of the designated submenus already exists),
            print(f"deleting previous menu: {existing}")                                    # print in the debug log that the already existing menu is being deleted,
            ToolMenus.get().remove_menu(existing.menu_name)                                 # and delete the menu

        self.submenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", self.submenuName, self.submenuLabel)   # creating a new submenu within the main dropdown menu with the designated name, display name and tooltip
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript())     # defining the button for creating a base material (name, display name, executable function)
        self.AddEntryScript("LoadFromDirectory", "Load From Directory", LoadMeshEntryScript())              # defining the button for importing a mesh (name, display name, executable function)
        ToolMenus.get().refresh_all_widgets()                                                               # rebuilds widgets that are currently open

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):                     # defining the function for creating a button within the submenu
        script.init_entry(self.submenu.menu_name, self.submenu.menu_name, "", name, label)  # defining the syntax of arguments for each button to be created
        script.register_menu_entry()                                                        # creating the button

UnrealSubstancePlugin()                                                                     # running the code