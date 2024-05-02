"""
Author: Tak
Website: https://ta-note.com
Description:
    Drag and drop install.py file in maya viewport.
    "<moduleName>.mod" file will created in "Documents\maya\modules" directory automatically.
"""

import os
import sys

from maya import cmds, mel


MODULE_PATH = os.path.dirname(__file__).replace('\\', '/')
MODULE_NAME = MODULE_PATH.rsplit('/', 1)[-1]
MAYA_VERSION = int(cmds.about(version=True))
MODULE_VERSION = 'Any'
SHELF_ICON_FILE = 'ChatGPT_logo.png'
SHELF_BUTTON_COMMAND = '''
from imp import reload
import chatmaya; reload(chatmaya)
chatmaya.run()
'''

PYTHON_VERSION_TABLE = {
    2023: 39,
    2024: 310
}


def onMayaDroppedPythonFile(*args, **kwargs):
    removeOldInstallModule()
    addEnvPaths()
    addShelfButtons()
    createModuleFile()
    cmds.confirmDialog(title='Info', message='"{}" module installed successfully.'.format(MODULE_NAME))


def removeOldInstallModule():
    foundOldInstall = False
    for modName in sys.modules:
        if modName == 'install':
            foundOldInstall = True
            break
    if foundOldInstall:
        del(sys.modules[modName])


def addEnvPaths():
    # Add python script paths
    pythonPaths = [
        '{}/scripts'.format(MODULE_PATH),
        '{}/extern/Python{}/site-packages'.format(MODULE_PATH, PYTHON_VERSION_TABLE[MAYA_VERSION])
    ]
    for path in pythonPaths:
        sys.path.append(path)

    # Add icon folder path
    iconPaths = mel.eval('getenv "XBMLANGPATH";')
    iconPaths += ';{}/icons'.format(MODULE_PATH)
    mel.eval('putenv "XBMLANGPATH" "{}";'.format(iconPaths))


def addShelfButtons():
    curShelf = getCurrentShelf()

    cmds.shelfButton(
        command=SHELF_BUTTON_COMMAND,
        annotation=MODULE_NAME,
        sourceType='Python',
        image=SHELF_ICON_FILE,
        image1=SHELF_ICON_FILE,
        parent=curShelf
    )


def getCurrentShelf():
    curShelf = None

    shelf = mel.eval('$gShelfTopLevel = $gShelfTopLevel')
    curShelf = cmds.tabLayout(shelf, query=True, selectTab=True)

    return curShelf


# Folders in the module directory that named as "icons, plug-ins, scripts" are automatically added to the maya environment variables.
def createModuleFile():
    moduleFileName = '{}.mod'.format(MODULE_NAME)

    contents = '''+ MAYAVERSION:2023 {0} {1} {2}
PYTHONPATH +:= extern/Python39/site-packages

+ MAYAVERSION:2024 {0} {1} {2}
PYTHONPATH +:= extern/Python310/site-packages
'''.format(MODULE_NAME, MODULE_VERSION, MODULE_PATH)

    with open(os.path.join(getModulesDirectory(), moduleFileName), 'w') as f:
        f.write(contents)


def getModulesDirectory():
    modulesDir = None

    mayaAppDir = cmds.internalVar(uad=True)
    modulesDir = os.path.join(mayaAppDir, 'modules')

    if not os.path.exists(modulesDir):
        os.mkdir(modulesDir)

    return modulesDir
