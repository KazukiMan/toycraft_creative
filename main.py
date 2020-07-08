# -*- coding: utf-8 -*-

#===========================================
#
#       Update Assistant Project - a auto update and installer solution for minecraft server update 
#       By Kazuki Amakawa (github.com/KazukiMan)
#
#       Connect us: Github: https://www.github.com/KazukiMan
#                   Main: KazukiAmakawa@gmail.com
#
#===========================================

import requests 
import os
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt
import json
import time
import shutil
import zipfile
import time 
from pathlib import Path
import webbrowser



TOOL_LOCATION = ""
FOR_TEST = False
CONNECT_INFO = "Copyright by Kazuki Amakawa \n\n Github: https://www.github.com/KazukiMan \n Mail: KazukiAmakawa@gmail.com\n\n Version: "



class default_setting():
    def __init__(self):
        #version_setting
        self.VERSION = ""
        self.WEB_SPONSOR_WEB = ""
        self.MAIN_SOURCE_JSON_FILE_WEB = ""
        self.INITIALIZATION_SITE = ""
        self.ADDONES_SITE = ""

        #default setting
        self.DEFAULT_LOC = ""
        self.DEFAULT_LANG = ""
        self.HAND_UPDATE_VERSION = ""


    def initialization_setting(self):
        filename = os.path.join(TOOL_LOCATION, ".inits", "version_setting.json")
        file = open(filename, "r")
        line = file.readline()
        file.close()
        decoded_hand = json.loads(line)

        self.VERSION = decoded_hand["VERSION"]
        self.WEB_SPONSOR_WEB = decoded_hand["WEB_SPONSOR_WEB"]
        self.MAIN_SOURCE_JSON_FILE_WEB = decoded_hand["MAIN_SOURCE_JSON_FILE_WEB"]
        self.INITIALIZATION_SITE = decoded_hand["INITIALIZATION_SITE"]
        self.ADDONES_SITE = decoded_hand["ADDONES_SITE"]
        
        filename = os.path.join(TOOL_LOCATION, ".inits", "default_setting.json")
        file = open(filename, "r")
        line = file.readline()
        file.close()
        decoded_hand = json.loads(line)

        self.DEFAULT_LOC = decoded_hand["DEFAULT_LOC"]
        self.DEFAULT_LANG = decoded_hand["DEFAULT_LANG"]
        self.HAND_UPDATE_VERSION = decoded_hand["HAND_UPDATE_VERSION"]
        return 



    def refresh_setting(self):
        data = []
        data.append({
            "VERSION": self.VERSION,
            "WEB_SPONSOR_WEB": self.WEB_SPONSOR_WEB,
            "MAIN_SOURCE_JSON_FILE_WEB": self.MAIN_SOURCE_JSON_FILE_WEB,
            "INITIALIZATION_SITE": self.INITIALIZATION_SITE,
            "ADDONES_SITE": self.ADDONES_SITE
            })
        
        filename = os.path.join(TOOL_LOCATION, ".inits","version_setting.json")
        with open(filename, "w") as file:
            json.dump(data[0], file)

        data = []
        data.append({
            "DEFAULT_LOC": self.DEFAULT_LOC,
            "DEFAULT_LANG": self.DEFAULT_LANG,
            "HAND_UPDATE_VERSION": self.HAND_UPDATE_VERSION
            })
        
        filename = os.path.join(TOOL_LOCATION, ".inits","default_setting.json")
        with open(filename, "w") as file:
            json.dump(data[0], file)

        self.initialization_setting()
SETTING = default_setting()



def download_file(url, filename, LANG):
    try:
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
    except:
        error_warning(LANG.STR_NOT_CONNECT)
    return 



def clear_all():
    try:
        shutil.rmtree(os.path.join(TOOL_LOCATION, ".config"))
    except:
        pass
    try:
        shutil.rmtree(os.path.join(TOOL_LOCATION, ".Download"))
    except:
        pass
    try:
        os.mkdir(os.path.join(TOOL_LOCATION, ".config"))
    except:
        pass
    try:
        os.mkdir(os.path.join(TOOL_LOCATION, ".Download"))
    except:
        pass
    return



def error_warning(warning_info):
    app = QtWidgets.QApplication([])

    error_dialog = QtWidgets.QErrorMessage()
    error_dialog.showMessage(warning_info)
    app.exec_()
    clear_all() 
    sys.exit()
    return



def SystemJudge():
    import platform  
    Str = platform.system() 
    if Str[0] == "w" or Str[0] == "W":
        return "Dos"
    elif Str == "Darwin": 
        return "Darwin"
    else:
        return "Linux"



def pre_read_json(filename):
    file = open(filename, "r", encoding="utf-8")
    str_json = ""
    while 1:
        line =file.readline()
        if not line:
            break 
        str_json += line[0:-1]

    return str_json



def read_package_list_json(package_list_loc):
    strJson = pre_read_json(package_list_loc)
    decoded_hand = json.loads(strJson)

    package_name = []
    package_site = []
    package_info = []
    latest_site = []
    for i in range(0, len(decoded_hand["package_list"])):
        package_name.append(decoded_hand["package_list"][i]["package_name"])
        package_site.append(decoded_hand["package_list"][i]["download_list"])
        package_info.append(decoded_hand["package_list"][i]["package_info"])
        latest_site.append(decoded_hand["package_list"][i]["latest_list"])
    return package_name, package_site, package_info, latest_site



def operation_main_function(command_list, client_route):
    #Analysis command and combine files/folder route
    combo_command = []
    tmp_string = ""
    for i in range(0, len(command_list)):
        if    command_list[i] == "-cp":
            combo_command.append("-cp")
        elif  command_list[i] == "-mv":
            combo_command.append("-mv")
        elif  command_list[i] == "-rm":
            combo_command.append("-rm")
        elif  command_list[i] == "-mkdir":
            combo_command.append("-mkdir")
        elif  command_list[i] == "-r":
            combo_command.append("-r")
        elif  command_list[i] == "-unzip":
            combo_command.append("-unzip")
        elif  command_list[i] == "-tool":
            tmp_string = os.path.join(tmp_string, TOOL_LOCATION)
        elif  command_list[i] == "-client":
            tmp_string = os.path.join(tmp_string, client_route)
        elif  command_list[i] == "-to":
            combo_command.append(tmp_string)
            tmp_string = ""
        else:
            tmp_string = os.path.join(tmp_string, command_list[i])
        
        if i+1 == len(command_list):
            combo_command.append(tmp_string)
            break
    #print(combo_command)


    #Operation
    if combo_command[0] == "-cp":
        if combo_command[1] == "-r":
            try:
                shutil.copytree(combo_command[2], combo_command[3])
            except:
                try:
                    shutil.rmtree(combo_command[3])
                    shutil.copytree(combo_command[2], combo_command[3])
                except:
                    pass
        else:
            try:
                shutil.copyfile(combo_command[1], combo_command[2])
            except:
                try:
                    os.remove(combo_command[2])
                    shutil.copyfile(combo_command[1], combo_command[2])
                except:
                    pass
    elif combo_command[0] == "-mv":
        if combo_command[1] == "-r":
            try:
                shutil.move(combo_command[2], combo_command[3])
            except:
                pass
        else:
            try:
                shutil.move(combo_command[1], combo_command[2])
            except:
                pass
    elif combo_command[0] == "-rm":
        if combo_command[1] == "-r":
            try:
                shutil.rmtree(combo_command[2])
            except:
                pass
        else:
            try:
                os.remove(combo_command[1])
            except:
                pass
    elif combo_command[0] == "-mkdir":
        try:
            os.mkdir(combo_command[1])    
        except:
            pass
    elif combo_command[0] == "-unzip":
        try:
            os.mkdir(combo_command[2])
        except:
            pass
        try:
            with zipfile.ZipFile(combo_command[1], 'r') as zip_ref:
                zip_ref.extractall(combo_command[2])
        except:
            pass



def get_version_and_json(jsonfile_location):
    strJson = pre_read_json(jsonfile_location)
    decoded_hand = json.loads(strJson)

    return decoded_hand["package_version"], decoded_hand["last_version"], decoded_hand



def read_todo_json(jsonfile_location):
    version, last_version, decoded_hand = get_version_and_json(jsonfile_location)
    download_list = []
    download_site = []
    for i in range(len(decoded_hand["package_download"])):
        download_list.append(decoded_hand["package_download"][i]["filename"])
        download_site.append(decoded_hand["package_download"][i]["download"])
    return version, last_version, download_list, download_site, decoded_hand["package_operation"]



class LANG_CLASS():
    def __init__(self):
        global SETTING

        self.STR_LANGUAGE_NAME_ASSETS = []
        self.STR_LANGUAGE_LOCATION = []

        self.NAME_CODE = int(SETTING.DEFAULT_LANG)

        self.STR_LANGUAGE_NAME = ""
        self.STR_NOT_CONNECT = ""
        self.STR_TITLE = ""
        self.STR_ASK_FOR_EXIT = ""
        self.STR_START_INSTALL = ""
        self.STR_OPEN_FOLDER = ""
        self.STR_FOLDER_MSG = ""
        self.STR_CHOOSE_FOLDER = ""
        self.STR_SET_PACKAGE = ""
        self.STR_SET_MODS = ""
        self.STR_UPDATE_BUTTON = ""
        self.STR_CONNECT_US = ""
        self.STR_SPONSOR_US = ""
        self.STR_TP_SELF_MOD = ""
        self.STR_TP_SCREEN = ""
        self.STR_COMMAND_ERROR = ""
        self.STR_DELETE_FOLDER = ""
        self.STR_DELETE_GAME_CHECK = ""
        self.STR_GAME_NOT_EXISTS = ""
        self.STR_PREPARED = ""
        self.STR_GAMEFILE_NOT_EXISTS = ""
        self.STR_INSTALL_TITLE = ""
        self.STR_INSTALL_TITLE_2 = ""
        self.STR_DOWNLOAD_1 = ""
        self.STR_DOWNLOAD_2 = ""
        self.STR_DOWNLOAD_3 = ""
        self.STR_INSTALL_1 = ""
        self.STR_INSTALL_2 = ""
        self.STR_INSTALL_3 = ""
        self.STR_INSTALL_END = ""
        self.STR_UPDATE_TITLE = ""
        self.STR_UPDATE = ""
        self.STR_UPDATE_END = ""
        self.STR_HAND_UPDATE = ""
        self.JAVA_NOT_INSTALL = ""
        self.UPDATE_NORMAl = ""



    def build_lang(self):
        filename = os.path.join(TOOL_LOCATION, self.STR_LANGUAGE_LOCATION[self.NAME_CODE])
        strJson = pre_read_json(filename)
        decoded_hand = json.loads(strJson)

        self.STR_LANGUAGE_NAME = decoded_hand["STR_LANGUAGE_NAME"]
        self.STR_NOT_CONNECT = decoded_hand["STR_NOT_CONNECT"]
        self.STR_TITLE = decoded_hand["STR_TITLE"]
        self.STR_ASK_FOR_EXIT = decoded_hand["STR_ASK_FOR_EXIT"]
        self.STR_START_INSTALL = decoded_hand["STR_START_INSTALL"]
        self.STR_OPEN_FOLDER = decoded_hand["STR_OPEN_FOLDER"]
        self.STR_FOLDER_MSG = decoded_hand["STR_FOLDER_MSG"]
        self.STR_CHOOSE_FOLDER = decoded_hand["STR_CHOOSE_FOLDER"]
        self.STR_SET_PACKAGE = decoded_hand["STR_SET_PACKAGE"]
        self.STR_SET_MODS = decoded_hand["STR_SET_MODS"]
        self.STR_UPDATE_BUTTON = decoded_hand["STR_UPDATE_BUTTON"]
        self.STR_CONNECT_US = decoded_hand["STR_CONNECT_US"]
        self.STR_SPONSOR_US = decoded_hand["STR_SPONSOR_US"]
        self.STR_TP_SELF_MOD = decoded_hand["STR_TP_SELF_MOD"]
        self.STR_TP_SCREEN = decoded_hand["STR_TP_SCREEN"]
        self.STR_COMMAND_ERROR = decoded_hand["STR_COMMAND_ERROR"]
        self.STR_DELETE_FOLDER = decoded_hand["STR_DELETE_FOLDER"]
        self.STR_DELETE_GAME_CHECK = decoded_hand["STR_DELETE_GAME_CHECK"]
        self.STR_GAME_NOT_EXISTS = decoded_hand["STR_GAME_NOT_EXISTS"]
        self.STR_PREPARED = decoded_hand["STR_PREPARED"]
        self.STR_GAMEFILE_NOT_EXISTS = decoded_hand["STR_GAMEFILE_NOT_EXISTS"]
        self.STR_INSTALL_TITLE = decoded_hand["STR_INSTALL_TITLE"]
        self.STR_INSTALL_TITLE_2 = decoded_hand["STR_INSTALL_TITLE_2"]
        self.STR_DOWNLOAD_1 = decoded_hand["STR_DOWNLOAD_1"]
        self.STR_DOWNLOAD_2 = decoded_hand["STR_DOWNLOAD_2"]
        self.STR_DOWNLOAD_3 = decoded_hand["STR_DOWNLOAD_3"]
        self.STR_INSTALL_1 = decoded_hand["STR_INSTALL_1"]
        self.STR_INSTALL_2 = decoded_hand["STR_INSTALL_2"]
        self.STR_INSTALL_3 = decoded_hand["STR_INSTALL_3"]
        self.STR_INSTALL_END = decoded_hand["STR_INSTALL_END"]
        self.STR_UPDATE_TITLE = decoded_hand["STR_UPDATE_TITLE"]
        self.STR_UPDATE = decoded_hand["STR_UPDATE"]
        self.STR_UPDATE_END = decoded_hand["STR_UPDATE_END"]
        self.STR_HAND_UPDATE = decoded_hand["STR_HAND_UPDATE"]
        self.JAVA_NOT_INSTALL = decoded_hand["JAVA_NOT_INSTALL"]
        self.UPDATE_NORMAl = decoded_hand["UPDATE_NORMAl"]



    def init_language_setting(self):
        dir_name = os.path.join(TOOL_LOCATION, ".inits", "languages")
        for parent, dirs, files in os.walk(dir_name):
            for file in files:
                strJson = pre_read_json(os.path.join(TOOL_LOCATION, ".inits", "languages", file))
                decoded_hand = json.loads(strJson)
                self.STR_LANGUAGE_NAME_ASSETS.append(decoded_hand["STR_LANGUAGE_NAME"])
                self.STR_LANGUAGE_LOCATION.append(os.path.join(TOOL_LOCATION, ".inits", "languages", file))
        self.build_lang()



class MainWindow(QtWidgets.QWidget):
    def __init__(self, package_name, package_info, package_loc, latest_loc, latest_site, LANG):
        super().__init__()
        self.package_name = package_name
        self.package_info = package_info
        self.package_loc = package_loc
        self.latest_loc = latest_loc
        self.latest_site = latest_site
        self.LANG = LANG
        self.initUI()



        
    def initUI(self):        
        self.resize(400, 600)
            #Setting default size
        self.center()
            #Setting default location
        self.setWindowTitle(self.LANG.STR_TITLE)
            #Setting window title
        self.topFiller = QtWidgets.QWidget()
        self.topFiller.setMinimumSize(250, 2000)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.topFiller)
            #Add Scroll Area
        self.vbox_final = QtWidgets.QVBoxLayout()
        

        # Define title ad image label
        self.img = QtGui.QPixmap(os.path.join(TOOL_LOCATION, ".inits", "img", "ad_img.png"))
            #Read image
        self.label_img = QtWidgets.QLabel(self)
            #Builc empty label
        self.label_img.setPixmap(self.img)
            #Fill image into label
        self.label_img.setScaledContents (True)
            #Set autosize of image
        
        self.hbox_label_img = QtWidgets.QHBoxLayout()
            #Define box for image
        self.hbox_label_img.addWidget(self.label_img)
            #Add image to box
        self.vbox_final.addLayout(self.hbox_label_img)
            #Add label img box to final box



        # Define location buttom
        self.label_location_pre = QtWidgets.QLabel(self)
            #Builc empty label - location of install
        self.label_location_pre.setText(self.LANG.STR_FOLDER_MSG)
            #Set label msg

        self.label_location = QtWidgets.QLabel(self)
            #Build empty label
        self.label_location.setText(SETTING.DEFAULT_LOC)
            #Setting default msg

        self.direction_button = QtWidgets.QPushButton(self.LANG.STR_OPEN_FOLDER)
            #Builc buttom for - open folder for install 
        self.direction_button.clicked.connect(self.get_folder)
            #Refresh the location for install
        
        self.hbox_direction = QtWidgets.QHBoxLayout()
            #Define box for add location
        self.hbox_direction.addWidget(self.label_location_pre)
            #Add intro info
        self.hbox_direction.addWidget(self.label_location)
            #Add location info
        self.hbox_direction.addStretch(1)
            #Setting structure
        self.hbox_direction.addWidget(self.direction_button)
            #Add change location button
        self.vbox_final.addLayout(self.hbox_direction)
            #Add direction box to final box



        # Define package choose list
        self.label_combo_box_pre = QtWidgets.QLabel(self)
            #Build empty label - for choose package
        self.label_combo_box_pre.setText(self.LANG.STR_SET_PACKAGE)
            #Set text

        self.combo_box = QtWidgets.QComboBox(self)
            #Build combo box for package choose
        self.combo_box.addItems(self.package_name)
            #Add json info into box
        self.combo_box.currentTextChanged.connect(self.change_package_intro)
            #refresh the box info

        self.label_combo_box_intro = QtWidgets.QLabel(self)
            #Build empty label - for package introduction
        self.label_combo_box_intro.setText(self.package_info[self.combo_box.currentIndex()])
            #Set default info

        self.vbox_final.addWidget(self.label_combo_box_pre)
            #Add package choose combobox msg
        self.vbox_final.addWidget(self.combo_box)
            #Add combo box identity
        self.vbox_final.addWidget(self.label_combo_box_intro)
            #Add package introduction
        self.vbox_final.addStretch(1)
            #Setting structure



        # Define info for installer and upgrade 
        self.install_package = QtWidgets.QLabel(self)
            #Build empty label
        self.install_package.setText(self.LANG.STR_PREPARED)
            #Setting default msg
        self.operation_info = QtWidgets.QLabel(self)
        self.vbox_final.addWidget(self.install_package)
        self.vbox_final.addWidget(self.operation_info)



        # Define buttons
        self.connect_button = QtWidgets.QPushButton(self.LANG.STR_CONNECT_US)
            #Define button to connect us
        self.connect_button.clicked.connect(self.connect_information)
            #Connect to information page
        
        self.sponsor_button = QtWidgets.QPushButton(self.LANG.STR_SPONSOR_US)
            #Define button sponsor us
        self.sponsor_button.clicked.connect(self.open_sponsor_page)
            #Connect to sonsor page
       
        #self.tp_screen_shot = QtWidgets.QPushButton(self.LANG.STR_TP_SCREEN)
        self.tp_screen_shot = QtWidgets.QPushButton()
            #Define button tp to screenshot folder

        self.tp_self_mod_button = QtWidgets.QComboBox(self)
            #Build combo box for package choose
        self.LANG.STR_LANGUAGE_NAME_ASSETS.append("Language")
        self.tp_self_mod_button.addItems(self.LANG.STR_LANGUAGE_NAME_ASSETS)
        self.tp_self_mod_button.setCurrentIndex(len(self.LANG.STR_LANGUAGE_NAME_ASSETS) - 1)
            #Add json info into box
        self.tp_self_mod_button.currentTextChanged.connect(self.language_change)
            #refresh the box info

        self.update_button = QtWidgets.QPushButton(self.LANG.STR_UPDATE_BUTTON)
            #Define button for update
        self.update_button.clicked.connect(self.update_start)
            #Connect to game function

        self.ok_button = QtWidgets.QPushButton(self.LANG.STR_START_INSTALL)
            #Define button for final install
        self.ok_button.clicked.connect(self.installer)
            #Connect to installer function



        self.hbox_tmp1 = QtWidgets.QHBoxLayout()
            #Define box1 for first 2 button
        self.hbox_tmp1.addWidget(self.tp_screen_shot)
            #Add button staff/screenshot/startgame to tmp1 box
        self.hbox_tmp1.addWidget(self.connect_button)
            #Add button staff/screenshot/startgame to tmp1 box
        self.hbox_tmp1.addWidget(self.update_button)
            #Add button staff/screenshot/startgame to tmp1 box
        self.hbox_tmp2 = QtWidgets.QHBoxLayout()
            #Define box2 for last 2 button
        self.hbox_tmp2.addWidget(self.tp_self_mod_button)
            #Add button sponsor/selfmod/installgame to tmp2 box
        self.hbox_tmp2.addWidget(self.sponsor_button)
            #Add button sponsor/selfmod/installgame to tmp2 box
        self.hbox_tmp2.addWidget(self.ok_button)
            #Add button sponsor/selfmod/installgame to tmp2 box

        self.vbox_final.addLayout(self.hbox_tmp1)
            #Add tmp1/tmp2 to vbox
        self.vbox_final.addLayout(self.hbox_tmp2)
            #Add tmp1/tmp2 to vbox



        self.setLayout(self.vbox_final)    
        self.show()

                

    """
    Functions for box identity
    """
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

    """
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '', LANG.STR_ASK_FOR_EXIT, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()     
    """


    """
    Functions for opeartion(except install and upgrade)
    """
    def get_folder(self):
        self.install_dir = QtWidgets.QFileDialog.getExistingDirectory(self, self.LANG.STR_CHOOSE_FOLDER, TOOL_LOCATION)
        self.label_location.setText(self.install_dir)
        SETTING.DEFAULT_LOC = self.install_dir
        SETTING.refresh_setting()
        INSTALL_LOCATION = self.install_dir
        filename = os.path.join(TOOL_LOCATION, ".inits", "default_loc")
        file = open(filename, "w", encoding="utf-8")
        file.write(self.install_dir)
        return 



    def change_package_intro(self):
        self.label_combo_box_intro.setText(self.package_info[self.combo_box.currentIndex()])
        return 



    def language_change(self):
        if self.tp_self_mod_button.currentIndex() == len(self.LANG.STR_LANGUAGE_NAME_ASSETS) - 1:
            return 
        else:
            SETTING.DEFAULT_LANG = str(self.tp_self_mod_button.currentIndex())
            SETTING.refresh_setting()
        return 



    def check_game_exists(self):
        filename = os.path.join(SETTING.DEFAULT_LOC, ".minecraft", ".installer.cfg")
        if not os.path.exists(filename):
            return ""
        file = open(filename, "r", encoding="utf-8")
        line = file.readline()
        file.close()
        
        return_line = ""
        for i in range(0, len(self.package_name)):
            #print(line, self.package_name)
            #time.sleep(1)
            if self.package_name[i] == line:
                return_line = line
                break
        
        return return_line



    """
    Functions for install and upgrade - main todo operation
    """
    def todo_main(self, version, last_version, download_list, download_site, operation_list, client_route):
        #Download files
        for i in range(len(download_list)):
            self.operation_info.setText(self.LANG.STR_DOWNLOAD_1 + str(i+1) + self.LANG.STR_DOWNLOAD_2 + str(len(download_list))+ self.LANG.STR_DOWNLOAD_3)
            QtWidgets.QApplication.processEvents()
            #print("正在下载：第" + str(i+1) + "项，共" + str(len(download_list))+ "项")
            current_download_location = os.path.join(TOOL_LOCATION, ".Download", download_list[i])
            download_file(download_site[i], current_download_location, self.LANG)

        #Command processing
        for i in range(len(operation_list)):    
            self.operation_info.setText(self.LANG.STR_INSTALL_1 + str(i+1) + self.LANG.STR_INSTALL_2 + str(len(operation_list))+ self.LANG.STR_INSTALL_3)
            QtWidgets.QApplication.processEvents()
            #print("正在安装文件：第" + str(i+1) + "项，共" + str(len(operation_list))+ "项")
            operation_main_function(operation_list[i], client_route)
        self.operation_info.setText("")




    """
    Functions for install and upgrade
    """
    def installer(self):
        #Analysis Json Files
        #print(self.default_route)
        package_installed_name = self.check_game_exists()
        if len(package_installed_name) != 0:
            reply = QtWidgets.QMessageBox.question(self, '', self.LANG.STR_DELETE_GAME_CHECK, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)    
            if reply == QtWidgets.QMessageBox.No:
                return
        else:
            reply = QtWidgets.QMessageBox.question(self, '', self.LANG.STR_DELETE_FOLDER, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                return

        try:
            shutil.rmtree(SETTING.DEFAULT_LOC)
        except:
            pass

        try:
            os.mkdir(SETTING.DEFAULT_LOC)
        except:
            pass
        
        self.install_package.setText(self.LANG.STR_INSTALL_TITLE + package_installed_name + self.LANG.STR_INSTALL_TITLE_2)
        QtWidgets.QApplication.processEvents()

        jsonfile_location = self.package_loc[self.combo_box.currentIndex()]
        version, last_version, download_list, download_site, main_processing = read_todo_json(jsonfile_location)
        pro_processing = [
        ["-unzip", "-tool", ".inits", "1.12.2-full.zip", "-to", "-tool", ".Download"],
        ["-cp", "-r", "-tool", ".Download", "1.12.2-full", ".minecraft",       "-to", "-client", ".minecraft"],
        ["-cp",       "-tool", ".Download", "1.12.2-full", "HMCL-3.2.149.jar", "-to", "-client", "HMCL.jar"],
        ["-cp",       "-tool", ".Download", "1.12.2-full", "HMCL-3.2.139.exe", "-to", "-client", "HMCL.exe"]
        ]
        post_processing = [
        ["-cp",       "-tool", jsonfile_location, "-to", "-client", ".minecraft", self.package_name[self.combo_box.currentIndex()]+"-latest.json"]
        ]
        operation_list = pro_processing + main_processing + post_processing
        res = self.todo_main(version, last_version, download_list, download_site, operation_list, SETTING.DEFAULT_LOC)
        filename = ".installer.cfg"
        filename = os.path.join(SETTING.DEFAULT_LOC, ".minecraft", ".installer.cfg")
        file = open(filename, "w", encoding="utf-8")
        file.write(self.package_name[self.combo_box.currentIndex()])
        file.close()
        
        self.install_package.setText(self.LANG.STR_INSTALL_END)
        QtWidgets.QApplication.processEvents()

        return 



    """
    Update Part
    """
    def update_start(self):
        #self.install_package.setText("sb1")
        #QtWidgets.QApplication.processEvents()
        #time.sleep(5)
        package_installed_name = self.check_game_exists()
        if len(package_installed_name) == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText(self.LANG.STR_GAME_NOT_EXISTS)
            msgBox.exec_()
            return

        #self.install_package.setText("sb12")
        #QtWidgets.QApplication.processEvents()
        #time.sleep(5)
        kase = 0
        for i in range(0, len(self.package_name)):
            if self.package_name[i] == package_installed_name:
                kase = i
                break
      
        #self.install_package.setText("sb3")
        #QtWidgets.QApplication.processEvents()
        #time.sleep(5)
        #print(kase)
        json_installed_version, _, _ = get_version_and_json(os.path.join(SETTING.DEFAULT_LOC, ".minecraft", package_installed_name+"-latest.json"))
        json_version_stack = []
        json_current_version, json_last_version, _ = get_version_and_json(os.path.join(TOOL_LOCATION, ".config", package_installed_name+"-latest.json"))
        

        while 1:
            if json_current_version == json_installed_version:
                break
            if len(json_version_stack) == 0:
                json_version_stack.append("-latest")
            else:
                json_version_stack.append(json_current_version)

            self.install_package.setText(self.LANG.STR_UPDATE_TITLE)
            QtWidgets.QApplication.processEvents()
            #print("正在下载更新数据库：" +  package_installed_name+json_last_version+".json")

            download_file(self.latest_site[kase] + json_last_version+".json", os.path.join(TOOL_LOCATION, ".config", package_installed_name+json_last_version+".json"), self.LANG)
            json_current_version, json_last_version, _ = get_version_and_json(os.path.join(TOOL_LOCATION, ".config", package_installed_name+json_last_version+".json"))

        if len(json_version_stack) != 0:
            for i in range(len(json_version_stack)-1, -1, -1):
                jsonfile_location = os.path.join(TOOL_LOCATION, ".config", package_installed_name+json_version_stack[i]+".json")
                
                self.install_package.setText(self.LANG.STR_UPDATE + json_version_stack[i])
                QtWidgets.QApplication.processEvents()
                #print("正在更新版本至 "+ json_version_stack[i]+" 版本")

                version, last_version, download_list, download_site, main_processing = read_todo_json(jsonfile_location)
                pro_processing = []
                post_processing = [
                ["-rm",       "-client", ".minecraft", package_installed_name+"-latest.json"],
                ["-cp",       "-tool", ".config", package_installed_name+json_version_stack[i]+".json", "-to", "-client", ".minecraft", package_installed_name+"-latest.json"]
                ]
                operation_list = pro_processing + main_processing + post_processing

                res = self.todo_main(version, last_version, download_list, download_site, operation_list, SETTING.DEFAULT_LOC)

        self.install_package.setText(self.LANG.STR_UPDATE_END)
        QtWidgets.QApplication.processEvents()
        if FOR_TEST:
            os.system("open " + os.path.join(SETTING.DEFAULT_LOC, "HMCL.jar"))
        else:
            if SystemJudge() == "Doc":
                os.system(os.path.join(SETTING.DEFAULT_LOC, "HMCL.exe"))
            elif SystemJudge() == "Darwin":
                os.system("open " + os.path.join(SETTING.DEFAULT_LOC, "HMCL.jar"))
                #game_start_path = os.path.join(SETTING.DEFAULT_LOC, "HMCL.jar")
                #os.system("cd " + SETTING.DEFAULT_LOC + " && java -jar " + game_start_path)
            else:
                game_start_path = os.path.join(SETTING.DEFAULT_LOC, "HMCL.jar")
                os.system("cd " + SETTING.DEFAULT_LOC + " && java -jar " + game_start_path)
            #print("正在启动游戏")
        return 



    def open_sponsor_page(self):
        webbrowser.open(SETTING.WEB_SPONSOR_WEB)
        return 



    def connect_information(self):
        QtWidgets.QMessageBox.about(self, '', CONNECT_INFO + SETTING.VERSION) 
        return



class initialization_window(QtWidgets.QWidget):
    def __init__(self, LANG, open_cmd_head):
        super().__init__()
        self.LANG = LANG
        self.open_cmd_head = open_cmd_head
        self.initUI()



    def initUI(self):        
        self.resize(400, 600)
            #Setting default size
        self.center()
            #Setting default location
        self.setWindowTitle(self.LANG.STR_TITLE)
            #Setting window title
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)

        self.topFiller = QtWidgets.QWidget()
        self.topFiller.setMinimumSize(250, 2000)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.topFiller)
            #Add Scroll Area
        self.vbox_final = QtWidgets.QVBoxLayout()
        
        # Define info for installer and upgrade 
        self.install_package = QtWidgets.QLabel(self)
            #Build empty label
        self.install_package.setText(self.LANG.STR_PREPARED)
            #Setting default msg
        self.operation_info = QtWidgets.QLabel(self)
        self.vbox_final.addWidget(self.install_package)
        self.vbox_final.addWidget(self.operation_info)

        self.setLayout(self.vbox_final)    
        self.show()
        self.update_mainprocessing()



    def update_preprocessing(self):
        # Check hand by update finished or not
        if len(SETTING.HAND_UPDATE_VERSION) != 0:
            #print(SETTING.HAND_UPDATE_VERSION)
            #print(SETTING.VERSION)
            if SETTING.HAND_UPDATE_VERSION != SETTING.VERSION:
                #print("sb")
                os.system(self.open_cmd_head + " " + os.path.join(TOOL_LOCATION, ".inits", "minecraft-new"))
                self.close()
                error_warning(self.LANG.STR_HAND_UPDATE)

            else:
                #print("sjb")
                try:
                    shutil.rmtree(os.path.join(TOOL_LOCATION, ".inits", "minecraft-new"))
                except:
                    pass
                SETTING.VERSION = SETTING.HAND_UPDATE_VERSION
                SETTING.HAND_UPDATE_VERSION = ""
                SETTING.refresh_setting()
                time.sleep(3)

        # Download assistant update config
        self.install_package.setText(self.LANG.STR_UPDATE_TITLE + "1/2")
        QtWidgets.QApplication.processEvents()
        #print("正在获取更新文件 1/2")
        assistant_loc = os.path.join(TOOL_LOCATION, ".config", "assistant_latest.json")
        if os.path.exists(os.path.join(TOOL_LOCATION, "main.py")):
            download_file(SETTING.INITIALIZATION_SITE+"/assistant_latest_source.json", assistant_loc, self.LANG)
        else:
            if SystemJudge() == "Dos":
                download_file(SETTING.INITIALIZATION_SITE+"/assistant_latest_win.json", assistant_loc, self.LANG)
            elif SystemJudge() == "Darwin":
                download_file(SETTING.INITIALIZATION_SITE+"/assistant_latest_mac.json", assistant_loc, self.LANG)
            else:
                #download_file(SETTING.INITIALIZATION_SITE+"assistant_latest_rpm.json", assistant_loc, LANG)
                pass



    def update_mainprocessing(self):
        self.update_preprocessing()

        true_download_list = []
        true_download_site = []
        true_processing = []

        # Check Update or not
        self.install_package.setText(self.LANG.STR_UPDATE_TITLE + "2/2")
        QtWidgets.QApplication.processEvents()
        #print("正在获取更新文件 2/2")
        assistant_loc = os.path.join(TOOL_LOCATION, ".config", "assistant_latest.json")
        version, last_version, download_list, download_site, main_processing = read_todo_json(assistant_loc)
        
        # Write update queue
        if version != SETTING.VERSION:
            true_download_list = download_list
            true_download_site = download_site
            true_processing = main_processing
            if last_version == "HAND_UPDATE":
                true_processing.append(["-unzip",    "-tool", ".Download", "minecraft-new.zip", "-to", "-tool", ".inits", "minecraft-new"])

        # Add addones download to queue
        if not os.path.exists(os.path.join(TOOL_LOCATION, ".inits", "1.12.2-full.zip")):
            true_download_list.append("1.12.2-full.zip")
            true_download_site.append(SETTING.ADDONES_SITE + "/1.12.2-full.zip")
            true_processing.append(["-mv",       "-tool", ".Download", "1.12.2-full.zip",   "-to", "-tool", ".inits", "1.12.2-full.zip"])
       

        
        if FOR_TEST:
            print(true_download_list)
            print(true_download_site)
            print(true_processing)
        
        # main download
        for i in range(len(true_download_site)):
            self.operation_info.setText(self.LANG.STR_DOWNLOAD_1 + str(i+1) + self.LANG.STR_DOWNLOAD_2 + str(len(true_download_site))+ self.LANG.STR_DOWNLOAD_3)
            QtWidgets.QApplication.processEvents()
            #print("正在下载：第" + str(i+1) + "项，共" + str(len(download_list))+ "项")
            current_download_location = os.path.join(TOOL_LOCATION, ".Download", true_download_list[i])
            download_file(true_download_site[i], current_download_location, self.LANG)

        # main opeartion
        for i in range(len(true_processing)):    
            self.operation_info.setText(self.LANG.STR_INSTALL_1 + str(i+1) + self.LANG.STR_INSTALL_2 + str(len(true_processing))+ self.LANG.STR_INSTALL_3)
            QtWidgets.QApplication.processEvents()
            #print("正在安装文件：第" + str(i+1) + "项，共" + str(len(operation_list))+ "项")
            operation_main_function(true_processing[i], TOOL_LOCATION)
        
        self.operation_info.setText("")
        QtWidgets.QApplication.processEvents()
        
        # Post operations 
        if version != SETTING.VERSION:
            if last_version == "HAND_UPDATE":
                os.system(self.open_cmd_head + " " + os.path.join(TOOL_LOCATION, ".inits", "minecraft-new"))
                SETTING.HAND_UPDATE_VERSION = version
                SETTING.refresh_setting()
                self.close()
                error_warning(self.LANG.STR_HAND_UPDATE)

            SETTING.VERSION = version
            SETTING.refresh_setting()
            error_warning(self.LANG.UPDATE_NORMAl)
        
        self.close()
        #QCoreApplication.instance().quit
        #QCoreApplication.quit()



    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



def main():
    global FOR_TEST
    global SETTING
    global TOOL_LOCATION



    """
    System Basic Initialization
    """ 
    """
    System Basic Initialization - Pre-Processing
    """ 
    # Parameter confirm
    not_direct_route = False        # Parameter for game file and assistant not include in same direction
    copy_route_root = ""            # Record of assistant direction
    first_time_initial = False      # Sign for first time file copy and download 
    open_cmd_head = ""

    if SystemJudge() == "Dos":
        TOOL_LOCATION = os.getcwd()

        not_direct_route = False
        copy_route_root = ""
        open_cmd_head = ""

    elif SystemJudge() == "Darwin":
        TOOL_LOCATION = os.path.join(str(Path.home()), "Library", "minecraft-mac")

        not_direct_route = True
        copy_route_root = "/Applications/minecraft-mac.app/Contents/MacOS/"
        open_cmd_head = "open"

    else:
        TOOL_LOCATION = os.getcwd()

        not_direct_route = False
        copy_route_root = ""
        open_cmd_head = ""

    if not os.path.exists(os.path.join(TOOL_LOCATION, ".inits")):
        first_time_initial = True

    if os.path.exists("main.py"):
        copy_route_root = ""



    # Surrounding build and file copy
    if not_direct_route:
        if first_time_initial:
            shutil.copytree(os.path.join(copy_route_root, ".inits"), 
                            os.path.join(TOOL_LOCATION, ".inits"))            
        else:
            shutil.copyfile(os.path.join(copy_route_root, ".inits", "version_setting.json"), 
                            os.path.join(TOOL_LOCATION, ".inits", "version_setting.json"))



    """
    System Basic Initialization - Main-Processing
    """ 
    SETTING.initialization_setting()    # Initialization Setting parameters
    if SETTING.DEFAULT_LOC == "":
        SETTING.DEFAULT_LOC = os.path.join(TOOL_LOCATION, "minecraft-1.12.2")
        SETTING.refresh_setting()
    if SETTING.DEFAULT_LANG == "":
        SETTING.DEFAULT_LANG = "0"
        SETTING.refresh_setting()
    
    LANG = LANG_CLASS()                 # Initialization Language parameters
    LANG.init_language_setting()

    clear_all()                         # Clear last time download files
    


    """
    Surrounding Initialization
    """
    if not os.system("java -version") == 0:
        if SystemJudge() == "Dos":
            webbrowser.open("https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241536_1f5b5a70bf22433b84d0e960903adac8")
        elif SystemJudge() == "Darwin":
            webbrowser.open("https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241527_1f5b5a70bf22433b84d0e960903adac8")
        else:
            webbrowser.open("https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241526_1f5b5a70bf22433b84d0e960903adac8")
        error_warning(LANG.JAVA_NOT_INSTALL)



    """
    Update Assistant GUI and operations
    """
    app1 = QtWidgets.QApplication(sys.argv)
    ex1 = initialization_window(LANG, open_cmd_head)
    #app1.quit()
    #sys.exit(app1.exec_())
    clear_all()                         # Clear download for main processing

    # Download main package lists
    package_list_loc = os.path.join(TOOL_LOCATION, ".config", "package_list.json")                      # Confirm location
    download_file(SETTING.MAIN_SOURCE_JSON_FILE_WEB, package_list_loc, LANG)                            # Download and save
    package_name, package_site, package_info, latest_site= read_package_list_json(package_list_loc)     # Analysis files for post-treatment

    # Download packages mods config files
    package_loc = []
    for i in range(len(package_name)):
        #Confirm the location and download files for every project/package
        package_loc.append(os.path.join(TOOL_LOCATION, ".config", package_name[i]+".json"))
        download_file(package_site[i], package_loc[i], LANG)
    
    latest_loc = []
    for i in range(len(latest_site)):
        #For Update
        latest_loc.append(os.path.join(TOOL_LOCATION, ".config", package_name[i]+"-latest.json"))
        download_file(latest_site[i] + "latest.json", latest_loc[i], LANG)

    

    """
    Main GUI window and operations
    """
    #app2 = QtWidgets.QApplication(sys.argv)
    ex2 = MainWindow(package_name, package_info, package_loc, latest_loc, latest_site, LANG)
    #app2.quit()
    #app2.exec_()
    sys.exit(app1.exec_())



if __name__ == '__main__':
    if FOR_TEST:
        print()
        print("WARNING: THIS IS TESTING VERSION, PLEASE CHECK THE FOR_TEST VARIABLE IF YOU WANT TO PUBLICK THE PACKAGE")
        print("WARNING: THIS IS TESTING VERSION, PLEASE CHECK THE FOR_TEST VARIABLE IF YOU WANT TO PUBLICK THE PACKAGE")
        print("WARNING: THIS IS TESTING VERSION, PLEASE CHECK THE FOR_TEST VARIABLE IF YOU WANT TO PUBLICK THE PACKAGE")
        print()
    main()









