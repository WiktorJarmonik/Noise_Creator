import os
import sys


try:
    import maya.mel
    import maya.cmds
    isMaya = True
except ImportError:
    isMaya = False


def onMayaDroppedPythonFile(*args, **kwargs):
    """This function is only supported since Maya 2017 Update 3"""
    pass


def _onMayaDropped():
    """Dragging and dropping this file into the scene executes the file."""

    srcPath = os.path.dirname(__file__)
    iconPath = os.path.join(srcPath, 'icons', 'noise_make_icon2.jpg')

    srcPath = os.path.normpath(srcPath)
    iconPath = os.path.normpath(iconPath)

    if not os.path.exists(iconPath):
        raise IOError('Cannot find ' + iconPath)

    for path in sys.path:
        if os.path.exists(path + '/Noise_Creator/make_noise_ui.py'):
            maya.cmds.warning('Noise Creator is already installed at ' + path)

    command = '''
import os
import sys
import maya.cmds as cmds

if not os.path.exists(r'{path}'):
    raise IOError(r'The source path "{path}" does not exist!')
    
if r'{path}' not in sys.path:
    sys.path.insert(0, r'{path}')
    
scriptDir = cmds.internalVar(userScriptDir=True)
sys.path.append(scriptDir+'/Noise_Creator/')
#py2 and py3 support
if sys.version_info[0] < 3:
    import make_noise_ui
    reload (make_noise_ui)
else:
    from importlib import reload
    import make_noise_ui
    reload (make_noise_ui)

# -----------------------------------
# Noise Creator
# Wiktor Jarmonik
# -----------------------------------
'''.format(path=srcPath)

    shelf = maya.mel.eval('$gShelfTopLevel=$gShelfTopLevel')
    parent = maya.cmds.tabLayout(shelf, query=True, selectTab=True)
    maya.cmds.shelfButton(
        command=command,
        annotation='Noise Creator by Wiktor Jarmonik',
        sourceType='Python',
        image=iconPath,
        image1=iconPath,
        parent=parent
    )

    print("\n// Noise Creator has been added to current shelf.")


if isMaya:
    _onMayaDropped()
