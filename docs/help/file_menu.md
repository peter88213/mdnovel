# File menu

**File operation**


## New

**Create a new novel project**

With **File \> New**, you can create a new project. This will open a
submenu.

Empty project  
- This will close the current project and create a blank project.
- A file select dialog asks for the new project’s file name. If you
  cancel the dialog, you can select the file name later when saving the
  project.

Create from Markdown...  
- This will close the current project and open a file dialog asking for
  a Markdown document to create the new projec from.
- The newly created project is saved automatically in the same directory
  as the Markdown document, using its file name and the extension *.novx*.
- If a project with the same file name as the Markdown document already
  exists in the directory, no new project will be created.
- If you select a previously exported document belonging to an existing
  project, this project will be updated and loaded.
- The Markdown document can either be a
  [Work-in-progress](getting_started#starting-with-a-work-in-progress),
  i.e. a regular novel manuscript with chapter headings and section
  contents, r an
  [outline](getting_started#starting-with-an-outline) containing
  the chapter and section structure with titles and descriptions.

## Open...

**Open a novel project**

With **File \> Open** or `Ctrl`-`O`, you can open an existing project
file.

---

**Note**

When opening a project, the current project will be closed. If there are
unsaved changes, you will be asked for saving.

---

## Reload

**Reload the novel project**

With **File \> Reload** or `Ctrl`-`R`, you can overwrite the project in
the memory with the last saved version.

---

**Tip**


This way you can undo changes made in the current session.

---

---

**Note**

If the project has changed on disk since last opened or saved, you will
get a warning.

---

## Restore backup

**Restore the latest backup file**

With **File \> Restore backup** or `Ctrl`-`B`, you can overwrite the
project in the memory with the latest backup file. You will get a
warning, because changes may be lost.

---

**Hint**

After restoring the backup, a backup copy is no longer available in the
project directory. A new backup copy is created when saving the project.

---

## Refresh tree

**Enforce tree refresh after making changes**

With **File \> Refresh tree** or `F5`, you can refresh the tree.

- "Normal" sections that have been moved to an "Unused" chapter are made
  "Unused".
- Parts and chapters are renumbered according to the [Auto numbering
  settings](book_view#auto-numbering).
- The "Trash" chapter is moved to the end of the book, if necessary.


## Open Project folder

**Launch the file manager**

With **File \> Open Project folder** or `Ctrl-P`, you can launch the
file manager with the current project folder. This might come in handy,
if you e.g. wish to delete files or edit configuration files.


## Save

**Save the project**

With **File \> Save** or `Ctrl`-`S`, you can save the project. A backup
copy is then automatically created.

---

**Note**

If the project has changed on disk since last opened, you will get a
warning.

---

## Save as...

**Save the project with another file name/at another place**

With **File \> Save as...** or `Ctrl`-`Shift`-`S`, you can save the
project with another file name/at another place. Then a file select
dialog opens to specify the new path and file name.

---

**Note**

Your current project remains as saved the last time. Changes since then
apply to the new project.

---

## Close

**Close the novel project**

With **File \> Close**, you can close the project without exiting the
program. When closing the project, you will be asked for saving the
project, if it has changed.

---

**Note**

If you open another project, the current project is automatically
closed.

---

## Quit/Exit

**Exit the program**

- Under Windows you can exit with **File \> Exit** or `Alt`-`F4`.
- Otherwise you can exit with **File \> Quit** or `Ctrl`-`Q`.

---

**Note**

When exiting the program, you will be asked for saving the project, if
it has changed.

---
