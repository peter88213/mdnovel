## Changelog

### Planned features

See the [GitHub "Features" project](https://github.com/users/peter88213/projects/17)

### Version 0.18.2

Refactor the code for better maintainability.

Based on apptk 2.1.0

### Version 0.18.1

- Link the project to the new apptk library.

Based on apptk 1.0.0

### Version 0.18.0

Refactor the code for better maintainability:
- Simplify the PopUpBase API.
- Extract and separate a MVC framework package.

### Version 0.17.6

Refactor the code for better maintainability:
- Provide an abstract base class for pop-up windows.
- Make ExportOptionsWindow and ViewOptionsWindow PopUpBase subclasses.
- Rename the NvView.view_options method.

### Version 0.17.5

- Provide an abstract base class for the view components.
- Make the tree viewer, contents viewer, toolbar, and properties viewer ViewComponentBase subclasses.
- Provide an abstract base class for the plugins.
- Make the plugins PluginBase subclasses.

### Version 0.17.4

- Make the application independent of the *idle3* package on Linux.

### Version 0.17.3

- Make the application independent of the *idle3* package on Linux.

### Version 0.17.2

- Refactor: Use the view's API instead of tkinter imports.

### Version 0.17.1

- Refactor the plugin system.

### Version 0.17.0

- Refactor the plugin system.

### Version 0.16.1

- Refactor the plugin system.

### Version 0.16.0

- Refactor, reintroduce a plugin system.

### Version 0.15.3

- Saving the editor window geometry before starting full screen mode.

### Version 0.15.2

- Fix a bug where the word count is not logged when saving the project.

### Version 0.15.1

- Fix the editor's word counter.

### Version 0.15.0

- Providing a "distraction free" editing mode.

### Version 0.14.1

- Refactor: Remove the locking mechanism code. 

### Version 0.14.0

- Remove .yw7 support (replaced by the external [mdnov_yw7](https://github.com/peter88213/mdnov_yw7) tool.
- Remove .novx support (replaced by the external [mdnov_novx](https://github.com/peter88213/mdnov_novx) tool.

### Version 0.13.1

- Add ID to the section list.

### Version 0.13.0

- Fix HTML report title display.
- Exporting item list.
- Exporting location list.
- Exporting character list.
- Exporting section list.

### Version 0.12.1

- Update "Story templates" submenu entries.

### Version 0.12.0

- Add Story structure template manager.
- Fix a bug where novx paragraph tags appear in markdown import.

### Version 0.11.0

- Supporting Timeline synchronisation.

### Version 0.10.0

- Remove the plugin manager.
- No longer handle exceptions when loading plugins.

### Version 0.9.1

- Remove the "css" entry from the File menu.
- Change the wording in the Section menu. 

### Version 0.9.0

- Provide links to the online manual.
- Remove the local help pages.

### Version 0.8.0

- Add a theme changer.

### Version 0.7.0

- Add a relationship matrix.

### Version 0.6.0

- Add a daily progress viewer.

### Version 0.5.0

- Remove document language processing.
- Update novx export: writing links according to DTD 1.4.

### Version 0.4.1

- Fix chapter/part heading prefix/suffix reading.
- Closing an editor window when the corresponding section is deleted.

### Version 0.4.0

- Reading and writing the mdnov file format, whis is now the standard file format.
- Prevent the same section from being loaded in more than one editor window at the same time.
- Update the setup script.

### Version 0.3.1

- Fix Markdown import/export issues.

### Version 0.3.0

- Export descriptions of plot lines and plot points.

### Version 0.2.0

- Export a story structure description.

### Version 0.1.3

- Reading Section.appendToPref from novx. This avoids unnessecarily asking for saving changes when closing. 

### Version 0.1.2

- Fix novx import/export and yw7 export.
- Provide a download link on the landing page.

### Version 0.1.1

- Bugfix / refactor.

### Version 0.1.0

- The novx format is the standard file format for the time being. 
- Featuring an in-place section editor.
- Importing and exporting the *.novx* file format.
- Importing and exporting the *.yw7* file format.
- Creating new projects from Markdown-formatted work-in-progress.
- Creating new projects from Markdown-formatted outline.
- Exporting a Markdown manuscript.
- Exporting a Markdown synopsis with part descriptions.
- Exporting a Markdown synopsis with chapter descriptions.
- Exporting a Markdown brief synopsis with chapter titles and section titles.
- Exporting a Markdown full synopsis with section descriptions.
- Exporting a csv Plot Grid.



