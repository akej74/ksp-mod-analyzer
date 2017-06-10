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
 
 Now you can get a clear overview all all mods and the status in each repository, including easy access to relevant forum threads and source code.

### Stand-alone release
A stand-alone version of KSP Mod Analyzer can be downloaded from the "Releases" tab. Built with PyInstaller and can be run without having Python installed.

### Design
- Python 3 with PyQt 5 for the user interface
