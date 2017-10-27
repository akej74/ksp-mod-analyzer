# KSP Mod Analyzer
Analyze Kerbal Space Program mods on SpaceDock, Curse and CKAN repositories.

<img src="https://github.com/akej74/ksp-mod-analyzer/blob/master/screenshots/ksp_mod_analyzer_screenshot_1.png" width="700">

### Features
- Parse SpaceDock, Curse and CKAN repositories and store data locally in a database
- Display mod availability on each repository
- Display meta-data for source code and forum links if available
- Filter mods with a real time filter
- Clickable URL links for all meta data as well as direct links to mod page on SpaceDock and Curse (click on verison number)
- Different ways of analysing the data, e.g:
  - Show all mods with aggregated metadata on one page
  - List mods for a specific repository (with aggregated metadata from other repositories if available)
  - List mods that only exists on a specific repository
- CSV export

 Now you can get a clear overview all all mods and the status in each repository, including easy access to relevant forum threads and source code.

### Stand-alone release for Windows
A stand-alone version of KSP Mod Analyzer can be downloaded from the "Releases" tab. Built with PyInstaller and can be run without having Python installed.

### Running the Python application on Linux/Windows
- Install latest version of Python 3
- Optional but recommended: Install PyCharm IDE
- Install the following packages:
  - `pip install PyQt5`
  - `pip install requests`
  - `pip install beautifulsoup4`
  - `pip install natsort`

- Clone the repo and run as follows (or run from PyCharm)
  - `git clone https://github.com/akej74/ksp-mod-analyzer.git`
  - `cd ksp-mod-analyzer`
  - `python3 ksp-mod-analyzer/main.py`

A `data` directory will be created in the current working directory to cache the downloads, so you should run it from the same directory each time.

### Note about "QT Designer"
- For editing the User Interface (`mainwindow.ui`), install QT Designer as follows:
  - Install latest QT5 open source suite from [QT main site](https://www.qt.io/)
  - In the install wizard, make sure you include the "Qt 5.3 MinGW" component
  - QT Designer will be installed in `C:\Qt\5.x\mingw53_32\bin\designer.exe`
  - Note that the executable is named "designer.exe"
- To convert the `mainwindow.ui` to `mainwindow.py`run the following command:
  - `<python installation directory>\Scripts\pyuic5.exe mainwindow.ui -o mainwindow.py`
