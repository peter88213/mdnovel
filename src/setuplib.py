"""mdnovel installer library module. 

Version 0.1.0

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from shutil import copytree
from shutil import copy2
from shutil import rmtree
import zipfile
import os
import sys
import stat
from pathlib import Path
from string import Template
import gettext
import locale
import platform
try:
    import tkinter as tk
except ModuleNotFoundError:
    print('The tkinter module is missing. Please install the tk support package for your python3 version.')
    sys.exit(1)

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    # Fallback for old Windows versions.
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('reg', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPNAME = 'mdnovel'
VERSION = ' @release'
APP = f'{APPNAME}.py'
START_UP_SCRIPT = 'run.pyw'
INI_FILE = f'{APPNAME}.ini'
INI_PATH = '/config/'
TEMPLATE_PATH = 'templates/'
SAMPLE_PATH = 'sample'

SUCCESS_MESSAGE = '''

$Appname is installed here:

$Apppath'''

SHORTCUT_MESSAGE = '''
Now you might want to create a shortcut on your desktop.  

On Windows, open the installation folder, hold down the Alt key on your keyboard, 
and then drag and drop "run.pyw" to your desktop.

On Linux, create a launcher on your desktop. With xfce for instance, the launcher's command may look like this:
python3 '$Apppath' %f
'''

ADD_TO_REGISTRY = f'''Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\Software\Classes\\.mdnovel]
[HKEY_CURRENT_USER\Software\Classes\\.mdnovel]
"Content Type"="text/xml"
@="mdnovel"
[HKEY_CURRENT_USER\Software\Classes\\mdnovel]
@="mdnovel Project"
[HKEY_CURRENT_USER\Software\Classes\\mdnovel\DefaultIcon]
@="$INSTALL\\\\icons\\\\nLogo64.ico"
[HKEY_CURRENT_USER\Software\Classes\\mdnovel\shell\open\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\""

'''

REMOVE_FROM_REGISTRY = f'''Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\Software\Classes\\mdnovel]
[-HKEY_CURRENT_USER\Software\Classes\\.mdnovel]

'''

START_UP_CODE = f'''import {APPNAME}
import tkinter as tk
from tkinter import messagebox
import traceback

def show_error(self, *args):
    err = traceback.format_exception(*args)
    messagebox.showerror('Exception', err)


tk.Tk.report_callback_exception = show_error
{APPNAME}.main()
'''

root = tk.Tk()
processInfo = tk.Label(root, text='')
message = []

pyz = os.path.dirname(__file__)


def extract_templates(templateDir):
    with zipfile.ZipFile(pyz) as z:
        for file in z.namelist():
            if file.startswith(TEMPLATE_PATH):
                targetFile = file.replace(TEMPLATE_PATH, '')
                if not targetFile:
                    continue
                if os.path.isfile(f'{templateDir}/{targetFile}'):
                    output(f'Overwriting "{templateDir}/{targetFile}" ...')
                else:
                    output(f'Copying "{templateDir}/{targetFile}" ...')
                with open(f'{templateDir}/{targetFile}', 'wb') as f:
                    f.write(z.read(file))


def cp_templates(templateDir):
    try:
        with os.scandir(TEMPLATE_PATH) as files:
            for file in files:
                if os.path.isfile(f'{templateDir}/{file.name}'):
                    output(f'Overwriting "{templateDir}/{file.name}" ...')
                else:
                    output(f'Copying "{file.name}" ...')
                copy2(f'{TEMPLATE_PATH}/{file.name}', f'{templateDir}/{file.name}')
    except:
        pass


def extract_file(sourceFile, targetDir):
    with zipfile.ZipFile(pyz) as z:
        z.extract(sourceFile, targetDir)


def extract_tree(sourceDir, targetDir):
    with zipfile.ZipFile(pyz) as z:
        for file in z.namelist():
            if file.startswith(f'{sourceDir}/'):
                z.extract(file, targetDir)


def fix_ini(iniFile):
    if not os.path.isfile(iniFile):
        return

    with open(iniFile, 'r') as f:
        text = f.read()
    if 'ed_color_bg_bright = black' in text:
        output('Removing outdated configuration file ...')
        os.remove(iniFile)


def cp_tree(sourceDir, targetDir):
    copytree(sourceDir, f'{targetDir}/{sourceDir}', dirs_exist_ok=True)


def make_context_menu(installPath):
    """Generate ".reg" files to extend the mdnovel context menu."""

    def save_reg_file(filePath, template, mapping):
        """Save a registry file."""
        with open(filePath, 'w') as f:
            f.write(template.safe_substitute(mapping))
        output(f'Creating "{os.path.normpath(filePath)}"')

    python = sys.executable.replace('\\', '\\\\')
    installUrl = installPath.replace('/', '\\\\')
    script = f'{installUrl}\\\\{START_UP_SCRIPT}'
    mapping = dict(PYTHON=python, SCRIPT=script, INSTALL=installUrl)
    # save_reg_file(f'{installPath}/add_mdnovel.reg', Template(ADD_TO_REGISTRY), mapping)
    save_reg_file(f'{installPath}/remove_mdnovel.reg', Template(REMOVE_FROM_REGISTRY), {})


def output(text):
    message.append(text)
    processInfo.config(text=('\n').join(message))


def open_folder(installDir):
    """Open an installation folder window in the file manager.
    """
    try:
        os.startfile(os.path.normpath(installDir))
        # Windows
    except:
        try:
            os.system('xdg-open "%s"' % os.path.normpath(installDir))
            # Linux
        except:
            try:
                os.system('open "%s"' % os.path.normpath(installDir))
                # Mac
            except:
                pass


def install(installDir, zipped):
    """Install the application."""
    if zipped:
        copy_file = extract_file
        copy_tree = extract_tree
        copy_templates = extract_templates
    else:
        copy_file = copy2
        copy_tree = cp_tree
        copy_templates = cp_templates

    #--- Create a general mdnovel installation directory, if necessary.
    os.makedirs(installDir, exist_ok=True)
    cnfDir = f'{installDir}/{INI_PATH}'
    if os.path.isfile(f'{installDir}/{APP}'):
        simpleUpdate = True
    else:
        simpleUpdate = False

    os.makedirs(cnfDir, exist_ok=True)

    #--- Delete the old version, but retain configuration, if any.
    # Do not remove the locale folder, because it may contain plugin data.
    # Do not remove the icons folder, because it may contain plugin data.
    with os.scandir(installDir) as files:
        for file in files:
            try:
                os.remove(file)
                output(f'"{file.name}" removed.')
            except:
                pass

    #--- Install the new version.
    output(f'Copying "{APP}" ...')
    copy_file(APP, installDir)

    # Create a starter script.
    output('Creating starter script ...')
    with open(f'{installDir}/{START_UP_SCRIPT}', 'w', encoding='utf-8') as f:
        f.write(f'import {APPNAME}\n{APPNAME}.main()')

    # Install the localization files.
    output('Copying locale ...')
    copy_tree('locale', installDir)

    # Install the icon files.
    output('Copying icons ...')
    copy_tree('icons', installDir)

    # Remove the editor configuration file, if outdated.
    fix_ini(f'{installDir}/config/editor.ini')

    # Install the sample templates.
    templateDir = f'{installDir}/templates'
    os.makedirs(templateDir, exist_ok=True)
    copy_templates(templateDir)

    # Provide the sample files.
    output('Copying/replacing sample files ...')
    rmtree(f'{installDir}/{SAMPLE_PATH}', ignore_errors=True)
    copy_tree(SAMPLE_PATH, installDir)

    #--- Make the scripts executable under Linux.
    st = os.stat(f'{installDir}/{APP}')
    os.chmod(f'{installDir}/{APP}', st.st_mode | stat.S_IEXEC)
    st = os.stat(f'{installDir}/{START_UP_SCRIPT}')
    os.chmod(f'{installDir}/{START_UP_SCRIPT}', st.st_mode | stat.S_IEXEC)

    #--- Generate registry entries for the context menu (Windows only).
    if platform.system() == 'Windows':
        make_context_menu(installDir)

    #--- Display a success message.
    mapping = {'Appname': APPNAME, 'Apppath': f'{installDir}/{START_UP_SCRIPT}'}
    output(Template(SUCCESS_MESSAGE).safe_substitute(mapping))

    #--- Ask for shortcut creation.
    if not simpleUpdate:
        output(Template(SHORTCUT_MESSAGE).safe_substitute(mapping))

    #--- Create a start-up script.
    if platform.system() == 'Windows':
        shebang = ''
    else:
        shebang = '#!/usr/bin/env python3\n'
    with open(f'{installDir}/{START_UP_SCRIPT}', 'w', encoding='utf-8') as f:
        f.write(f'{shebang}{START_UP_CODE}')


def main(zipped=True):
    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    # Open a tk window.
    root.title('Setup')
    output(f'*** Installing {APPNAME}{VERSION} ***\n')
    header = tk.Label(root, text='')
    header.pack(padx=5, pady=5)

    # Prepare the messaging area.
    processInfo.pack(padx=5, pady=5)

    # Run the installation.
    homePath = str(Path.home()).replace('\\', '/')
    mdnovelPath = f'{homePath}/.mdnovel'
    try:
        install(mdnovelPath, zipped)
    except Exception as ex:
        output(str(ex))

    # Show options: open installation folders or quit.
    root.openButton = tk.Button(text="Open installation folder", command=lambda: open_folder(f'{homePath}/.mdnovel'))
    root.openButton.config(height=1, width=30)
    root.openButton.pack(padx=5, pady=5)
    root.quitButton = tk.Button(text="Quit", command=quit)
    root.quitButton.config(height=1, width=30)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()

