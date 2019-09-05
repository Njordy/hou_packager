# hou_packager
 A simple SideFX Houdini package manager. 
 It lets the user to easily "install", disable or delete any (ready) Houdini HDA libraries.  

## Instlallation
In order to execute the script you would need to have Python3 installed on a system, as well as this packages: pathlib-mate, PySide2.
It can be easily done entering this into your terminal (via pip):
* `pip install pathlib-mate`
* `pip install PySide2`
 
After this sorted out you should feed the path to .py script to pythinw.exe.

## Usage
Then you open the application for the first time you will be asked to specify the Houdini config folder (place where "houdini.env" file is situated). This path variable will be written in hou_packager.json file in your Documents folder. If application doesn't work correctly, it's probably because the path is incorrect. You can edit the JSON file manually, or just delete for a clean start of the app. 

*Windows*
`%HOME%/houdiniX.X/`

*macOS*
`~/Library/Preferences/houdini/X.X`

*Linux*
`~/houdiniX.X/`

This [Houdini Package](http://www.sidefx.com/docs/houdini/ref/plugins.html) system is basically just a JSON file wilth a few variables. hou_packager helps you to skip the manial job of creating a file, and writing a path to an HDA folder by yourself. You can just drop beforementioned foler into th dropzone of the application and it's done. 
The folder *must* obey the houdini structure: `[folder name]/[otls]/*` or it won't work.

## Download

If you ain't a big on compiling it yourself, or interpreting via pythonw... well, take it from "Releases" page above, buddy. If you are a linux user, you have compiled it by now :)
