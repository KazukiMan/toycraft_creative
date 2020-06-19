# -*- coding: utf-8 -*-

#===========================================
#
#       Update Assistant Project - a auto update and installer solution for minecraft server update 
#       By Kazuki Amakawa (github.com/KazukiMan)
#
#       main.py
#       main function of all the programming       
#
#===========================================

import requests 
import os
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import json
import time
import shutil
import zipfile
import time 

from libpy import LANG




def download_file(url, filename):
    try:
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
    except:
        error_warning(LANG.STR_NOT_CONNECT)
    return 



def clear_all():
    try:
        shutil.rmtree(".config")
    except:
        pass
    try:
        shutil.rmtree(".Download")
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



def write_log(log_string, mode_string = "WARNING"):
    filename = "debug.log"
    file = open(filename, "a+", encoding="utf-8")
    write_log_string = "["
    write_log_string += time.ctime()
    write_log_string += "]"
    write_log_string += "  "
    write_log_string += mode_string
    write_log_string += ":"
    write_log_string += log_string
    file.write(write_log_string)
    file.close()
    return











"""
PRE-TRETMENT FUNCTION
"""
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



def check_default_route_exists():
    if not os.path.exists(os.path.join(os.getcwd(), ".inits", "default_loc")):
        return ""
    else:
        filename = os.path.join(os.getcwd(), ".inits", "default_loc")
        file = open(filename, "r", encoding="utf-8")
        line = file.readline()
        file.close()
        return line



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
            tmp_string = os.path.join(tmp_string, os.getcwd())
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









class MainWindow(QtWidgets.QWidget):
    def __init__(self, package_name, package_info, package_loc, latest_loc, latest_site, default_route):
        super().__init__()
        self.package_name = package_name
        self.package_info = package_info
        self.package_loc = package_loc
        self.latest_loc = latest_loc
        self.latest_site = latest_site
        self.default_route = default_route
        self.initUI()



        
    def initUI(self):        
        self.resize(400, 600)
            #Setting default size
        self.center()
            #Setting default location
        self.setWindowTitle(LANG.STR_TITLE)
            #Setting window title
        self.topFiller = QtWidgets.QWidget()
        self.topFiller.setMinimumSize(250, 2000)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.topFiller)
            #Add Scroll Area
        self.vbox_final = QtWidgets.QVBoxLayout()


        # Define title ad image label
        self.img = QtGui.QPixmap(os.path.join(os.getcwd(), ".inits", "img", "ad_img.jpg"))
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
        self.label_location_pre.setText(LANG.STR_FOLDER_MSG)
            #Set label msg

        self.label_location = QtWidgets.QLabel(self)
            #Build empty label
        self.label_location.setText(self.default_route)
            #Setting default msg

        self.direction_button = QtWidgets.QPushButton(LANG.STR_OPEN_FOLDER)
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
        self.label_combo_box_pre.setText(LANG.STR_SET_PACKAGE)
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
        self.install_package.setText(LANG.STR_PREPARED)
            #Setting default msg
        self.operation_info = QtWidgets.QLabel(self)
        self.vbox_final.addWidget(self.install_package)
        self.vbox_final.addWidget(self.operation_info)



        # Define buttons
        self.update_button = QtWidgets.QPushButton(LANG.STR_UPDATE_BUTTON)
            #Define button for update
        self.update_button.clicked.connect(self.update_start)
            #Connect to game function
        self.connect_button = QtWidgets.QPushButton(LANG.STR_CONNECT_US)
            #Define button to connect us
        self.sponsor_button = QtWidgets.QPushButton(LANG.STR_SPONSOR_US)
            #Define button sponsor us
        self.tp_screen_shot = QtWidgets.QPushButton(LANG.STR_TP_SCREEN)
            #Define button tp to screenshot folder
        self.tp_self_mod_button = QtWidgets.QPushButton(LANG.STR_TP_SELF_MOD)
            #Define button to self add mod folder
        self.ok_button = QtWidgets.QPushButton(LANG.STR_START_INSTALL)
            #Define button for final install
        self.ok_button.clicked.connect(self.installer)
            #Connect to installer function
        

        self.hbox_tmp1 = QtWidgets.QHBoxLayout()
            #Define box1 for first 2 button
        self.hbox_tmp1.addWidget(self.connect_button)
            #Add button staff/screenshot/startgame to tmp1 box
        self.hbox_tmp1.addWidget(self.tp_screen_shot)
            #Add button staff/screenshot/startgame to tmp1 box
        self.hbox_tmp1.addWidget(self.update_button)
            #Add button staff/screenshot/startgame to tmp1 box
        self.hbox_tmp2 = QtWidgets.QHBoxLayout()
            #Define box2 for last 2 button
        self.hbox_tmp2.addWidget(self.sponsor_button)
            #Add button sponsor/selfmod/installgame to tmp2 box
        self.hbox_tmp2.addWidget(self.tp_self_mod_button)
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
        self.install_dir = QtWidgets.QFileDialog.getExistingDirectory(self, LANG.STR_CHOOSE_FOLDER, os.getcwd())
        self.label_location.setText(self.install_dir)
        self.default_route = self.install_dir
        INSTALL_LOCATION = self.install_dir
        filename = os.path.join(os.getcwd(), ".inits", "default_loc")
        file = open(filename, "w", encoding="utf-8")
        file.write(self.install_dir)



    def change_package_intro(self):
        self.label_combo_box_intro.setText(self.package_info[self.combo_box.currentIndex()])



    def check_game_exists(self):
        filename = os.path.join(self.default_route, ".minecraft", ".installer.cfg")
        if not os.path.exists(filename):
            return ""
        file = open(filename, "r", encoding="utf-8")
        line = file.readline()
        file.close()
        for i in range(0, len(self.package_name)):
            if line == self.package_name[i]:
                return line
            else:
                return ""




    """
    Functions for install and upgrade - main todo operation
    """
    def todo_main(self, version, last_version, download_list, download_site, operation_list, client_route):
        #Download files
        for i in range(len(download_list)):
            self.operation_info.setText(LANG.STR_DOWNLOAD_1 + str(i+1) + LANG.STR_DOWNLOAD_2 + str(len(download_list))+ LANG.STR_DOWNLOAD_3)
            QtWidgets.QApplication.processEvents()
            #print("正在下载：第" + str(i+1) + "项，共" + str(len(download_list))+ "项")
            current_download_location = os.path.join(os.getcwd(), ".Download", download_list[i])
            download_file(download_site[i], current_download_location)

        #Command processing
        for i in range(len(operation_list)):    
            self.operation_info.setText(LANG.STR_INSTALL_1 + str(i+1) + LANG.STR_INSTALL_2 + str(len(operation_list))+ LANG.STR_INSTALL_3)
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
            reply = QtWidgets.QMessageBox.question(self, '', LANG.STR_DELETE_GAME_CHECK, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)    
            if reply == QtWidgets.QMessageBox.No:
                return
        else:
            reply = QtWidgets.QMessageBox.question(self, '', LANG.STR_DELETE_FOLDER, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                return

        try:
            shutil.rmtree(self.default_route)
        except:
            pass

        try:
            os.mkdir(self.default_route)
        except:
            pass
        
        self.install_package.setText(LANG.STR_INSTALL_TITLE + package_installed_name + LANG.STR_INSTALL_TITLE_2)
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
        res = self.todo_main(version, last_version, download_list, download_site, operation_list, self.default_route)
        filename = ".installer.cfg"
        filename = os.path.join(self.default_route, ".minecraft", ".installer.cfg")
        file = open(filename, "w", encoding="utf-8")
        file.write(self.package_name[self.combo_box.currentIndex()])
        file.close()
        
        self.install_package.setText(LANG.STR_INSTALL_END)
        QtWidgets.QApplication.processEvents()

        return 



    """
    Update Part
    """
    def update_start(self):
        package_installed_name = self.check_game_exists()
        if len(package_installed_name) == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText(LANG.STR_GAME_NOT_EXISTS)
            msgBox.exec_()
            return

        kase = 0
        for i in range(0, len(self.package_name)):
            if self.package_name[i] == package_installed_name:
                kase = i
                break
        json_installed_version, _, _ = get_version_and_json(os.path.join(self.default_route, ".minecraft", package_installed_name+"-latest.json"))
        json_version_stack = []
        json_current_version, json_last_version, _ = get_version_and_json(os.path.join(os.getcwd(), ".config", package_installed_name+"-latest.json"))
    
        while 1:
            if json_current_version == json_installed_version:
                break
            if len(json_version_stack) == 0:
                json_version_stack.append("-latest")
            else:
                json_version_stack.append(json_current_version)

            self.install_package.setText(LANG.STR_UPDATE_TITLE)
            QtWidgets.QApplication.processEvents()
            #print("正在下载更新数据库：" +  package_installed_name+json_last_version+".json")

            download_file(self.latest_site[kase] + json_last_version+".json", os.path.join(os.getcwd(), ".config", package_installed_name+json_last_version+".json"))
            json_current_version, json_last_version, _ = get_version_and_json(os.path.join(os.getcwd(), ".config", package_installed_name+json_last_version+".json"))


        if len(json_version_stack) != 0:
            for i in range(len(json_version_stack)-1, -1, -1):
                jsonfile_location = os.path.join(os.getcwd(), ".config", package_installed_name+json_version_stack[i]+".json")
                
                self.install_package.setText(LANG.STR_UPDATE + json_version_stack[i])
                QtWidgets.QApplication.processEvents()
                #print("正在更新版本至 "+ json_version_stack[i]+" 版本")

                version, last_version, download_list, download_site, main_processing = read_todo_json(jsonfile_location)
                pro_processing = []
                post_processing = [
                ["-rm",       "-client", ".minecraft", package_installed_name+"-latest.json"],
                ["-cp",       "-tool", ".config", package_installed_name+json_version_stack[i]+".json", "-to", "-client", ".minecraft", package_installed_name+"-latest.json"]
                ]
                operation_list = pro_processing + main_processing + post_processing

                res = self.todo_main(version, last_version, download_list, download_site, operation_list, self.default_route)

        self.install_package.setText(LANG.STR_UPDATE_END)
        QtWidgets.QApplication.processEvents()
        game_start_path = os.path.join(self.default_route, "HMCL.jar")
        os.system("cd " + self.default_route + " && java -jar " + game_start_path)
        #print("正在启动游戏")











def main():
    # Build folder for config files and download files
    clear_all()
    try:
        os.mkdir(".config")
    except:
        pass
    try:
        os.mkdir(".Download")
    except:
        pass
    
    if not os.path.exists(os.path.join(os.getcwd(), ".inits", "1.12.2-full.zip")):
        error_warning(LANG.STR_GAMEFILE_NOT_EXISTS)
            
    # Download config json files
    # Download main package lists
    package_list_loc = os.path.join(os.getcwd(), ".config", "package_list.json")            # Confirm location
    download_file(LANG.MAIN_SOURCE_JSON_FILE_WEB, package_list_loc)   # Download and save
    package_name, package_site, package_info, latest_site= read_package_list_json(package_list_loc)     # Analysis files for post-treatment

    # Download packages mods config files
    package_loc = []
    for i in range(len(package_name)):
        #Confirm the location and download files for every project/package
        package_loc.append(os.path.join(os.getcwd(), ".config", package_name[i]+".json"))
        download_file(package_site[i], package_loc[i])
    
    latest_loc = []
    for i in range(len(latest_site)):
        #For Update
        latest_loc.append(os.path.join(os.getcwd(), ".config", package_name[i]+"-latest.json"))
        download_file(latest_site[i] + "latest.json", latest_loc[i])



    default_route = check_default_route_exists()
    if len(default_route) == 0:
        default_route = os.path.join(os.getcwd(), "minecraft-1.12.2")

    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow(package_name, package_info, package_loc, latest_loc, latest_site, default_route)
    sys.exit(app.exec_()) 




if __name__ == '__main__':
    main()