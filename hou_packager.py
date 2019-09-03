import json, os, sys
from pathlib_mate import Path
import PySide2.QtWidgets as qt
import PySide2.QtCore as qtcore

def get_root_dir():
   if (os.name == "posix" or os.name == "Darwin"):
      save_path = Path("~").expanduser()
      print(save_path)
   else:
      save_path = Path().home().joinpath("documents") #Path.expanduser("~") / "documents"
   return save_path

class Settings(object):
    def __init__(self):
       self.__configuration_path = Path(get_root_dir()) / "hou_packager.json"
       self.__packages_path = Path()

       #loading of config
       if self.__configuration_path.exists():
          with open(self.__configuration_path.abspath, "r") as f:
             data = json.load(f)
             self.__packages_path = Path(data["cfg_path"])
       else:
          #self.__configuration_path.touch()
          false_dir = True
          while false_dir:
            self.__packages_path = self.__request_dir__() ##gettting that folder from user
            files_to_check = self.__packages_path.iterdir()
            for f in files_to_check:
               if f.basename == "houdini.env":
                  false_dir = False
            self.dingus_box = qt.QMessageBox()
            self.dingus_box.setBaseSize(qtcore.QSize(360, 160))

            if false_dir:
               self.dingus_box.setText("Bad Folder")
               self.dingus_box.setInformativeText("Hey, you are a dingus!\nThat ain't a folder I've asked for!")
            else:
               self.dingus_box.setText("Done")
               self.dingus_box.setInformativeText("Config file has been created.\nIf you need to change the foder just delete hou_packager.json file.")
            self.dingus_box.exec_()

          with open(self.__configuration_path.abspath, "w") as f:
             new_dic = {}
             new_dic["cfg_path"] = self.__packages_path.abspath
             data = json.dumps(new_dic, indent=3)
             f.write(data)

    def __request_dir__(self):
       #return Path("/") ##TODO: add an interface to get dir
       return Path(Window().get_config_dir())

    def give_path(self):
       return self.__packages_path / "packages"

class Package(object):
   def __init__(self, path, package_name, data):
      self.__name = package_name
      self.__path = path
      self.__json_data = data

   def __save_changes(self):
      with open(self.__path.abspath, "w") as f:
         f.write(json.dumps(self.__json_data, indent=3))

   def just_save_all(self):
      self.__save_changes()

   def change_enable(self, value):
      self.__json_data["enable"] = value
      self.__save_changes()
      print("saved?")
      print(self.__json_data["enable"])

   def change_path(self, value):
      self.__json_data["path"] = value
      self.__save_changes()

   def give_enabled(self):
      return self.__json_data["enable"]

   def del_file(self):
      self.__path.remove()

def init_packages(folder):
   packages = {}
   if not folder.exists():
      folder.mkdir()
      return packages
   else:
      files = folder.iterdir()
      for f in files:
         path = Path(f)
         if path.ext == ".json":
            with open(path.abspath, "r") as f_read:
               data = json.load(f_read)
               if not "enable" in data.keys():
                  data["enable"] = True
               obj = Package(path, path.fname, data)
               packages[path.fname] = obj
      return packages

class DropZone(qt.QGroupBox):
   def __init__(self):
      super(DropZone, self).__init__()

      self.setTitle("Add new items:")

      self.m_layout = qt.QVBoxLayout()
      self.help_txt = qt.QLabel("Drag&Drop folders with otls/hda")
      self.help_txt.setAlignment(qtcore.Qt.AlignCenter)
      self.m_layout.addWidget(self.help_txt)
      self.setLayout(self.m_layout)

      self.setAcceptDrops(True)

   def dropEvent(self, event):
      if event.mimeData().hasUrls:
         event.accept()
         e_urls = event.mimeData().urls()
         self.add_new = False
         self.final_path = ""

         for f in e_urls:
            new_path = Path(f.toLocalFile())
            if new_path.is_dir():
               folder_content = new_path.iterdir()
               for iterated_file in folder_content:
                  if iterated_file.name == "otls" or iterated_file.name == "scripts" or iterated_file.name == "toolbar":
                     self.final_path = new_path
                     self.add_new = True
               if new_path.name == "otls":
                  self.final_path = new_path.parent
                  self.add_new = True

            if self.add_new:
               json_data = {}
               json_data["enable"] = True
               json_data["path"] = self.final_path.abspath
               json_file_path = str(packages_path / self.final_path.basename)
               json_file_path = Path(json_file_path + ".json")

               obj = Package(json_file_path , self.final_path.basename, json_data)
               obj.just_save_all()
               packages[self.final_path.basename] = obj
               window.load_newest(self.final_path.basename)

   def dragEnterEvent(self, event):
     if event.mimeData().hasUrls:
         event.accept()
     else:
         event.ignore()

class Entry(qt.QWidget):
   def __init__(self, enabled, name):
      super(Entry, self).__init__()

      self.__name = name
      self.__enable = enabled

      self.layout = qt.QHBoxLayout()
      self.setLayout(self.layout)

      self.o_enabled = qt.QCheckBox()
      if enabled:
         self.o_enabled.toggle()
      self.o_name = qt.QLabel(name)
      self.o_delete = qt.QPushButton("x")
      self.layout.addWidget(self.o_enabled, 0, 0)
      self.layout.addWidget(self.o_name, 1, 1)
      self.layout.addWidget(self.o_delete, 0)

      self.layout.setContentsMargins(10, 0, 10, 0)

      self.o_delete.clicked.connect(self.del_element)
      self.o_enabled.toggled.connect(self.change_enable)

   def del_element(self):
      packages[self.__name].del_file()
      self.close()

   def change_enable(self):
      if self.__enable:
         self.__enable = False
      else:
         self.__enable = True
      packages[self.__name].change_enable(self.__enable)

class Window(qt.QMainWindow):
   def __init__(self):
      super(Window, self).__init__()
      self.setWindowTitle("Houdini Packager")
      self.setFixedWidth(300)
      self.q = qt.QWidget()
      self.q.setSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Fixed)
      self.window_layout = qt.QVBoxLayout()
      self.q.setLayout(self.window_layout)
      self.setCentralWidget(self.q)

      self.gb = qt.QGroupBox()
      self.gb.setTitle("Found packages:")
      self.window_layout.addWidget(self.gb)

      self.main_layout = qt.QVBoxLayout()
      self.gb.setLayout(self.main_layout)


   def get_config_dir(self):
      self.intro_text = "Seems like you are using this application for a first time. Please, specify the Houdini config folder where you have ""houdini.env"" file."

      if (os.name == "posix" or os.name == "Darwin"):
         get_path = Path().home().joinpath("Library/Preferences/houdini/") #Path("~").expanduser()
      else:
         get_path = Path().home().joinpath("documents") #Path.expanduser("~") / "documents"

      self.intro = qt.QMessageBox()
      self.intro.setBaseSize(qtcore.QSize(360, 180))
      self.intro.setText("Choose Houdini config folder")
      self.intro.setInformativeText(self.intro_text)
      self.reaction = self.intro.exec_()
      if self.reaction == 1024:
         self.path_btn = qt.QFileDialog.getExistingDirectory(self, "Open Image", str(get_path))
      else:
         self.path_btn = ""

      return self.path_btn

   def load_entries(self):
      for pack in packages.keys():
         x = Entry(packages[pack].give_enabled(), str(pack))
         self.main_layout.addWidget(x)

      self.droppy = DropZone()

      self.space = qt.QSpacerItem(0, 40, qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
      self.window_layout.addSpacerItem(self.space)
      self.q_button = qt.QPushButton("Save and Close")
      self.q_button.clicked.connect(self.button_clicked)
      self.window_layout.addWidget(self.droppy)
      self.window_layout.addWidget(self.q_button)

      self.main_layout.setContentsMargins(10, 10, 0, 0)

   def load_newest(self, value):
      x = Entry(packages[value].give_enabled(), str(value))
      self.main_layout.addWidget(x)

   def button_clicked(self):
      self.close()


if __name__ == "__main__":
   app = qt.QApplication([])
   if getattr(sys, "frozen", False):
      qt.QApplication.addLibraryPath(sys._MEIPASS)

   window = Window()

   packages_path = Settings().give_path()
   packages = init_packages(packages_path)

   window.load_entries()
   window.show()
   app.exec_()