[![Download the latest release](docs/img/download-button.png)](https://github.com/peter88213/mdnovel/raw/main/dist/mdnovel_v0.99.0.pyzw)
[![Changelog](docs/img/changelog-button.png)](docs/changelog.md)
[![Feedback](docs/img/feedback-button.png)](https://github.com/peter88213/mdnovel/discussions/)
[![Online help](docs/img/help-button.png)](https://peter88213.github.io/mdnovhelp-en/)

# ![N](docs/img/nLogo32.png) mdnovel

A novel writing application using markdown.

![Screenshot](docs/Screenshots/screen01.png)

## Features

- With *mdnovel*, extensive novels can be broken down into **parts, chapters, and sections**. 
- *mdnovel* provides a section text editor with an optional distraction-free mode. 
- You can store data on **characters, locations, and items** that are important for the story. 
  This includes the optional definition of a **viewpoint character** for each section. 
- All of this appears as a clear and editable **tree** structure with listed information. 
- Summaries can be entered at all these levels, from which **synopses** and lists can be generated. 
- If you choose a **narrative structure**, *mdnovel* can display stages (e.g. acts or steps) in the tree.
  When plotting, descriptions of these stages can be entered, from which *mdnovel* can generate 
  its own documentation. Prefabricated structural models can also be imported from templates.
- *mdnovel* also allows you to create and document an underlying structure of **plot lines** 
  (e.g. subplots or character arcs) apart from the chapters and sections. This can then be linked 
  to the sections of the novel text.
- *mdnovel* provides a **plot grid** with plot line notes for each section. This allows you to 
  see the big picture and keep track of multiple subplots.   
- The section relationships to plot lines, characters, locations, and items 
  can also be displayed and edited with a spreadsheet-like matrix.
- To keep track of progress, the **word count** and the **completion status** of the sections are displayed. 
  *mdnovel* dan display a list of daily word count log entries.
- Individual chapters and sections can be flagged as "unused" to exclude them from document export.
- You can add information about the **narrative time** and duration to each section. If you enter a date, 
  the day of the week is displayed. You can also call up the age of characters that are assigned to
  a section. The date and time information can be synchronised with the [Timeline](http://thetimelineproj.sourceforge.net/) application.
- For **printing**, *mdnovel* exports a neatly designed novel manuscript that can be converted with *pandoc*
  into several document and ebook formats. 
- *mdnovel* saves its data in a single, easy-to-understand Markdown/YAML-formatted text file.
- *mdnovel* is written in Python and should run on several **operating systems**, like Windows and Linux.
- The application is ready for internationalization with GNU gettext. German translations are provided. 

[Screenshots](docs/Screenshots/)

## Requirements

- Windows or Linux. Mac OS support is experimental.
- [Python](https://www.python.org/) version 3.6+. 
     - For current Windows versions, use version 3.9.10 or above.
     - For Vista and Windows 7, use version 3.7.2.
     - Linux users: Make sure you have the *python3-tk* package installed. 
       To see the tooltips, make sure that you have the *idle3* package installed.
- Users may want to install [pandoc](https://pandoc.org/) for processing the exported documents.
- To have a [wider choice of design themes](https://ttkthemes.readthedocs.io/en/latest/themes.html), you can 
  [install the ttkthemes package](https://ttkthemes.readthedocs.io/en/latest/installation.html).
- If you want to visualize the course of narrative time, you can optionally install
  [Timeline version 2.4+](http://thetimelineproj.sourceforge.net/).


## General note about the fitness for use

This program is primarily a proof of concept. I do not use it for my own writing. 
For me, it is now feature complete and I do not intend to develop it further except to fix bugs.   

As far as I can tell, the program is stable and reliable. However, the section editor is rather rudimentary; 
it has neither a search function nor a spell checker. 

Also, I don't know any writers who write novels in Markdown and create their manuscripts with the help of *Pandoc*. 
But perhaps you are the exception. In any case, I hope you enjoy playing around and experimenting with *mdnovel*.


## Download and install

### Default: Executable Python zip archive

Download the latest release [mdnovel_v0.99.0.pyzw](https://github.com/peter88213/mdnovel/raw/main/dist/mdnovel_v0.99.0.pyzw)

- Launch *mdnovel_v0.99.0.pyzw* by double-clicking (Windows/Linux desktop),
- or execute `python mdnovel_v0.99.0.pyzw` (Windows), resp. `python3 mdnovel_v0.99.0.pyzw` (Linux) on the command line.

#### Important

Many web browsers recognize the download as an executable file and offer to open it immediately. 
This starts the installation.

However, depending on your security settings, your browser may 
initially  refuse  to download the executable file. 
In this case, your confirmation or an additional action is required. 
If this is not possible, you have the option of downloading 
the zip file. 


### Alternative: Zip file

The package is also available in zip format: [mdnovel_v0.99.0.zip](https://github.com/peter88213/mdnovel/raw/main/dist/mdnovel_v0.99.0.zip)

- Extract the *mdnovel_v0.99.0* folder from the downloaded zipfile "mdnovel_v0.99.0.zip".
- Move into this new folder and launch *setup.pyw* by double-clicking (Windows/Linux desktop), 
- or execute `python setup.pyw` (Windows), resp. `python3 setup.pyw` (Linux) on the command line.

---

[Changelog](docs/changelog.md)

## Usage

See the [online manual](https://peter88213.github.io/mdnovhelp-en/)

---

## Tools

- [mdnov_novx](https://github.com/peter88213/mdnov_novx) -- Converter between .mdnov and .novx file format.
- [mdnov_yw7](https://github.com/peter88213/mdnov_yw7) -- Converter between .mdnov and .yw7 file format.

---

## Credits

- The logo is made using the free *Pusab* font by Ryoichi Tsunekawa, [Flat-it](http://flat-it.com/).

## License

This is Open Source software, and *mdnovel* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/mdnovel/blob/main/LICENSE) file.

