# -*- coding: utf-8 -*-

# petgfunctions.py - This python "helper" script holds a lot of functions

# Copyright (c) 2012-2013 Harry van der Wolf. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public Licence as published
# by the Free Software Foundation, either version 2 of the Licence, or
# version 3 of the Licence, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public Licence for more details.

# This file is part of pyexiftoolgui.
# pyexiftoolgui is a pySide script program that reads and writes  
# gps tags from/to files. It can use a "reference" image to write the
# gps tags to a multiple set of files that are taken at the same
# location.
# pyexiftoolgui is a graphical frontend for the open source
# command line tool exiftool by Phil Harvey, but it's not
# a complete exiftool gui: not at all.

import os, sys, platform, shlex, subprocess, time, re, string, datetime

import PySide
from PySide.QtCore import *
from PySide.QtGui import *

import programinfo
import programstrings

from ui_create_args import Ui_Dialog_create_args
from ui_export_metadata import Ui_Dialog_export_metadata
from ui_remove_metadata import Ui_Dialog_remove_metadata
from ui_modifydatetime import Ui_DateTimeDialog
from ui_syncdatetime import Ui_SyncDateTimeTagsDialog
#from ui_rename_photos import Ui_Dialog_rename_files

#------------------------------------------------------------------------
# All kind of functions

###################################################################################################################
# Start of Startup checks and configuration
###################################################################################################################
def remove_workspace( self ):
    # Remove our temporary workspace
#    try:
#        fls = os.remove(self.tmpworkdir + "/*")
#    except:
#        print("No files in " + self.tmpworkdir + " or no folder at all")
#    try: 
#        fldr = os.rmdir(self.tmpworkdir)
#    except:
#        print("Couldn't remove folder")
    print(self.tmpworkdir)
    if self.OSplatform == "Windows":
        self.tmpworkdir = self.tmpworkdir.replace("/", "\\")
        command_line = "rmdir /S /Q " + self.tmpworkdir
    else:
        command_line = "rm -rf " + self.tmpworkdir
        p = os.system(command_line)
        #args = shlex.split(command_line)
        #print args
        #p = subprocess.call(args, shell=True)

    if p == 0:
        print(("Removed " + self.tmpworkdir + " and it contents."))
    else:
        print(("Error removing " + self.tmpworkdir + " and it contents."))

def is_executable(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def check_for_program(program):
    exists = False
    for path in os.environ["PATH"].split(os.pathsep):
        path_plus_program = os.path.join(path, program)
        if is_executable(path_plus_program):
            #print "program " + program + " found"
            exists = True
    return exists
# End of function check_for_program and is_executable (mini sub for check_for_program)

def exiftool_version_level_text(self):
        if float(self.exiftoolversion) < 9.07:
           self.statusbar.showMessage("I will disable the GPano options as exiftool >=9.07 is required. You have " + str(self.exiftoolversion))
           exiftoolleveltext = "Your exiftool version is " + str(self.exiftoolversion) + " . You need >=9.07 to write to images.\n"
           exiftoolleveltext += "Exiftool and therefore pyExifToolGUI can read the tags. See the View Data tab."
           self.lbl_exiftool_leveltext.setText(exiftoolleveltext)
        elif float(self.exiftoolversion) < 9.09:
        #else:
           exiftoolleveltext = "Your exiftool version is " + str(self.exiftoolversion) + " . Tags marked with * are obligatory. " 
           exiftoolleveltext += "\"Pose Heading Degrees\" is necessary to make it also function in Google Maps.\n Tags marked with *** are only writable with exiftool >= 9.09"
           self.lbl_exiftool_leveltext.setText(exiftoolleveltext)
           self.statusbar.showMessage("Your exiftoolversion is " + str(self.exiftoolversion))
        else:
           exiftoolleveltext = "Your exiftool version is " + str(self.exiftoolversion) + " . Tags marked with * are obligatory. " 
           exiftoolleveltext += "\"Pose Heading Degrees\" is necessary to make it also function in Google Maps. Tags marked with *** are only writable with exiftool >= 9.09"
           self.lbl_exiftool_leveltext.setText(exiftoolleveltext)
           self.statusbar.showMessage("Your exiftoolversion is " + str(self.exiftoolversion))
        #print "exiftoolversion : " + self.exiftoolversion


def tool_check( self ):
    # We need this startup check as long as we don't have a package
    # that deals with dependencies

   if self.alternate_exiftool == True:
       self.exiftoolprog = self.exiftooloption.text()
   else:
       self.exiftoolprog = "exiftool"
   # Check for exiftool, based on the setting or no setting above
   if (self.OSplatform in ("Windows", "win32")):
        if ("exiftool.exe" in self.exiftoolprog) or ("Exiftool.exe" in self.exiftoolprog):
            self.exiftool_dir = os.path.join(self.realfile_dir, "exiftool", "exiftool.exe")
            #self.exiftoolprog = self.exiftool_dir + "\exiftool.exe"
            if not os.path.isfile(self.exiftoolprog):
                       configure_message = "exiftool is missing or incorrectly configured in Preferences!\n"
                       configure_message += "This tool is an absolute must have!\nPlease set the correct location or install exiftool first.\n\n"
                       configure_message += "If your exiftool is named \"exiftool(-k).exe\", rename it to \"exiftool.exe\""
                       ret = QMessageBox.critical(self, "exiftool is missing or incorrectly configured", configure_message)
                       result = self.select_exiftool()
                       #print str(result)
                       if result == "":
                          ret = QMessageBox.critical(self, "Canceled exiftool selection", "You canceled the exiftool selection.\nThe program will quit!\nFirst install exiftool or restart this program and select the correct exiftool.")
                          sys.exit()
                       else:
                          self.exiftoolprog = result
            #print self.exiftoolprog
            args = '"' + self.exiftoolprog + '" -ver'
            print("windows args " + args)
            self.exiftoolversion = subprocess.check_output(args, shell=True)
            print("self.exiftoolversion " + str(self.exiftoolversion)) 
   else:
        if not check_for_program(self.exiftoolprog):
            ret = QMessageBox.critical(self, "exiftool is missing or incorrectly configured", "exiftool is missing or incorrectly configured in Preferences!\nThis tool is an absolute must have!\nPlease set the correct location or install exiftool first.")
            #sys.exit()
            result = self.select_exiftool()
            #print str(result)
            if result == "":
                ret = QMessageBox.critical(self, "Canceled exiftool selection", "You canceled the exiftool selection.\nThe program will quit!\nFirst install exiftool or restart this program and select the correct exiftool.")
                sys.exit()
            else:
                self.exiftoolprog = result
                #print "result 2" + self.exiftoolprog
        command_line = '"' + self.exiftoolprog + '" -ver'
        args = shlex.split(command_line)
        self.exiftoolversion = subprocess.check_output(args)
   # remove last character which is the final ending \n (where \ is only the escape character)
   self.exiftoolversion = self.exiftoolversion[:-1]
   exiftool_version_level_text(self)
# End of function tool_check

def write_config(self, aftererror):
    if sys.version_info>(3,0,0):
        print("We are on python 3")
        # for python3 we use it's own write_config3 function
        write_config3(self, aftererror)
        return
        #import configparser
        #config = configparser.ConfigParser()
    elif sys.version_info<(2,7,0):
        sys.stderr.write("\n\nYou need python 2.7 or later to use pyexiftoolgui\n")
        exit(1) 
    else: # 2.7.0 < version < 3.0.0
        import ConfigParser
        config = ConfigParser.RawConfigParser()

    # Here we write to our pyexiftoolgui config file
    #print "Writing our config file"

    # Create our config
    config.add_section("preferences")
    if aftererror == 1: # Some error occurred. Go back to defaults
        config.set("preferences", "alternate_exiftool", str(False))
        self.alternate_exiftool = False
        config.set("preferences", "exiftooloption", "exiftool")
        config.set("preferences", "pref_thumbnail_preview",str(True))
        config.set("preferences", "def_creator", "")
        config.set("preferences", "def_copyright", "")
    else:
        if self.exiftooloption.text() in ("exiftool", ""):
            config.set("preferences", "alternate_exiftool", str(False))
            config.set("preferences", "exiftooloption", "exiftool")
        else: # user has changed it
            config.set("preferences", "alternate_exiftool", str(True))
            config.set("preferences", "exiftooloption", self.exiftooloption.text())
            if self.pref_thumbnail_preview.isChecked():
               config.set("preferences", "pref_thumbnail_preview",str(True))
            else:
               config.set("preferences", "pref_thumbnail_preview",str(False))
        config.set("preferences", "def_creator", self.def_creator.text())
        config.set("preferences", "def_copyright", self.def_copyright.text())

    userpath = os.path.expanduser('~')
    try:
        fldr = os.mkdir(os.path.join(userpath, '.pyexiftoolgui'))
        #print "fldr gives: " + fldr
    except:
        print("Check for config folder: exists => OK")
    try:
        with open(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg'), 'wb') as configfile:
            config.write(configfile)
    except:
        print("couldn't write configfile")

def write_config3(self, aftererror):
    import configparser
    config = configparser.ConfigParser()

    # Here we write to our pyexiftoolgui config file
    #print "Writing our config file"

    # Create our config
    config["preferences"] = {}
    if aftererror == 1: # Some error occurred. Go back to defaults
        config["preferences"]["alternate_exiftool"] = str(False)
        self.alternate_exiftool = False
        config["preferences"]["exiftooloption"] = "exiftool"
        config["preferences"]["pref_thumbnail_preview"] = str(True)
        config["preferences"]["def_creator"] = ""
        config["preferences"]["def_copyright"] = ""
    else:
        if self.exiftooloption.text() in ("exiftool", ""):
            config["preferences"]["alternate_exiftool"] = str(False)
            config["preferences"]["exiftooloption"] = "exiftool"
        else: # user has changed it
            config["preferences"]["alternate_exiftool"] = str(True)
            config["preferences"]["exiftooloption"] = self.exiftooloption.text()
            if self.pref_thumbnail_preview.isChecked():
               config["preferences"]["pref_thumbnail_preview"] = str(True)
            else:
               config["preferences"]["pref_thumbnail_preview"] = str(False)
        config["preferences"]["def_creator"] = self.def_creator.text()
        config["preferences"]["def_copyright"] = self.def_copyright.text()

    userpath = os.path.expanduser('~')
    try:
        fldr = os.mkdir(os.path.join(userpath, '.pyexiftoolgui'))
        #print "fldr gives: " + fldr
    except:
        print("Check for config folder: exists => OK")
    try:
        with open(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg'), 'w') as configfile:
            config.write(configfile)
    except:
        print("couldn't write configfile")
# end of write_config3: The python3 config writer


def error_reading_configparameter(self):
    message = ("Somehow I encountered an error reading the config file.\n"
           "This can happen when:\n- an updated version added or removed a parameter\n"
           "- when the config file somehow got damaged.\n"
                   "- when this is the very first program start.\n\n"
           "I will simply create a new config file. Please "
           "check your preferences.")
    ret = QMessageBox.warning(self, "error reading config", message) 
    # simply run the write_config function to create our initial config file
    aftererror = True
    write_config(self, 1)

def read_config(self):
    if sys.version_info>(3,0,0):
        print("We are on python 3. We will use the python3 read_config3 configparser")
        #import configparser
        #config = configparser.ConfigParser()
        read_config3(self)
        return
    elif sys.version_info<(2,7,0):
        sys.stderr.write("\n\nYou need python 2.7 or later to use pyexiftoolgui\n")
        exit(1) 
    else: # 2.7.0 < version < 3.0.0
        import ConfigParser
        config = ConfigParser.RawConfigParser()

    #print "Reading our config file"
    userpath = os.path.expanduser('~')
    print(userpath)
    print(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg'))
    # First we check in the safe way for the existence of the config file
    if os.path.isfile(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg')):
        try:
            with open(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg')) as f: pass
            # If no error we can continue
            #print "no error on config check, continue"
            print("reading config.cfg")
            config.read(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg'))
            #print("config.cfg read")
            try: 
                self.alternate_exiftool = config.getboolean("preferences", "alternate_exiftool")
            except:
                error_reading_configparameter(self)  
            try:
                self.exiftooloption.setText(config.get("preferences", "exiftooloption"))
            except:
                error_reading_configparameter(self)
            try:
                if config.get("preferences", "pref_thumbnail_preview") == "True":
                    self.pref_thumbnail_preview.setChecked(1)
                else:
                    self.pref_thumbnail_preview.setChecked(0)
            except:
                error_reading_configparameter(self)
            try:
                self.def_creator.setText(config.get("preferences", "def_creator"))
            except:
                error_reading_configparameter(self)
            try:
                self.def_copyright.setText(config.get("preferences", "def_copyright"))
            except:
                error_reading_configparameter(self)
        
        except IOError as e: # error reading the config file itself
            print("Very first program start, updated pyexiftoolgui with added/removed setting or user deleted the config file")
    else:
        error_reading_configparameter(self)

def read_config3(self):
    # This is the config read function for python3
    import configparser
    config = configparser.ConfigParser()
    userpath = os.path.expanduser('~')
    print(userpath)
    print(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg'))
    # First we check in the safe way for the existence of the config file
    if os.path.isfile(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg')):
        try:
            with open(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg')) as f: pass
            # If no error we can continue
            #print "no error on config check, continue"
            config.read(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg'))
            try: 
                if config["preferences"]["alternate_exiftool"] == "True":
                    self.alternate_exiftool = True
                else:
                    self.alternate_exiftool = False
            except:
                error_reading_configparameter(self)  
            try:
                self.exiftooloption.setText(config["preferences"]["exiftooloption"])
            except:
                error_reading_configparameter(self)
            try:
                if config["preferences"]["pref_thumbnail_preview"] == "True":
                    self.pref_thumbnail_preview.setChecked(1)
                else:
                    self.pref_thumbnail_preview.setChecked(0)
            except:
                error_reading_configparameter(self)
            try:
                self.def_creator.setText(config["preferences"]["def_creator"])
            except:
                error_reading_configparameter(self)
            try:
                self.def_copyright.setText(config["preferences"]["def_copyright"])
            except:
                error_reading_configparameter(self)
        
        except IOError as e: # error reading the config file itself
            print("Very first program start, updated pyexiftoolgui with added/removed setting or user deleted the config file")
    else:
        error_reading_configparameter(self)

###################################################################################################################
# End of Startup checks and configuration
###################################################################################################################

#------------------------------------------------------------------------
# General help messagebox
def help_mbox(self,helptitle, helptext):
    self.helpmbox = QMessageBox()
    self.helpmbox.setWindowTitle(helptitle)
    self.helpmbox.setText(helptext)
    ret = self.helpmbox.exec_()
#------------------------------------------------------------------------
# image functions
def images_dialog(self, qApp):
    loadedimages = QFileDialog(self)
    qApp.processEvents()
    loadedimages.setFileMode(QFileDialog.ExistingFiles)
    if self.OSplatform == "Darwin":
            loadedimages.setDirectory(os.path.expanduser('~/Pictures'))
    elif self.OSplatform == "Linux":
            loadedimages.setDirectory(os.path.expanduser('~/Pictures'))
    elif self.OSplatform == "Windows":
            loadedimages.setDirectory(os.path.expanduser('~/My Pictures'))

    qApp.processEvents()
    self.statusbar.showMessage("Loading images")
    qApp.processEvents()
#    loadedimages.setNameFilter("image files (*.jpg *.tif *.tiff *.png)\nAll Files (*.*)")
    loadedimages.setNameFilter("image files (" + programstrings.SUPPORTEDIMAGES + ")\nsupported formats (" + programstrings.SUPPORTEDFORMATS + ")\nAll Files (*.*)")
    loadedimages.setViewMode(QFileDialog.Detail)
    filenamesstring = ""
    if loadedimages.exec_():
        fileNames = loadedimages.selectedFiles()
        qApp.processEvents()
        for fileName in fileNames:
           # Make sure that spaces in path/file names etcetera are
           # covered by putting them within spaces
           #print fileName
           filenamesstring += "\"" + fileName + "\" "
        #ret= QMessageBox.about(self, "file names", """ %s""" % fnstring)
        #return fileNames
        self.fileNames = fileNames
        self.filenamesstring = filenamesstring
    else:
        # user canceled
        self.statusbar.showMessage("you canceled loading the images.")
        fileNames = ""
    return (fileNames, filenamesstring)


def loadimages(self,loadedimages, loadedimagesstring,qApp):
    if loadedimagesstring == "":
        # user canceled loading images
        print("user canceled loading images")
    else:
        imagestring = ""
        rowcounter = 0
        total_images = len(loadedimages)
        self.progressbar.setRange(0, total_images)
        self.progressbar.setValue(0)
        self.progressbar.show()
        qApp.processEvents()
        self.MaintableWidget.clearContents()
        self.MaintableWidget.setRowCount(0)
        #self.MaintableWidget.setRowCount(len(loadedimages))
        self.resolutions = []
        cur_width_height = ""
        for loadedimage in loadedimages:
            if self.DebugMsg:
                print(rowcounter)
                print(loadedimage + "\n")
                print(loadedimagesstring)

            #print "loaded image: " + loadedimage
            folder,imagefile = os.path.split(loadedimage)
            self.image_folder = folder
            qtablefilename = QTableWidgetItem(imagefile)
            self.MaintableWidget.insertRow(rowcounter)
            # in case thumbs are disabled
            dis_thumb_string = QTableWidgetItem("disabled")
            if self.pref_thumbnail_preview.isChecked():
                # Now create the thumbnail to be displayed
                thumbnail = QLabel(self)
                image = QImage(loadedimage)
                thumbnail.setPixmap(QPixmap.fromImage(image))
                thumbnail.setScaledContents(True)
                # Fill the table
                self.MaintableWidget.setRowHeight(rowcounter,75)
                self.MaintableWidget.setColumnWidth(0,75)
                self.MaintableWidget.setColumnWidth(1,225)
                self.MaintableWidget.setCellWidget(rowcounter, 0, thumbnail)
            else:
                # Fill the table
                self.MaintableWidget.setColumnWidth(0,75)
                self.MaintableWidget.setColumnWidth(1,225)
                self.MaintableWidget.setItem(rowcounter, 0, dis_thumb_string)
            self.MaintableWidget.setItem(rowcounter, 1, qtablefilename)
            self.MaintableWidget.setToolTip('image(s) folder: ' + folder)
            rowcounter += 1
            self.progressbar.setValue(rowcounter) 
            self.statusbar.showMessage("Creating thumbnail of: " + os.path.basename(loadedimage))
            qApp.processEvents()
            imagestring += loadedimage + " "
        if self.allDebugMsg:
            ret= QMessageBox.about(self, "file names", "images found \n %s" % loadedimagesstring)
            ret= QMessageBox.about(self, "file names", "images found 2 \n %s" % imagestring)
        #self.imagesfolderlineitem.setText(folder)
        # After loading the photos we will enable buttons and events
        self.activate_buttons_events()



def imageinfo(self, qApp):
    self.statusbar.showMessage("")
    selected_row = self.MaintableWidget.currentRow()
    selected_image = "\"" + self.fileNames[selected_row] + "\""
    if self.radioButton_all.isChecked():
        exiftool_params = ""
        arguments = " -a "
        header = "all tags"
    if self.radioButton_exif.isChecked():
        exiftool_params = "-exif:all"
        header = "EXIF tags"
    if self.radioButton_xmp.isChecked():
        exiftool_params = "-xmp:all"
        header = "XMP tags"
    if self.radioButton_iptc.isChecked():
        exiftool_params = "-iptc:all"
        header = "IPTC tags"
    if self.radioButton_iccprofile.isChecked():
        exiftool_params = "-icc_profile:all"
        header = "ICC profile tags"
    if self.radioButton_gps.isChecked():
        exiftool_params = "-gps:all -xmp:GPSLatitude -xmp:GPSLongitude -xmp:Location -xmp:Country -xmp:State -xmp:City"
        arguments = " -a -gps:all -xmp:GPSLatitude -xmp:GPSLongitude -xmp:Location -xmp:Country -xmp:State -xmp:City"
        header = "GPS tags"
    if self.radioButton_gpano.isChecked():
        exiftool_params = " -xmp:CroppedAreaImageHeightPixels -xmp:CroppedAreaImageWidthPixels -xmp:CroppedAreaLeftPixels -xmp:CroppedAreaTopPixels -xmp:FullPanoHeightPixels -xmp:FullPanoWidthPixels -xmp:ProjectionType -xmp:UsePanoramaViewer -xmp:PoseHeadingDegrees -xmp:InitialViewHeadingDegrees -xmp:InitialViewPitchDegrees -xmp:InitialViewRollDegrees -xmp:StitchingSoftware -xmp:InitialHorizontalFOVDegrees"
        arguments = " -xmp:CroppedAreaImageHeightPixels -xmp:CroppedAreaImageWidthPixels -xmp:CroppedAreaLeftPixels -xmp:CroppedAreaTopPixels -xmp:FullPanoHeightPixels -xmp:FullPanoWidthPixels -xmp:ProjectionType -xmp:UsePanoramaViewer -xmp:PoseHeadingDegrees -xmp:InitialViewHeadingDegrees -xmp:InitialViewPitchDegrees -xmp:InitialViewRollDegrees -xmp:StitchingSoftware -xmp:InitialHorizontalFOVDegrees"
        header = "GPano tags"
    if self.radioButton_makernotes.isChecked():
        exiftool_params = "-makernotes:all"
        header = "makernotes tags"
    if self.OSplatform == "Windows":
            selected_image = selected_image.replace("/", "\\")
            args = "\"" + self.exiftoolprog + "\" -a " + exiftool_params + " " + selected_image
            p = subprocess.check_output(args, universal_newlines=True, shell=True)
    else:
            command_line = "\"" + self.exiftoolprog + "\" -a " + exiftool_params + " " + selected_image
            args = shlex.split(command_line)
            p = subprocess.check_output(args, universal_newlines=True)
    #arguments = arguments + " " + selected_image
    #print "ET = " + self.exiftoolprog + " arguments are " + arguments
    #myprocess = QProcess(self)
    #myprocess.start(self.exiftoolprog, arguments)
    #myprocess.waitForFinished(-1)
    #p = myprocess.readAll()
    #print "p after myprocess"
    #print p
    if len(p) == 0:
       p = header + "   :   No data available\n"
       #print p
    # remove last character which is the final ending \n (where \ is only the escape character)        
    p = p[:-1]
    p_lines = re.split('\n',p)
    self.exiftableWidget.clearContents()
    self.exiftableWidget.setRowCount(0)
    rowcounter = 0
    for line in p_lines:
       try: 
           descriptor, description = re.split(':', line,1)
           descriptor = descriptor.strip()
           description = description.strip()
           #print "descriptor " + descriptor + " ;description " + description
           self.exiftableWidget.insertRow(rowcounter)
           self.exiftableWidget.setColumnWidth(0,225)
           self.exiftableWidget.setColumnWidth(1,325)
           self.exiftableWidget.setItem(rowcounter, 0, QTableWidgetItem(descriptor))
           self.exiftableWidget.setItem(rowcounter, 1, QTableWidgetItem(description))
           rowcounter += 1
           qApp.processEvents()
       except:
           print("always the last line that doesn't work")

def copy_defaults(self, qApp, category):
    if category == "exif":
       self.exif_Artist.setText(self.def_creator.text())
       self.exif_Copyright.setText(self.def_copyright.text())
    elif category == "xmp":
       self.xmp_creator.setText(self.def_creator.text())
       self.xmp_rights.setText(self.def_copyright.text())
    elif category == "iptc":
       self.iptc_creator.setText(self.def_creator.text())
       self.iptc_rights.setText(self.def_copyright.text())

#------------------------------------------------------------------------
# Edit -> Gps tab and actions
def convertLatLong(self, direction):
    # only "int" at the latest moment or calculations go wrong
    if direction == 'dms2d':
       # first latitude
       # Note that "South" latitudes and "West" longitudes convert to negative decimal numbers
       if int(self.calc_lat_sec.text()) in range(0, 60):
          latd = float(self.calc_lat_sec.text()) / float(60)
       else:
          ret = QMessageBox.critical(self, "seconds error", "seconds must fall in the range 0 to <60")
       if int(self.calc_lat_min.text()) in range(0, 60):
         latd = (int(self.calc_lat_min.text()) + latd) / float(60)
       else:
         ret = QMessageBox.critical(self, "minutes error", "minutes must fall in the range 0 to <60")
       # check whether lat degrees falls within 0 and 89
       if int(self.calc_lat_deg.text()) in range(0, 90):
         latd = latd + int(self.calc_lat_deg.text())
       else:
         ret = QMessageBox.critical(self, "degrees error", "Latitude degrees must fall in the range 0 to 89")
       if self.radioButton_calc_gpsS.isChecked(): # South
         # this means a negative decimal latitude
         latd = -(latd)
       self.calc_latitude.setText(str(round(latd,6)))
       # now longitude
       if int(self.calc_lon_sec.text()) in range(0, 60):
         lond = float(self.calc_lon_sec.text()) / float(60)
       else:
         ret = QMessageBox.critical(self, "seconds error", "seconds must fall in the range 0 to <60")
       if int(self.calc_lon_min.text()) in range(0, 60):
         lond = (int(self.calc_lon_min.text()) + lond) / float(60)
       else:
         ret = QMessageBox.critical(self, "minutes error", "minutes must fall in the range 0 to <60")
       # check whether lon degrees falls within 0 and 179
       if int(self.calc_lon_deg.text()) in range(0, 179):
         lond = lond + int(self.calc_lon_deg.text())
       else:
         ret = QMessageBox.critical(self, "degrees error", "Longitude degrees must fall in the range 0 to 179")
       if self.radioButton_calc_gpsW.isChecked(): # West
         lond = -(lond)
       # Update value in decimal latituted field
       self.calc_longitude.setText(str(round(lond,6)))
    else: # direction is d2dms
       # First latitude
       latitude = self.calc_latitude.text()
       # First check on "," in string
       if "," in latitude:
          latitude = latitude.replace(',','.')
          self.calc_latitude.setText(latitude)
       # Now check whether we have a "." in our strong. If not we have an integer and re is not necessary
       if "." in latitude:
         latint, latremain = re.split('\.', latitude)
       else:
         latint = latitude
       if int(latint) in range (-89, 89):
         if (int(latint)) < 0:
                 latint = -(int(latint))
                 latitude = -(float(latitude))
                 self.radioButton_calc_gpsS.setChecked(1)
         else:
                 self.radioButton_calc_gpsN.setChecked(1)

         deg = str(latint)
         self.calc_lat_deg.setText(deg)
         min = (float(latitude) - int(deg)) * 60
         self.calc_lat_min.setText(str(int(min)))
         sec = int(round(((float(min) - int(min)) *60), 0))
         self.calc_lat_sec.setText(str(sec))
       else:
         ret = QMessageBox.critical(self, "degrees error", "Latitude decimal must fall in the range -90 < degr < 90")
       # Now longitude
       longitude = self.calc_longitude.text()
       # First check on "," in string
       if "," in longitude:
          longitude = longitude.replace(',','.')
          self.calc_longitude.setText(longitude)
       # Now check whether we have a "." in our strong. If not we have an integer and re is not necessary
       if "." in longitude:
          lonint, lonremain = re.split('\.',(self.calc_longitude.text()))
       else:
          lonint = longitude
       if int(lonint) in range (-179, 179):
         if (int(lonint)) < 0:
                 lonint = -(int(lonint))
                 longitude = -(float(longitude))
                 self.radioButton_calc_gpsW.setChecked(1)
         else:
                 self.radioButton_calc_gpsE.setChecked(1)
         #longitude = float(lonint) + (float(lonremain)/(10**multiplier))
         deg = str(lonint)
         self.calc_lon_deg.setText(deg)
         min = (float(longitude) - int(deg)) * 60
         self.calc_lon_min.setText(str(int(min)))
         sec = int(round(((float(min) - int(min)) *60), 0))
         self.calc_lon_sec.setText(str(sec))
       else:
         ret = QMessageBox.critical(self, "degrees error", "Longitude decimal must fall in the range -180 < degr < 180")

def clear_gps_fields(self):
    self.calc_lat_deg.setText("")
    self.calc_lat_min.setText("")
    self.calc_lat_sec.setText("")
    self.calc_latitude.setText("")
    self.radioButton_calc_gpsN.setChecked(1)
    self.calc_lon_deg.setText("")
    self.calc_lon_min.setText("")
    self.calc_lon_sec.setText("")
    self.calc_longitude.setText("")
    self.gps_lat_decimal.setText("")
    self.gps_lon_decimal.setText("")
    self.radioButton_calc_gpsE.setChecked(1)
    self.gps_altitude.setText("")
    self.chk_AboveSeaLevel.setChecked(1)
    self.gps_lat_deg.setText("")
    self.gps_lat_min.setText("")
    self.gps_lat_sec.setText("")
    self.gps_lon_deg.setText("")
    self.gps_lon_min.setText("")
    self.gps_lon_sec.setText("")
    self.radioButton_gpsN.setChecked(1)
    self.radioButton_gpsE.setChecked(1)
    self.xmp_location.setText("")
    self.xmp_country.setText("")
    self.xmp_state.setText("")
    self.xmp_city.setText("")
    self.chk_xmp_location.setChecked(1)
    self.chk_xmp_country.setChecked(1)
    self.chk_xmp_state.setChecked(1)
    self.chk_xmp_city.setChecked(1)
    self.gps_timestamp.setText("")
    self.gps_datestamp.setText("")
    self.gps_versionid.setText("")
    self.gps_mapdatum.setText("")
    self.chk_gps_timestamp.setChecked(1)
    self.chk_gps_datestamp.setChecked(1)

def copy_calc_to_gpsinput(self):
    self.gps_lat_decimal.setText(self.calc_latitude.text())
    self.gps_lon_decimal.setText(self.calc_longitude.text())
    self.gps_lat_deg.setText(self.calc_lat_deg.text())
    self.gps_lat_min.setText(self.calc_lat_min.text())
    self.gps_lat_sec.setText(self.calc_lat_sec.text())
    self.gps_lon_deg.setText(self.calc_lon_deg.text())
    self.gps_lon_min.setText(self.calc_lon_min.text())
    self.gps_lon_sec.setText(self.calc_lon_sec.text())
    if self.radioButton_calc_gpsN.isChecked():
        self.radioButton_gpsN.setChecked(1)
    else:
        self.radioButton_gpsS.setChecked(1)
    if self.radioButton_calc_gpsE.isChecked():
        self.radioButton_gpsE.setChecked(1)
    else:
        self.radioButton_gpsW.setChecked(1)


def d2dms(self, value, sort):
    # This is a simplified one-way copy of the convertLatLong function above for the input read-only fields
    # Both cold be integrated, more efficient, but this is faster to maintain (and I'm lazy)
    value = abs(float(value))
    deg = int(value)
    min = (float(value) - int(deg)) * 60
    sec = int(round(((float(min) - int(min)) *60), 0))
    # only "int" at the latest moment or calculations go wrong
    if sort == "lat":
       self.gps_lat_deg.setText(str(deg))
       self.gps_lat_min.setText(str(int(min)))
       self.gps_lat_sec.setText(str(sec))
    else:
       self.gps_lon_deg.setText(str(deg))
       self.gps_lon_min.setText(str(int(min)))
       self.gps_lon_sec.setText(str(sec))
       

def copygpsfromselected(self,qApp):
        # First clean input fields
        clear_gps_fields(self)
        exiftool_params = ' -e -n -a -gps:all -xmp:Location -xmp:Country -xmp:State -xmp:City -xmp:GPSLatitude -xmp:GPSLongitude '
        data = True
        p = read_image_info(self, exiftool_params)
        if len(p) == 0:
           data = False
           message = ("<p>You are trying to copy the gps/location info from your source image, but your source image "
                      "doesn't contain data or doesn't seem to contain data (or you didn't select an image).</p>"
                      "<p>In case your camera has a GPS system, but only uses it's internal \"maker\" options "
                      "to store the gps data, I can't retrieve the data as it is stored differently "
                      "for every brand of camera.</p>"
                      "<p>If this is the case for your camera, your only option is to copy & paste the information out "
                      "of the table rows from the \"General\" tab.")
           ret = QMessageBox.warning(self, "Error copying gps info from source image", message)
        else:
           # remove last character which is the final ending \n (where \ is only the escape character)        
           p = p[:-1]
           p_lines = re.split('\n',p)
           rowcounter = 0
           for line in p_lines:
            #try: 
               descriptor, description = re.split(':', line,1)
               descriptor = descriptor.strip()
               description = description.strip()
               gpslat = 0
               gpslon = 0
               latref = 0
               lonref = 0
               if descriptor == "GPS Version ID":
                     self.gps_versionid.setText(description)
               if descriptor == "GPS Latitude Ref":
                  latref = 1
                  latrefvalue = description
                  if description == "N":
                     self.radioButton_gpsN.setChecked(1)
                  else:
                     self.radioButton_gpsS.setChecked(1)
               if descriptor == "GPS Latitude":
                     gpslat += 1
                     if gpslat == 2:
                        print("we have a xmp latitude")
                     gpslatvalue = description
                     self.gps_lat_decimal.setText(str(round(float(description),6)))
               if descriptor == "GPS Longitude Ref":
                  lonref = 1
                  lonrefvalue = description
                  if description == "E":
                     self.radioButton_gpsE.setChecked(1)
                  else:
                     self.radioButton_gpsW.setChecked(1)
               if descriptor == "GPS Longitude":
                      gpslon += 1
                      if gpslon == 2:
                         print("we have an xmp longitude")
                      gpslonvalue = description
                      self.gps_lon_decimal.setText(str(round(float(description),6)))
               if descriptor == "GPS Altitude Ref":
                  if description == "0":
                     self.chk_AboveSeaLevel.setChecked(1)
                  else:
                     self.chk_AboveSeaLevel.setChecked(0)
               if descriptor == "GPS Altitude":
                      self.gps_altitude.setText(str(round(float(description),1)))
               if descriptor == "Location":
                     self.xmp_location.setText(description)
               if descriptor == "Country":
                     self.xmp_country.setText(description)
               if descriptor == "State":
                     self.xmp_state.setText(description)
               if descriptor == "City":
                     self.xmp_city.setText(description)
               if descriptor == "GPS Time Stamp":
                     self.gps_timestamp.setText(description)
               if descriptor == "GPS Date Stamp":
                     self.gps_datestamp.setText(description)
               if descriptor == "GPS Map Datum":
                     self.gps_mapdatum.setText(description)
               #print "rowcounter " + str(rowcounter) + " descriptor " + descriptor + " ;description " + description
               rowcounter += 1
               #qApp.processEvents()
            #except:
               #print "always the last line that doesn't work"

        # We bluntly walk through all tags as we don't know whether they are complete.
        # Now we need to check for neg/pos latitutes and longitudes by REF values as
        # We do not know now whether we have exif decimal values (always positive)
        # or xmp decimal values which can be negative or positive.
        # That's not so elegant but much simpler then building internal checks.
        if latref == 1:
           value = self.gps_lat_decimal.text()
           if latrefvalue == "N":
               self.gps_lat_decimal.setText(str(abs(float(value))))
           else: # E = negative
               if value.count('-') == 0: # doesn't contain a - but should contain it.
                  self.gps_lat_decimal.setText('-' + value)
        if lonref == 1:
           value = self.gps_lon_decimal.text()
           if latrefvalue == "E":
               self.gps_lon_decimal.setText(str(abs(float(value))))
           else: # W = negative
               if value.count('-') == 0: # doesn't contain a - but should contain it.
                  self.gps_lon_decimal.setText('-' + value)
        # Check whether we have xmp lat/lon
        if data:
           d2dms(self, gpslatvalue, "lat")
           d2dms(self, gpslonvalue, "lon")

def savegpsdata(self, qApp):
        exiftool_params=""
        # Exif and xmp gps data
        if self.chk_lat_lon_alt.isChecked():
            exiftool_params =  ' -exif:GPSLatitude="' + self.gps_lat_decimal.text() + '" '
            value = float(self.gps_lat_decimal.text())
            if value > 0:
                exiftool_params +=  ' -exif:GPSLatitudeREF="N" '
            else:
                exiftool_params +=  ' -exif:GPSLatitudeREF="S" '
            exiftool_params +=  ' -xmp:GPSLatitude="' + self.gps_lat_decimal.text() + '" '
            exiftool_params +=  ' -exif:GPSLongitude="' + self.gps_lon_decimal.text() + '" '
            value = float(self.gps_lon_decimal.text())
            if value > 0:
                exiftool_params +=  ' -exif:GPSLongitudeREF="E" '
            else:
                exiftool_params +=  ' -exif:GPSLongitudeREF="W" '
            exiftool_params +=  ' -xmp:GPSLongitude="' + self.gps_lon_decimal.text() + '" '
            exiftool_params +=  ' -exif:GPSAltitude="' + self.gps_altitude.text() + '" '
            exiftool_params +=  ' -xmp:GPSAltitude="' + self.gps_altitude.text() + '" '
            if self.chk_AboveSeaLevel.isChecked():
                exiftool_params +=  ' -exif:GPSAltitudeRef= "0" '  # Above sea level
            else:
                exiftool_params +=  ' -exif:GPSAltitudeRef= "1" '  # Below sea level
        # Location data for XMP and IPTC
        if self.chk_xmp_location.isChecked():
               exiftool_params +=  '-xmp:Location="' + self.xmp_location.text() + '" '
               exiftool_params +=  '-iptc:Sub-location="' + self.xmp_location.text() + '" '
        if self.chk_xmp_country.isChecked():
               exiftool_params +=  '-xmp:Country="' + self.xmp_country.text() + '" '
               exiftool_params +=  '-iptc:Country-PrimaryLocationName="' + self.xmp_country.text() + '" '
        if self.chk_xmp_state.isChecked():
               exiftool_params +=  '-xmp:State="' + self.xmp_state.text() + '" '
               exiftool_params +=  '-iptc:Province-State="' + self.xmp_state.text() + '" '
        if self.chk_xmp_city.isChecked():
               exiftool_params +=  '-xmp:City="' + self.xmp_city.text() + '" '
               exiftool_params +=  '-iptc:City="' + self.xmp_city.text() + '" '
        # Map date/time and format stuff
        if self.chk_gps_timestamp.isChecked():
               exiftool_params +=  '-exif:Copyright="' + self.exif_Copyright.text() + '" '
        if self.chk_gps_datestamp.isChecked():
               exiftool_params +=  '-exif:UserComment="' + self.exif_UserComment.text() + '" '
        if self.gps_mapdatum.text() == "":
               exiftool_params +=  '-exif:GPSMapDatum="WGS-84" '
        else:
               exiftool_params +=  '-exif:GPSMapDatum="' + self.gps_mapdatum.text() + '" '
        print(exiftool_params)
        # Now write the data to the photo(s)
        if self.chk_gps_backuporiginals.isChecked():
           write_image_info(self, exiftool_params, qApp, True)
        else:
           write_image_info(self, exiftool_params, qApp, False)


#------------------------------------------------------------------------
# Edit -> Exif tab and actions
def clear_exif_fields(self):
        self.exif_Make.setText("")
        self.exif_Model.setText("")
        self.exif_ModifyDate.setText("")
        self.exif_DateTimeOriginal.setText("")
        self.exif_CreateDate.setText("")
        self.exif_Artist.setText("")
        self.exif_Copyright.setText("")
        self.exif_UserComment.setText("")
        self.exif_ImageDescription.clear()

        self.chk_exif_Make.setChecked(1)
        self.chk_exif_Model.setChecked(1)
        self.chk_exif_ModifyDate.setChecked(1)
        self.chk_exif_DateTimeOriginal.setChecked(1)
        self.chk_exif_CreateDate.setChecked(1)
        self.chk_exif_Artist.setChecked(1)
        self.chk_exif_Copyright.setChecked(1)
        self.chk_exif_UserComment.setChecked(1)
        self.chk_exif_ImageDescription.setChecked(1)

def copyexiffromselected(self,qApp):
        # First clean input fields
        clear_exif_fields(self)
        exiftool_params = ' -e -n -exif:Make -exif:Model -exif:ModifyDate -exif:DateTimeOriginal -exif:CreateDate -exif:Artist -exif:Copyright -exif:UserComment -exif:ImageDescription '
        p = read_image_info(self, exiftool_params)
        if len(p) == 0:
           data = False
           message = ("<p>You are trying to copy exif info from your source image, but your source image "
                      "doesn't contain the specified exif data or doesn't seem to contain any exif data (or you didn't select an image).</p>")
           ret = QMessageBox.warning(self, "Error copying exif info from source image", message)
        else:
           # remove last character which is the final ending \n (where \ is only the escape character)        
           p = p[:-1]
           p_lines = re.split('\n',p)
           rowcounter = 0
           for line in p_lines:
            #try: 
               descriptor, description = re.split(':', line,1)
               descriptor = descriptor.strip()
               description = description.strip()
               gpslat = 0
               gpslon = 0
               if descriptor == "Make":
                     self.exif_Make.setText(description)
               if descriptor == "Camera Model Name":
                     self.exif_Model.setText(description)
               if descriptor == "Modify Date":
                     self.exif_ModifyDate.setText(description)
               if descriptor == "Date/Time Original":
                      self.exif_DateTimeOriginal.setText(description)
               if descriptor == "Create Date":
                     self.exif_CreateDate.setText(description)
               if descriptor == "Artist":
                     self.exif_Artist.setText(description)
               if descriptor == "Copyright":
                     self.exif_Copyright.setText(description)
               if descriptor == "User Comment":
                     self.exif_UserComment.setText(description)
               if descriptor == "Image Description":
                     self.exif_ImageDescription.insertPlainText(description)
               #print "rowcounter " + str(rowcounter) + " descriptor " + descriptor + " ;description " + description
               rowcounter += 1

def saveexifdata(self, qApp):
        exiftool_params = ""
        if self.chk_exif_Make.isChecked():
               exiftool_params =  ' -exif:Make="' + self.exif_Make.text() + '" '
        if self.chk_exif_Model.isChecked():
               exiftool_params +=  '-exif:Model="' + self.exif_Model.text() + '" '
        if self.chk_exif_ModifyDate.isChecked():
               exiftool_params +=  '-exif:ModifyDate="' + self.exif_ModifyDate.text() + '" '
        if self.chk_exif_DateTimeOriginal.isChecked():
               exiftool_params +=  '-exif:DateTimeOriginal="' + self.exif_DateTimeOriginal.text() + '" '
        if self.chk_exif_CreateDate.isChecked():
               exiftool_params +=  '-exif:CreateDate="' + self.exif_CreateDate.text() + '" '
        if self.chk_exif_Artist.isChecked():
               exiftool_params +=  '-exif:Artist="' + self.exif_Artist.text() + '" '
        if self.chk_exif_Copyright.isChecked():
               exiftool_params +=  '-exif:Copyright="' + self.exif_Copyright.text() + '" '
        if self.chk_exif_UserComment.isChecked():
               exiftool_params +=  '-exif:UserComment="' + self.exif_UserComment.text() + '" '
        if self.chk_exif_ImageDescription.isChecked():
               ImgDescr = self.exif_ImageDescription.toPlainText()
               exiftool_params +=  '-exif:ImageDescription="' + ImgDescr + '" '

        if self.chk_exif_backuporiginals.isChecked():
           write_image_info(self, exiftool_params, qApp, True)
        else:
           write_image_info(self, exiftool_params, qApp, False)
               
#------------------------------------------------------------------------
# Edit -> xmp tab and actions
def clear_xmp_fields(self):
        self.xmp_creator.setText("")
        self.xmp_rights.setText("")
        self.xmp_label.setText("")
        self.xmp_subject.setText("")
        self.xmp_title.setText("")
        self.xmp_rating1.setChecked(1)
        self.xmp_description.clear()
        self.xmp_person.setText("")

        self.chk_xmp_creator.setChecked(1)
        self.chk_xmp_rights.setChecked(1)
        self.chk_xmp_label.setChecked(1)
        self.chk_xmp_subject.setChecked(1)
        self.chk_xmp_title.setChecked(1)
        self.chk_xmp_rating.setChecked(1)
        self.chk_xmp_description.setChecked(1)
        self.chk_xmp_person.setChecked(1)

def copyxmpfromselected(self,qApp):
        # First clean input fields
        clear_xmp_fields(self)
        xmptool_params = ' -e -n -xmp:Creator -xmp:Rights -xmp:Label -xmp:Subject -xmp:Title -xmp:Rating -xmp:Description -xmp:Person -xmp:PersonInImage '
        p = read_image_info(self, xmptool_params)
        if len(p) == 0:
           data = False
           message = ("<p>You are trying to copy xmp info from your source image, but your source image "
                      "doesn't contain the specified xmp data or doesn't seem to contain any xmp data (or you didn't select an image).</p>")
           ret = QMessageBox.warning(self, "Error copying xmp info from source image", message)
        else:
           # remove last character which is the final ending \n (where \ is only the escape character)        
           p = p[:-1]
           p_lines = re.split('\n',p)
           rowcounter = 0
           for line in p_lines:
            #try: 
               descriptor, description = re.split(':', line,1)
               descriptor = descriptor.strip()
               description = description.strip()
               gpslat = 0
               gpslon = 0
               if descriptor == "Creator":
                     self.xmp_creator.setText(description)
               if descriptor == "Rights":
                     self.xmp_rights.setText(description)
               if descriptor == "Label":
                     self.xmp_label.setText(description)
               if descriptor == "Subject":
                      self.xmp_subject.setText(description)
               if descriptor == "Title":
                     self.xmp_title.setText(description)
               if descriptor == "Rating":
                     if description == "1":
                        self.xmp_rating1.setChecked(1)
                     elif description == "2":
                        self.xmp_rating2.setChecked(2)
                     elif description == "3":
                        self.xmp_rating3.setChecked(3)
                     elif description == "4":
                        self.xmp_rating4.setChecked(4)
                     elif description == "5":
                        self.xmp_rating5.setChecked(5)
               if descriptor == "Description":
                     self.xmp_description.insertPlainText(description)
               if descriptor == "Person":
                     self.xmp_person.setText(description)
               if descriptor == "Person In Image":
                     self.xmp_person.setText(description)
               #print "rowcounter " + str(rowcounter) + " descriptor " + descriptor + " ;description " + description
               rowcounter += 1

def savexmpdata(self, qApp):
        xmptool_params = ""
        if self.chk_xmp_creator.isChecked():
               xmptool_params =  ' -xmp:Creator="' + self.xmp_creator.text() + '" '
        if self.chk_xmp_rights.isChecked():
               xmptool_params +=  '-xmp:Rights="' + self.xmp_rights.text() + '" '
        if self.chk_xmp_label.isChecked():
               xmptool_params +=  '-xmp:Label="' + self.xmp_label.text() + '" '
        if self.chk_xmp_subject.isChecked():
               xmptool_params +=  '-xmp:Subject="' + self.xmp_subject.text() + '" '
        if self.chk_xmp_title.isChecked():
               xmptool_params +=  '-xmp:Title="' + self.xmp_title.text() + '" '
        if self.chk_xmp_rating.isChecked():
               if self.xmp_rating1.isChecked():
                  rating = "1"
               elif self.xmp_rating2.isChecked():
                  rating = "2"
               elif self.xmp_rating3.isChecked():
                  rating = "3"
               elif self.xmp_rating4.isChecked():
                  rating = "4"
               else:
                  rating = "5"
               xmptool_params +=  '-xmp:Rating="' + rating + '" '
        if self.chk_xmp_description.isChecked():
               Descr = self.xmp_description.toPlainText()
               xmptool_params +=  '-xmp:Description="' + Descr + '" '
        if self.chk_xmp_person.isChecked():
               xmptool_params +=  '-xmp:Person="' + self.xmp_person.text() + '" '
               xmptool_params +=  '-xmp:PersonInImage="' + self.xmp_person.text() + '" '

        if self.chk_xmp_backuporiginals.isChecked():
           write_image_info(self, xmptool_params, qApp, True)
        else:
           write_image_info(self, xmptool_params, qApp, False)
               
#------------------------------------------------------------------------
# Edit -> GPano tab and actions
def clear_gpano_fields(self):
        self.xmp_StitchingSoftware.setText("")
        self.xmp_CroppedAreaImageHeightPixels.setText("")
        self.xmp_CroppedAreaImageWidthPixels.setText("")
        self.xmp_CroppedAreaLeftPixels.setText("")
        self.xmp_CroppedAreaTopPixels.setText("")
        self.xmp_FullPanoHeightPixels.setText("")
        self.xmp_FullPanoWidthPixels.setText("")
        self.xmp_ProjectionType.setCurrentIndex(0)
        self.xmp_UsePanoramaViewer.setChecked(1)
        self.xmp_PoseHeadingDegrees.setText("")
        self.xmp_InitialViewHeadingDegrees.setText("")
        self.xmp_InitialViewPitchDegrees.setText("")
        self.xmp_InitialViewRollDegrees.setText("")
        self.xmp_InitialHorizontalFOVDegrees.setText("")

        self.chk_xmp_StitchingSoftware.setChecked(1)
        self.chk_xmp_CroppedAreaImageHeightPixels.setChecked(1)
        self.chk_xmp_CroppedAreaImageWidthPixels.setChecked(1)
        self.chk_xmp_CroppedAreaLeftPixels.setChecked(1)
        self.chk_xmp_CroppedAreaTopPixels.setChecked(1)
        self.chk_xmp_FullPanoHeightPixels.setChecked(1)
        self.chk_xmp_FullPanoWidthPixels.setChecked(1)
        self.chk_xmp_ProjectionType.setChecked(1)
        self.chk_xmp_UsePanoramaViewer.setChecked(1)
        self.chk_xmp_PoseHeadingDegrees.setChecked(1)
        self.chk_xmp_InitialViewHeadingDegrees.setChecked(1)
        self.chk_xmp_InitialViewPitchDegrees.setChecked(1)
        self.chk_xmp_InitialViewRollDegrees.setChecked(1)
        self.chk_xmp_InitialHorizontalFOVDegrees.setChecked(1)

def copygpanofromselected(self,qApp):
        # First clean input fields
        clear_exif_fields(self)
        exiftool_params = ' -e -n -xmp:CroppedAreaImageHeightPixels -xmp:CroppedAreaImageWidthPixels -xmp:CroppedAreaLeftPixels -xmp:CroppedAreaTopPixels -xmp:FullPanoHeightPixels -xmp:FullPanoWidthPixels -xmp:ProjectionType -xmp:UsePanoramaViewer -xmp:PoseHeadingDegrees -xmp:InitialViewHeadingDegrees -xmp:InitialViewRollDegrees -xmp:InitialViewPitchDegrees -xmp:StitchingSoftware -xmp:InitialHorizontalFOVDegrees '
        p = read_image_info(self, exiftool_params)
        if len(p) == 0:
           data = False
           message = ("<p>You are trying to copy GPano (Google Photosphere) info from your source image, but your source image "
                      "doesn't contain the specified GPano data or doesn't seem to contain any GPano data (or you didn't select an image).</p>")
           ret = QMessageBox.warning(self, "Error copying GPano info from source image", message)
        else:
           # remove last character which is the final ending \n (where \ is only the escape character)        
           p = p[:-1]
           p_lines = re.split('\n',p)
           rowcounter = 0
           for line in p_lines:
            #try: 
               descriptor, description = re.split(':', line,1)
               descriptor = descriptor.strip()
               description = description.strip()
               gpslat = 0
               gpslon = 0
               if descriptor == "Cropped Area Image Height Pixels":
                     self.xmp_CroppedAreaImageHeightPixels.setText(description)
               if descriptor == "Cropped Area Image Width Pixels":
                     self.xmp_CroppedAreaImageWidthPixels.setText(description)
               if descriptor == "Cropped Area Left Pixels":
                     self.xmp_CroppedAreaLeftPixels.setText(description)
               if descriptor == "Cropped Area Top Pixels":
                      self.xmp_CroppedAreaTopPixels.setText(description)
               if descriptor == "Full Pano Height Pixels":
                     self.xmp_FullPanoHeightPixels.setText(description)
               if descriptor == "Full Pano Width Pixels":
                     self.xmp_FullPanoWidthPixels.setText(description)
               if descriptor == "Projection Type":
                     if description == "equirectangular":
                        self.xmp_ProjectionType.setCurrentIndex(0)
                     elif description == "equirectangular":
                        self.xmp_ProjectionType.setCurrentIndex(1)
                     elif description == "rectilinear":
                        self.xmp_ProjectionType.setCurrentIndex(2)
               if descriptor == "Use Panorama Viewer":
                     if description == "True":
                        self.xmp_UsePanoramaViewer.setChecked(1)
                     else:
                        self.xmp_UsePanoramaViewer.setChecked(0)
               if descriptor == "Pose Heading Degrees":
                     self.xmp_PoseHeadingDegrees.setText(description)
               if descriptor == "Initial View Heading Degrees":
                     self.xmp_InitialViewHeadingDegrees.setText(description)
               if descriptor == "Initial View Pitch Degrees":
                     self.xmp_InitialViewPitchDegrees.setText(description)
               if descriptor == "Initial View Roll Degrees":
                     self.xmp_InitialViewRollDegrees.setText(description)
               if descriptor == "Stitching Software":
                     self.xmp_StitchingSoftware.setText(description)
               if descriptor == "Initial Horizontal FOV Degrees":
                     self.xmp_InitialHorizontalFOVDegrees.setText(description)
               #print "rowcounter " + str(rowcounter) + " descriptor " + descriptor + " ;description " + description
               rowcounter += 1

def savegpanodata(self, qApp):
        exiftool_params = ""
        if self.chk_xmp_CroppedAreaImageHeightPixels.isChecked():
               exiftool_params =  ' -xmp:CroppedAreaImageHeightPixels="' + self.xmp_CroppedAreaImageHeightPixels.text() + '" '
        if self.chk_xmp_CroppedAreaImageWidthPixels.isChecked():
               exiftool_params +=  '-xmp:CroppedAreaImageWidthPixels="' + self.xmp_CroppedAreaImageWidthPixels.text() + '" '
        if self.chk_xmp_CroppedAreaLeftPixels.isChecked():
               exiftool_params +=  '-xmp:CroppedAreaLeftPixels="' + self.xmp_CroppedAreaLeftPixels.text() + '" '
        if self.chk_xmp_CroppedAreaTopPixels.isChecked():
               exiftool_params +=  '-xmp:CroppedAreaTopPixels="' + self.xmp_CroppedAreaTopPixels.text() + '" '
        if self.chk_xmp_FullPanoHeightPixels.isChecked():
               exiftool_params +=  '-xmp:FullPanoHeightPixels="' + self.xmp_FullPanoHeightPixels.text() + '" '
        if self.chk_xmp_FullPanoWidthPixels.isChecked():
               exiftool_params +=  '-xmp:FullPanoWidthPixels="' + self.xmp_FullPanoWidthPixels.text() + '" '
        if self.chk_xmp_ProjectionType.isChecked():
               #print "projectiontype " + str(self.xmp_ProjectionType.currentIndex())
               #print "projectiontype " + str(self.xmp_ProjectionType.currentText())
               if self.xmp_ProjectionType.currentIndex() == 0:
                  exiftool_params +=  '-xmp:ProjectionType="equirectangular" '
               elif self.xmp_ProjectionType.currentIndex() == 1:
                  exiftool_params +=  '-xmp:ProjectionType="cylindrical" '
               elif self.xmp_ProjectionType.currentIndex() == 2:
                  exiftool_params +=  '-xmp:ProjectionType="rectangular" '
        if self.chk_xmp_UsePanoramaViewer.isChecked(): 
               if self.xmp_UsePanoramaViewer.isChecked():
                  exiftool_params +=  '-xmp:UsePanoramaViewer=1 '
               else:
                  exiftool_params +=  '-xmp:UsePanoramaViewer=0 '
        if self.chk_xmp_PoseHeadingDegrees.isChecked():
               exiftool_params +=  '-xmp:PoseHeadingDegrees="' + self.xmp_PoseHeadingDegrees.text() + '" '
        if self.chk_xmp_InitialViewHeadingDegrees.isChecked():
               exiftool_params +=  '-xmp:InitialViewHeadingDegrees="' + self.xmp_InitialViewHeadingDegrees.text() + '" '
        if self.chk_xmp_InitialViewPitchDegrees.isChecked():
               exiftool_params +=  '-xmp:InitialViewPitchDegrees="' + self.xmp_InitialViewPitchDegrees.text() + '" '
        if self.chk_xmp_InitialViewRollDegrees.isChecked():
               exiftool_params +=  '-xmp:InitialViewRollDegrees="' + self.xmp_InitialViewRollDegrees.text() + '" '
        if self.chk_xmp_StitchingSoftware.isChecked():
               exiftool_params +=  '-xmp:StitchingSoftware="' + self.xmp_StitchingSoftware.text() + '" '
        if self.chk_xmp_InitialHorizontalFOVDegrees.isChecked():
               exiftool_params +=  '-xmp:InitialHorizontalFOVDegrees="' + self.xmp_InitialHorizontalFOVDegrees.text() + '" '

        if self.chk_gpano_backuporiginals.isChecked():
           write_image_info(self, exiftool_params, qApp, True)
        else:
           write_image_info(self, exiftool_params, qApp, False)


#------------------------------------------------------------------------
# Edit -> geotagging tab and actions
def geotag_source_folder(self, qApp):
        self.statusbar.showMessage("")
        select_folder = QFileDialog(self)
        select_folder.setFileMode(QFileDialog.Directory)
        qApp.processEvents()
        if platform.system() == "Darwin":
            select_folder.setDirectory(os.path.expanduser('~/Pictures'))
        elif platform.system() == "Linux":
            select_folder.setDirectory(os.path.expanduser('~/Pictures'))
        elif platform.system() == "Windows":
            select_folder.setDirectory(os.path.expanduser('~/My Pictures'))
        select_folder.setViewMode(QFileDialog.Detail)
        qApp.processEvents()
        geotag_source_folder = ""
        if select_folder.exec_():
           geotag_source_folder = select_folder.selectedFiles()[0]
           self.geotag_source_folder = geotag_source_folder 
           self.LineEdit_geotag_source_folder.setText(geotag_source_folder)
           #print(str(self.geotag_source_folder))
           # button to write can be enabled
           self.btn_write_geotaginfo.setEnabled(True)
        else:
	   # user canceled
           self.statusbar.showMessage("you canceled selecting a folder for geotagging.")
           geotag_source_folder = ""

def geotag_gps_file(self, qApp):
        self.statusbar.showMessage("")
        select_file = QFileDialog(self,"Open gpx track log file")
        select_file.setFileMode(QFileDialog.ExistingFiles)
        qApp.processEvents()
        if platform.system() == "Darwin":
            select_file.setDirectory(os.path.expanduser('~/Pictures'))
        elif platform.system() == "Linux":
            select_file.setDirectory(os.path.expanduser('~/Pictures'))
        elif platform.system() == "Windows":
            select_file.setDirectory(os.path.expanduser('~/My Pictures'))
        qApp.processEvents()
        select_file.setViewMode(QFileDialog.Detail)
        #select_file.setNameFilter("gpx track log files (*.gpx *.GPX *.log *.LOG)\nAll files (*.*)")
        geotag_gps_file = ""
        if select_file.exec_():
           print("select file exec")
           geotag_gps_file = select_file.selectedFiles()[0]
           self.geotag_gps_file = geotag_gps_file
           print("file should be selected")
           self.LineEdit_geotag_log_file.setText(geotag_gps_file)
           #print(str(self.geotag_gps_file))
        else:
	   # user canceled
           self.statusbar.showMessage("you canceled selecting the GPS track log file.")
           geotag_gps_file = ""

#------------------------------------------------------------------------
# Edit -> Lens tab and actions
def clear_lens_fields(self):
        self.lens_make.setText("")
        self.lens_model.setText("")
        self.lens_serialnumber.setText("")
        self.lens_focallength.setText("")
        self.lens_focallengthin35mmformat.setText("")
        self.lens_maxaperturevalue.setText("")
        self.lens_fnumber.setText("")
        self.lens_meteringmode.setCurrentIndex(0)
        #self.lens_meteringmode.setText("")

        self.chk_lens_make.setChecked(1)
        self.chk_lens_model.setChecked(1)
        self.chk_lens_serialnumber.setChecked(1)
        self.chk_lens_focallength.setChecked(1)
        self.chk_lens_focallengthin35mmformat.setChecked(1)
        self.chk_lens_maxaperturevalue.setChecked(1)
        self.chk_lens_fnumber.setChecked(1)
        self.chk_lens_meteringmode.setChecked(1)

def copylensfromselected(self,qApp):
        # First clean input fields
        clear_lens_fields(self)
        lenstool_params = ' -e -n -exif:lensmake -exif:lensmodel -exif:lensserialnumber -exif:focallength -exif:focallengthIn35mmformat -exif:fnumber -exif:maxaperturevalue -exif:meteringmode '
        p = read_image_info(self, lenstool_params)
        if len(p) == 0:
           data = False
           message = ("<p>You are trying to copy lens info from your source image, but your source image "
                      "doesn't contain the specified lens data or doesn't seem to contain any lens data (or you didn't select an image).</p>")
           ret = QMessageBox.warning(self, "Error copying lens info from source image", message)
        else:
           # remove last character which is the final ending \n (where \ is only the escape character)        
           p = p[:-1]
           p_lines = re.split('\n',p)
           rowcounter = 0
           for line in p_lines:
            #try: 
               descriptor, description = re.split(':', line,1)
               descriptor = descriptor.strip()
               description = description.strip()
               gpslat = 0
               gpslon = 0
               if descriptor == "lensmake":
                     self.lens_make.setText(description)
               if descriptor == "lensmodel":
                     self.lens_model.setText(description)
               if descriptor == "lensserialnumber":
                     self.lens_lensserialnumber.setText(description)
               if descriptor == "focallength":
                      self.lens_focallength.setText(description)
               if descriptor == "focallengthin35mmformat":
                     self.lens_focallengthin35mmformat.setText(description)
               if descriptor == "maxaperturevalue":
                     self.lens_maxaperturevalue.setText(description)
               if descriptor == "fnumber":
                     self.lens_fnumber.setText(description)
               if descriptor == "meteringmode":
                     self.lens_meteringmode.setText(description)
               #print "rowcounter " + str(rowcounter) + " descriptor " + descriptor + " ;description " + description
               rowcounter += 1

def savelensdata(self, qApp):
        lenstool_params = ""
        if self.chk_lens_make.isChecked():
               lenstool_params =  ' -exif:lensmake="' + self.lens_make.text() + ' -xmp:lensmake="' + self.lens_make.text() + '" '
        if self.chk_lens_model.isChecked():
               lenstool_params +=  '-exif:lensmodel="' + self.lens_model.text() + '-xmp:lensmodel="' + self.lens_model.text() + '" '
        if self.chk_lens_serialnumber.isChecked():
               lenstool_params +=  '-exif:lensserialnumber="' + self.lens_serialnumber.text() + '-xmp:lensserialnumber="' + self.lens_serialnumber.text() + '" '
        if self.chk_lens_focallength.isChecked():
               lenstool_params +=  '-exif:lensfocallength="' + self.lens_focallength.text() + '-xmp:lensfocallength="' + self.lens_focallength.text() + '" '
        if self.chk_lens_focallengthin35mmformat.isChecked():
               lenstool_params +=  '-exif:focallengthin35mmformat="' + self.lens_focallengthin35mmformat.text() + '-xmp:focallengthin35mmformat="' + self.lens_focallengthin35mmformat.text() + '" '
        if self.chk_lens_maxaperturevalue.isChecked():
               lenstool_params +=  '-exif:maxaperturevalue="' + self.lens_maxaperturevalue.text() + '-xmp:maxaperturevalue="' + self.lens_maxaperturevalue.text() + '" '
        if self.chk_lens_fnumber.isChecked():
               lenstool_params +=  '-exif:fnumber="' + self.lens_fnumber.text() + '-xmp:fnumber="' + self.lens_fnumber.text() + '" '
        if self.chk_lens_meteringmode.isChecked():
               lenstool_params +=  '-exif:meteringmode="' + self.lens_meteringmode.text() + '-xmp:meteringmode="' + self.lens_meteringmode.text() + '" '

        if self.chk_lens_backuporiginals.isChecked():
           write_image_info(self, lenstool_params, qApp, True)
        else:
           write_image_info(self, lenstool_params, qApp, False)
		   
#---
def date_to_datetimeoriginal(self, qApp):
    exiftool_params = " -FileModifyDate<DateTimeOriginal "
    message = "If you have modified your images in a \"sloppy\" image editor or copied them around or whatever other action(s), the file "
    message += "date/time of your images might have changed to the date your did the action/modification on the image "
    message += "where as the real file date (= creation date) of your images is most certainly (much) older.\n"
    message += "This function will take the original date/time when the photo was taken from the exif:DateTimeOriginal "
    message += "and use that (again) as file date/time.\n\n"
    message += "Do you want to continue?"
    reply = QMessageBox.question(self, "Set file date/time to DateTimeOriginal?", message, QMessageBox.Yes | QMessageBox.No)
    if reply == QMessageBox.Yes:
       write_image_info(self, exiftool_params, qApp, False)
       
#------------------------------------------------------------------------
# Other dialogs and windows and their related functions
def info_window(self):
    if self.OSplatform == "Windows":
            if os.path.isfile(os.path.join(self.parent_dir, 'COPYING')):
               # started from python
               license_file = os.path.join(self.parent_dir, 'COPYING')
            elif os.path.isfile(os.path.join(self.realfile_dir, 'COPYING')):
               # Started from the executable 
               license_file = os.path.join(self.realfile_dir, 'COPYING')
            else:
               QMessageBox.critical(self, "Can't find the license file", "Please check www.gnu.org/license")
    elif self.OSplatform == "Darwin":
            if os.path.isfile(os.path.join(self.parent_dir, 'COPYING')):
               # started from python
               license_file = os.path.join(self.parent_dir, 'COPYING')
            elif os.path.isfile(os.path.join(self.realfile_dir, "pyexiftoolgui.app","Contents","Resources","COPYING")):
               # Started from the executable 
               license_file = os.path.join(self.realfile_dir,"pyexiftoolgui.app","Contents","Resources",'COPYING')
            else:
               QMessageBox.critical(self, "Can't find the license file", "Please check www.gnu.org/license")
    else:
            license_file = os.path.join(self.parent_dir, 'COPYING')
    self.info_window_dialog = QDialog()
    self.info_window_dialog.resize(500, 640)
    self.info_window_text = QTextEdit(self.info_window_dialog)
    self.info_window_text.setGeometry(QRect(3, 11, 491, 591))
    self.info_window_text.setObjectName("info_window_text")
    self.buttonBox = QDialogButtonBox(self.info_window_dialog)
    self.buttonBox.setGeometry(QRect(300, 610, 176, 27))
    self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
    self.buttonBox.setObjectName("buttonBox")
    self.info_window_dialog.setWindowTitle(programinfo.NAME + " " + programinfo.VERSION + " license")
    self.info_window_text.setText(open(license_file).read())
    QObject.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton*)"), self.info_window_dialog.close)
    QMetaObject.connectSlotsByName(self.info_window_dialog)
    self.info_window_dialog.exec_()
#---
class dialog_synchronizedatetime(QDialog, Ui_SyncDateTimeTagsDialog):
    # This loads the py file created by pyside-uic from the ui.
    # the Quiloader segfaults on windows after ending the function
    def __init__(self, parent=None):
        super(dialog_synchronizedatetime, self).__init__(parent)
        self.setupUi(self)

def synchronizedatetime(self, qApp):
    self.synchronizedatetime_dialog = dialog_synchronizedatetime()

#---
def qddt_shift_clicked(self):
    if self.modifydatetime_dialog.chk_qddt_shift.isChecked():
       self.modifydatetime_dialog.qddt_modifydate.setEnabled(False)
       self.modifydatetime_dialog.qddt_datetimeoriginal.setEnabled(False)
       self.modifydatetime_dialog.qddt_createdate.setEnabled(False)
    else:
       self.modifydatetime_dialog.qddt_modifydate.setEnabled(True)
       self.modifydatetime_dialog.qddt_datetimeoriginal.setEnabled(True)
       self.modifydatetime_dialog.qddt_createdate.setEnabled(True)

def qddt_use_reference_image_data(self):
    if self.modifydatetime_dialog.chk_qddt_use_referencedata.isChecked():
        exiftool_params = " -exif:ModifyDate -exif:DateTimeOriginal -exif:CreateDate "
        if self.OSplatform == "Windows":
                self.referenceimage = self.referenceimage.replace("/", "\\")
                args = '"' + self.exiftoolprog + '" -a ' + exiftool_params + ' ' + self.referenceimage
                p = subprocess.check_output(args, universal_newlines=True, shell=True)
        else:
                command_line = '"' + self.exiftoolprog + '" -a ' + exiftool_params + ' ' + self.referenceimage
                args = shlex.split(command_line)
                p = subprocess.check_output(args, universal_newlines=True)
        p = p[:-1]
        p_lines = re.split('\n',p)
        for line in p_lines:
            try: 
               descriptor, description = re.split(':', line,1)
               descriptor = descriptor.strip()
               description = description.strip()
               if descriptor == "Modify Date":
                  modifydate = description
                  self.modifydatetime_dialog.qddt_modifydate.setText(modifydate)
               if descriptor == "Date/Time Original":
                  datetimeoriginal = description
                  self.modifydatetime_dialog.qddt_datetimeoriginal.setText(datetimeoriginal)
               if descriptor == "Create Date":
                  createdate = description
                  self.modifydatetime_dialog.qddt_createdate.setText(createdate)
            except:
               print("always the last line that doesn't work")

       #self.referenceimage
       #result = read_image_info(self, exiftool_params)
    else:
       now = datetime.datetime.now()
       strnow = now.strftime("%Y:%m:%d %H:%M:%S")
       self.modifydatetime_dialog.qddt_modifydate.setText(strnow)
       self.modifydatetime_dialog.qddt_datetimeoriginal.setText(strnow)
       self.modifydatetime_dialog.qddt_createdate.setText(strnow)


class dialog_modifydatetime(QDialog, Ui_DateTimeDialog):
    # This loads the py file created by pyside-uic from the ui.
    # the Quiloader segfaults on windows after ending the function
    def __init__(self, parent=None):
        super(dialog_modifydatetime, self).__init__(parent)
        self.setupUi(self)

def modifydatetime(self, qApp):
    self.modifydatetime_dialog = dialog_modifydatetime()
    now = datetime.datetime.now()
    strnow = now.strftime("%Y:%m:%d %H:%M:%S")
    self.modifydatetime_dialog.qddt_modifydate.setText(strnow)
    self.modifydatetime_dialog.qddt_datetimeoriginal.setText(strnow)
    self.modifydatetime_dialog.qddt_createdate.setText(strnow)
    self.modifydatetime_dialog.qddt_shiftdatetime.setText("0000:00:00 00:00:00")
    # Set proper event
    self.modifydatetime_dialog.chk_qddt_shift.clicked.connect(self.moddialog_shift_clicked)
    self.modifydatetime_dialog.chk_qddt_use_referencedata.clicked.connect(self.moddialog_use_reference_image_data)

    if self.modifydatetime_dialog.exec_() == QDialog.Accepted:
       print("You selected Save")
       if self.modifydatetime_dialog.chk_qddt_shift.isChecked():
          # we will do a date/time shift
          if self.modifydatetime_dialog.qddt_shiftdatetime.text() == "0000:00:00 00:00:00":
             QMessageBox.information(self,"No shift value set", "You selected the shift function but you left the value at \"0000:00:00 00:00:00\".\nI can't do anything. ")
             # exit function
             return
          else: 
             print(self.modifydatetime_dialog.qddt_shiftdatetime.text()) 
             # We will first build the parameter string and then check for forward or backward timeshift and simply use
             # a string replace on the already created exiftool_parameters string
             exiftool_params = ""
             if self.modifydatetime_dialog.chk_qddt_datetimeoriginal.isChecked():
                exiftool_params += " \"-exif:DateTimeOriginal-=" + self.modifydatetime_dialog.qddt_shiftdatetime.text() + "\" "
                if self.modifydatetime_dialog.chk_qddt_updatexmp.isChecked():
                   exiftool_params +=  " \"-xmp:DateTimeOriginal-=" + self.modifydatetime_dialog.qddt_shiftdatetime.text() + "\" "
             if self.modifydatetime_dialog.chk_qddt_modifydate.isChecked():
                exiftool_params += " \"-exif:ModifyDate-=" + self.modifydatetime_dialog.qddt_shiftdatetime.text() + "\" "
                if self.modifydatetime_dialog.chk_qddt_updatexmp.isChecked():
                   exiftool_params +=  " \"-xmp:ModifyDate-=" + self.modifydatetime_dialog.qddt_shiftdatetime.text() + "\" "
             if self.modifydatetime_dialog.chk_qddt_createdate.isChecked():
                exiftool_params += " \"-exif:CreateDate-=" + self.modifydatetime_dialog.qddt_shiftdatetime.text() + "\" "
                if self.modifydatetime_dialog.chk_qddt_updatexmp.isChecked():
                   exiftool_params +=  " \"-xmp:DateTimeDigitized-=" + self.modifydatetime_dialog.qddt_shiftdatetime.text() + "\" "

             if self.modifydatetime_dialog.chk_qddt_forward.isChecked():
                print("we are going to shift date and time forward")
                exiftool_params = exiftool_params.replace("-=", "+=")
             write_image_info(self, exiftool_params, qApp, False)
       else:
          # Update the selected date time fields, so no date/time shift
          if self.modifydatetime_dialog.chk_qddt_modifydate.isChecked():
             print("-exif:ModifyDate " + self.modifydatetime_dialog.qddt_modifydate.text())
             exiftool_params =  '-exif:ModifyDate="' + self.modifydatetime_dialog.qddt_modifydate.text() + '" '
             if self.modifydatetime_dialog.chk_qddt_updatexmp.isChecked():
               exiftool_params +=  '-xmp:ModifyDate="' + self.modifydatetime_dialog.qddt_modifydate.text() + '" '
          if self.modifydatetime_dialog.chk_qddt_datetimeoriginal.isChecked():
             print(self.modifydatetime_dialog.qddt_datetimeoriginal.text())
             exiftool_params +=  '-exif:DateTimeOriginal="' + self.modifydatetime_dialog.qddt_datetimeoriginal.text() + '" '
             if self.modifydatetime_dialog.chk_qddt_updatexmp.isChecked():
                exiftool_params +=  '-xmp:DateTimeOriginal="' + self.modifydatetime_dialog.qddt_datetimeoriginal.text() + '" '
          if self.modifydatetime_dialog.chk_qddt_createdate.isChecked():
             print(self.modifydatetime_dialog.qddt_createdate.text())
             exiftool_params +=  '-exif:CreateDate="' + self.modifydatetime_dialog.qddt_createdate.text() + '" '
             if self.modifydatetime_dialog.chk_qddt_updatexmp.isChecked():
                exiftool_params +=  '-xmp:DateTimeDigitized="' + self.modifydatetime_dialog.qddt_createdate.text() + '" '
          print(exiftool_params)
          write_image_info(self, exiftool_params, qApp, False)
    else:
       print("you cancelled") 
       self.statusbar.showMessage("you canceled the \"Modification of date/time\" action")   

#---
def check_create_args_boxes(self):
    if self.create_args_dialog.qdca_chk_args_all_metadata.isChecked():
        self.create_args_dialog.qdca_chk_args_exif_data.setChecked(1)
        self.create_args_dialog.qdca_chk_args_xmp_data.setChecked(1)
        self.create_args_dialog.qdca_chk_args_gps_data.setChecked(1)
        self.create_args_dialog.qdca_chk_args_iptc_data.setChecked(1)
        self.create_args_dialog.qdca_chk_args_iccprofile_data.setChecked(1)
    else:
        self.create_args_dialog.qdca_chk_args_exif_data.setChecked(0)
        self.create_args_dialog.qdca_chk_args_xmp_data.setChecked(0)
        self.create_args_dialog.qdca_chk_args_gps_data.setChecked(0)
        self.create_args_dialog.qdca_chk_args_iptc_data.setChecked(0)
        self.create_args_dialog.qdca_chk_args_iccprofile_data.setChecked(0)

class dialog_create_args(QDialog, Ui_Dialog_create_args):
    # This loads the py file created by pyside-uic from the ui.
    # the Quiloader segfaults on windows after ending the function
    def __init__(self, parent=None):
        super(dialog_create_args, self).__init__(parent)
        self.setupUi(self)

    print("create arguments file(s) from selected image(s)")

def create_args(self, qApp):    
    self.create_args_dialog = dialog_create_args()
    # Set proper event
    self.create_args_dialog.qdca_chk_args_all_metadata.clicked.connect(self.check_create_args_boxes)

    if self.create_args_dialog.exec_() == QDialog.Accepted:
            message = "You selected:\n\n"
            empty_selection = 0
            if self.create_args_dialog.qdca_chk_args_all_metadata.isChecked():
               print("Add all metadata to args file(s)")
               message += "- Add all metadata\n"
               et_param = " -a -all "
            else:
               empty_selection = 1
               et_param = ""
               if self.create_args_dialog.qdca_chk_args_exif_data.isChecked():
                  print("Add exif data to args file(s)")
                  message += "- Add exif data\n"
                  et_param += " -a -exif:all "
                  empty_selection = 0
               if self.create_args_dialog.qdca_chk_args_xmp_data.isChecked():
                  print("Add xmp data to args file(s)")
                  message += "- Add xmp data\n"
                  et_param += " -a -xmp:all "
                  empty_selection = 0
               if self.create_args_dialog.qdca_chk_args_gps_data.isChecked():
                  print("Add gps data to args file(s)")
                  message += "- Add gps data\n"
                  et_param += " -a -gps:all "
                  empty_selection = 0
               if self.create_args_dialog.qdca_chk_args_iptc_data.isChecked():
                  print("Add iptc data to args file(s)")
                  message += "- Add iptc data\n"
                  et_param += " -a -iptc:all "
                  empty_selection = 0                  
               if self.create_args_dialog.qdca_chk_args_iccprofile_data.isChecked():
                  print("Add icc profile data to args file(s)")
                  message += "- Add icc profile data\n"
                  et_param += " -a -icc_profile:all "
                  empty_selection = 0                  
            if empty_selection == 1:
               QMessageBox.information(self,"Nothing selected", "You selected nothing. Cancel would have been the correct option.\nNothing will we done.")
            else:
               message += "\nAre you sure you want to add the above metadata from the selected image(s) to your args file(s)?"
               ret = QMessageBox.question(self, "Add metadata from image(s) to args file(s)", message, buttons=QMessageBox.Ok|QMessageBox.Cancel) 
               if ret == QMessageBox.Ok:
                  print("User wants to continue")
                  et_param += " -args --filename --directory -w args "
                  print(et_param)
                  write_image_info(self, et_param, qApp, False)
               else:
                  self.statusbar.showMessage("you canceled the \"Export metadata to args file(s)\" action")   
    else:
            print("you cancelled") 
            self.statusbar.showMessage("you canceled the \"Export metadata to args file(s)\" action")

            
#---
def check_export_metadata_boxes(self):
# This one checks whether "export all" is checked
    if self.export_metadata_dialog.qdem_chk_export_all_metadata.isChecked():
        self.export_metadata_dialog.qdem_chk_export_exif_data.setChecked(1)
        self.export_metadata_dialog.qdem_chk_export_xmp_data.setChecked(1)
        self.export_metadata_dialog.qdem_chk_export_gps_data.setChecked(1)
        self.export_metadata_dialog.qdem_chk_export_iptc_data.setChecked(1)
        self.export_metadata_dialog.qdem_chk_export_iccprofile_data.setChecked(1)
    else:
        self.export_metadata_dialog.qdem_chk_export_exif_data.setChecked(0)
        self.export_metadata_dialog.qdem_chk_export_xmp_data.setChecked(0)
        self.export_metadata_dialog.qdem_chk_export_gps_data.setChecked(0)
        self.export_metadata_dialog.qdem_chk_export_iptc_data.setChecked(0)
        self.export_metadata_dialog.qdem_chk_export_iccprofile_data.setChecked(0)

def check_xmpexport_metadata_boxes(self):
# This one checks whether the xmp export file is checked
    #print "in the check_xmpexport_metadata_boxes"
    if self.export_metadata_dialog.qdem_xmp_radiobutton.isChecked():
        self.export_metadata_dialog.qdem_chk_export_all_metadata.setChecked(0)
        self.export_metadata_dialog.qdem_chk_export_exif_data.setChecked(0)
        self.export_metadata_dialog.qdem_chk_export_xmp_data.setChecked(1)
        self.export_metadata_dialog.qdem_chk_export_gps_data.setChecked(0)
        self.export_metadata_dialog.qdem_chk_export_iptc_data.setChecked(0)
        self.export_metadata_dialog.qdem_chk_export_iccprofile_data.setChecked(0)
        self.export_metadata_dialog.qdem_chk_export_all_metadata.setEnabled(False)
        self.export_metadata_dialog.qdem_chk_export_exif_data.setEnabled(False)
        self.export_metadata_dialog.qdem_chk_export_gps_data.setEnabled(False)
        self.export_metadata_dialog.qdem_chk_export_iptc_data.setEnabled(False)
        self.export_metadata_dialog.qdem_chk_export_iccprofile_data.setEnabled(False)
    else:
        self.export_metadata_dialog.qdem_chk_export_all_metadata.setEnabled(True)
        self.export_metadata_dialog.qdem_chk_export_exif_data.setEnabled(True)
        self.export_metadata_dialog.qdem_chk_export_xmp_data.setEnabled(True)
        self.export_metadata_dialog.qdem_chk_export_gps_data.setEnabled(True)
        self.export_metadata_dialog.qdem_chk_export_iptc_data.setEnabled(True)
        self.export_metadata_dialog.qdem_chk_export_iccprofile_data.setEnabled(True)

class dialog_export_metadata(QDialog, Ui_Dialog_export_metadata):
    # This loads the py file created by pyside-uic from the ui.
    # the Quiloader segfaults on windows after ending the function
    def __init__(self, parent=None):
        super(dialog_export_metadata, self).__init__(parent)
        self.setupUi(self)

    print("create arguments file(s) from selected image(s)")

def export_metadata(self, qApp):    
    self.export_metadata_dialog = dialog_export_metadata()
    # Set proper events
    self.export_metadata_dialog.qdem_chk_export_all_metadata.clicked.connect(self.check_export_metadata_boxes)
    self.export_metadata_dialog.qdem_txt_radiobutton.clicked.connect(self.check_xmpexport_metadata_boxes)
    self.export_metadata_dialog.qdem_tab_radiobutton.clicked.connect(self.check_xmpexport_metadata_boxes)
    self.export_metadata_dialog.qdem_xml_radiobutton.clicked.connect(self.check_xmpexport_metadata_boxes)
    self.export_metadata_dialog.qdem_html_radiobutton.clicked.connect(self.check_xmpexport_metadata_boxes)
    self.export_metadata_dialog.qdem_xmp_radiobutton.clicked.connect(self.check_xmpexport_metadata_boxes)

    if self.export_metadata_dialog.exec_() == QDialog.Accepted:
            message = "You selected:\n\n"
            empty_selection = 0
            if self.export_metadata_dialog.qdem_chk_export_all_metadata.isChecked():
               print("export all metadata")
               message += "- export all metadata\n"
               et_param = " -a -all "
            else:
               empty_selection = 1
               et_param = ""
               if self.export_metadata_dialog.qdem_chk_export_exif_data.isChecked():
                  print("export exif data")
                  message += "- export exif data\n"
                  et_param += " -a -exif:all "
                  empty_selection = 0
               if self.export_metadata_dialog.qdem_chk_export_xmp_data.isChecked():
                  print("export xmp data")
                  message += "- export xmp data\n"
                  et_param += " -a -xmp:all "
                  empty_selection = 0
               if self.export_metadata_dialog.qdem_chk_export_gps_data.isChecked():
                  print("export gps data")
                  message += "- export gps data\n"
                  et_param += " -a -gps:all "
                  empty_selection = 0
               if self.export_metadata_dialog.qdem_chk_export_iptc_data.isChecked():
                  print("export iptc data")
                  message += "- export iptc data\n"
                  et_param += " -a -iptc:all "
                  empty_selection = 0                  
               if self.export_metadata_dialog.qdem_chk_export_iccprofile_data.isChecked():
                  print("export icc profile data")
                  message += "- export icc profile data\n"
                  et_param += " -a -icc_profile:all "
                  empty_selection = 0                  
            if empty_selection == 1:
               QMessageBox.information(self,"Nothing selected", "You selected nothing. Cancel would have been the correct option.\nNothing will we done.")
            else:
               message += "\nAre you sure you want to export the above metadata from the selected image(s)?"
               ret = QMessageBox.question(self, "export metadata from image(s)", message, buttons=QMessageBox.Ok|QMessageBox.Cancel) 
               if ret == QMessageBox.Ok:
                  print("User wants to continue")
                  print(et_param)
                  if self.export_metadata_dialog.qdem_txt_radiobutton.isChecked():
                          et_param += " -w! txt "
                  elif self.export_metadata_dialog.qdem_tab_radiobutton.isChecked():
                          et_param += " -t -w! txt "
                  elif self.export_metadata_dialog.qdem_xml_radiobutton.isChecked():
                          et_param += " -X -w! xml "
                  elif self.export_metadata_dialog.qdem_html_radiobutton.isChecked():
                          et_param += " -h -w! html "
                  elif self.export_metadata_dialog.qdem_xmp_radiobutton.isChecked():
                          et_param = " xmpexport "
                  elif self.export_metadata_dialog.qdem_csv_radiobutton.isChecked():
                          et_param += " -csv "
                  write_image_info(self, et_param, qApp, False)
               else:
                  self.statusbar.showMessage("you canceled the \"Export of metadata\" action")   
    else:
            print("you cancelled") 
            self.statusbar.showMessage("you canceled the \"Export of metadata\" action")   


#---
def check_remove_metadata_boxes(self):
    if self.rem_metadata_dialog.chk_rem_all_metadata.isChecked():
        self.rem_metadata_dialog.chk_rem_exif_data.setChecked(1)
        self.rem_metadata_dialog.chk_rem_xmp_data.setChecked(1)
        self.rem_metadata_dialog.chk_rem_gps_data.setChecked(1)
        self.rem_metadata_dialog.chk_rem_iptc_data.setChecked(1)
        self.rem_metadata_dialog.chk_rem_iccprofile_data.setChecked(1)
    else:
        self.rem_metadata_dialog.chk_rem_exif_data.setChecked(0)
        self.rem_metadata_dialog.chk_rem_xmp_data.setChecked(0)
        self.rem_metadata_dialog.chk_rem_gps_data.setChecked(0)
        self.rem_metadata_dialog.chk_rem_iptc_data.setChecked(0)
        self.rem_metadata_dialog.chk_rem_iccprofile_data.setChecked(0)


class dialog_remove_metadata(QDialog, Ui_Dialog_remove_metadata):
    # This loads the py file created by pyside-uic from the ui.
    # the Quiloader segfaults on windows after ending the function
    def __init__(self, parent=None):
        super(dialog_remove_metadata, self).__init__(parent)
        self.setupUi(self)

      
def remove_metadata(self, qApp):    
#    ui = os.path.join(self.ui_dir, "remove_metadata.ui")
#    loader = QUiLoader()
#    if self.OSplatform == "Windows":
#       #uifile = QFile ("scripts\\ui\\remove_metatada.ui")
#       #file = QFile(":/forms/myform.ui")
#       ui = ui.replace("/", "\\")
#       print "ui " + ui
#    uifile = QFile(ui)
#    uifile.open(QFile.ReadOnly)
#    self.rem_metadata_dialog = loader.load(uifile, self)
#    uifile.close()
#    self.rem_metadata_dialog.adjustSize()


    self.rem_metadata_dialog = dialog_remove_metadata()
    # Set proper event
    self.rem_metadata_dialog.chk_rem_all_metadata.clicked.connect(self.check_remove_metadata_boxes)

    if self.rem_metadata_dialog.exec_() == QDialog.Accepted:
            message = "You selected:\n\n"
            empty_selection = 0
            if self.rem_metadata_dialog.chk_rem_all_metadata.isChecked():
               print("Remove all metadata")
               message += "- Remove all metadata\n"
               et_param = " -all= "
            else:
               empty_selection = 1
               et_param = ""
               if self.rem_metadata_dialog.chk_rem_exif_data.isChecked():
                  print("Remove exif data")
                  message += "- Remove exif data\n"
                  et_param += " -exif:all= "
                  empty_selection = 0
               if self.rem_metadata_dialog.chk_rem_xmp_data.isChecked():
                  print("Remove xmp data")
                  message += "- Remove xmp data\n"
                  et_param += " -xmp:all= "
                  empty_selection = 0
               if self.rem_metadata_dialog.chk_rem_gps_data.isChecked():
                  print("Remove gps data")
                  message += "- Remove gps data\n"
                  et_param += " -gps:all= "
                  empty_selection = 0
               if self.rem_metadata_dialog.chk_rem_iptc_data.isChecked():
                  print("Remove iptc data")
                  message += "- Remove iptc data\n"
                  et_param += " -iptc:all= "
                  empty_selection = 0                  
               if self.rem_metadata_dialog.chk_rem_iccprofile_data.isChecked():
                  print("Remove icc profile data")
                  message += "- Remove icc profile data\n"
                  et_param += " -icc_profile:all= "
                  empty_selection = 0                  
            if empty_selection == 1:
               QMessageBox.information(self,"Nothing selected", "You selected nothing. Cancel would have been the correct option.\nNothing will we done.")
            else:
               message += "\nAre you sure you want to remove the above metadata from the selected image(s)?"
               ret = QMessageBox.question(self, "Remove metadata from image(s)", message, buttons=QMessageBox.Ok|QMessageBox.Cancel) 
               if ret == QMessageBox.Ok:
                  print("User wants to continue")
                  print(et_param)
                  if self.rem_metadata_dialog.chk_rem_backuporiginals.isChecked():
                     print("make backup of originals")
                     write_image_info(self, et_param, qApp, True)
                  else:
                     write_image_info(self, et_param, qApp, False)
               else:
                  self.statusbar.showMessage("you canceled the \"Removal of metadata\" action")   
    else:
            print("you cancelled") 
            self.statusbar.showMessage("you canceled the \"Removal of metadata\" action")   

#------------------------------------------------------------------------
# This is the part where the geotag functions will be executed
def write_geotag_info(self,qApp):
       # First check if we have something to work on
       result = check_geotag_folder_before_run_geotag_photos(self)
       if result == "nothing_to_work_with":
          # error message already displayed, exit function
          return
       else:
          # work_on gets the geotag folder or the main images screen selection
          work_on = result
          # Now check whether we have a GPS track log file
          if self.LineEdit_geotag_log_file.text() == "":
		# user did not specify a GPS track log file
		QMessageBox.information(self,"No GPS track log file", "You did not select a GPS track log file\n. Cancelling this action")
		return "nothing_to_work_with"
          else:
		# At this stage we have images and a track log file
		run_geotag_photos(self, work_on, qApp)
        
#---
def check_geotag_folder_before_run_geotag_photos(self):
    print("self.LineEdit_geotag_source_folder #" + self.LineEdit_geotag_source_folder.text() + "#")
    if self.LineEdit_geotag_source_folder.text() == "":
       # user did not select a source folder, now check in the except whether he/she selected images in the main screen
       try:
           #if len(self.fileNames) == 0:
           selected_rows = self.MaintableWidget.selectedIndexes()
           if len(selected_rows) == 0:
                  QMessageBox.information(self,"Nothing to work with","You did not specify a source folder and neither did you load/select any photos in the main screen.")
                  return "nothing_to_work_with"
           else:
                  # just exit this function with the option "main_screen_selection"
                  print("main_screen_selection")
                  return "main_screen_selection"
       except:
           QMessageBox.information(self,"Nothing to work with","You did not specify a source folder and neither did you load/select any photos in the main screen.")
           return "nothing_to_work_with"
    else:
      # just exit this function with the option rename_source_folder (this is not the path)
      print("geotag_source_folder")
      return "geotag_source_folder"

#---
def run_geotag_photos(self, work_on, qApp):
       # Now do the real work
       # Check whether user specified a geosync time
       if self.LineEdit_geotagging_geosynctime.text() == "":
          exiftoolparams = " -P -overwrite_original_in_place -geotag '" + self.LineEdit_geotag_log_file.text() + "'"
          xmpparams = " -P -overwrite_original_in_place -xmp:geotag='" + self.LineEdit_geotag_log_file.text() + "'"
       else:
          # A geosync time has been specified. just make sure to remove extra quotes or double quotes
          gstime = self.LineEdit_geotagging_geosynctime.text()
          gstime = gstime.replace("'", "")
          gstime = gstime.replace('"', '')
          exiftoolparams = " -P -overwrite_original_in_place -geotag '" + self.LineEdit_geotag_log_file.text() + "' -geosync=" + gstime + " "
          xmpparams = " -P -overwrite_original_in_place -xmp:geotag='" + self.LineEdit_geotag_log_file.text() + "' -geosync=" + gstime + " "

       # final check
       if work_on == "nothing_to_work_with":
          # This should already been dealt with earlier, but in case I did something stupid we simply exit this function
          return
       elif work_on == "main_screen_selection":
          # we use the images that were selected from the main screen
          print("we use the images that were selected from the main screen")
          selected_rows = self.MaintableWidget.selectedIndexes()
          #exiftoolparams = "'-FileName<" + self.prefix + "_" + self.suffix + ".%le' " + self.prefixformat + " " + self.suffixformat + "-." + self.combobox_digits.currenttext() + "nc" + self.sourcefolder + "/*"
          rowcounter = 0
          total_rows = len(selected_rows)
          self.progressbar.setRange(0, total_rows)
          self.progressbar.setValue(0)
          self.progressbar.show()
          rows = []
          qApp.processEvents()
          for selected_row in selected_rows:
                selected_row = str(selected_row)
                selected_row = selected_row.replace("<PySide.QtCore.QModelIndex(",'')
                selected_row, tail = re.split(',0x0',selected_row)
                #print str(selected_row)
                row, column = re.split(',',selected_row)
                if row not in rows:
                        rows.append(row)
                        selected_image = "\"" + self.fileNames[int(row)] + "\""
                        print('exiftool ' + exiftoolparams + ' ' + selected_image)
                        rowcounter += 1
                        self.progressbar.setValue(rowcounter)
                        parameters = ' ' + exiftoolparams + ' ' + selected_image
                        xmpparameters = ' ' + xmpparams + ' ' + selected_image
                        self.statusbar.showMessage("Trying to geotag " + os.path.basename(selected_image))
                        qApp.processEvents()
                        if self.OSplatform in ("Windows", "win32"):
                           parameters = parameters.replace("/", "\\")
                           parameters = parameters.replace("'", "\"")
                           xmpparameters = xmpparameters.replace("/", "\\")
                           xmpparameters = xmpparameters.replace("'", "\"")
                           args = '"' + self.exiftoolprog + '" ' + parameters
                           xmpargs = '"' + self.exiftoolprog + '" ' + xmpparameters
                           print(args)
                           print(xmpargs)
                           p = subprocess.call(args, shell=True)
                           p = subprocess.call(xmpargs, shell=True)
                        else:
                           #parameters = parameters.replace("'", "\"")
                           command_line = '"' + self.exiftoolprog + '" ' + exiftoolparams + ' ' + selected_image
                           xmp_command_line = '"' + self.exiftoolprog + '" ' + xmpparams + ' ' + selected_image
                           args = shlex.split(command_line)
                           xmpargs = shlex.split(xmp_command_line)
                           print("command_line " + command_line)
                           print("xmp command_line " + xmp_command_line)
                           #p = subprocess.call(command_line)
                           p = subprocess.call(args)
                           p = subprocess.call(xmpargs)
                self.statusbar.showMessage("Finished geotagging images where timestamps fit.")
                qApp.processEvents()
          self.progressbar.hide()
          self.statusbar.showMessage("")
       elif work_on == "geotag_source_folder":
          # work on all images in the source folder and do it in this function self
          #print "work on all images in the source folder"
          #print self.rename_photos_dialog.LineEdit_rename_source_folder.text()
          self.statusbar.showMessage("Trying to geotag all images in: " + self.LineEdit_geotag_source_folder.text())
          print("Trying to geotag all images in: " + self.LineEdit_geotag_source_folder.text())
          parameters = exiftoolparams + ' "' + self.LineEdit_geotag_source_folder.text() + '"'
          xmpparameters = xmpparams + ' "' + self.LineEdit_geotag_source_folder.text() + '"'
          if self.OSplatform in ("Windows", "win32"):
              parameters = parameters.replace("/", "\\")
              parameters = parameters.replace("'", "\"")
              xmpparameters = xmpparameters.replace("/", "\\")
              xmpparameters = xmpparameters.replace("'", "\"")
              args = '"' + self.exiftoolprog + '" ' + parameters
              xmpargs = '"' + self.exiftoolprog + '" ' + xmpparameters
              print("args " + args)
              print("xmpargs " + xmpargs)
              p = subprocess.call(args, shell=True)
              p = subprocess.call(xmpargs, shell=True)
          else:
              pathofimages = self.LineEdit_geotag_source_folder.text().replace(" ", "\\ ")
              command_line = '"' + self.exiftoolprog + '" ' + exiftoolparams + ' "' + pathofimages + '"'
              xmpcommand_line = '"' + self.exiftoolprog + '" ' + xmpparams + ' "' + pathofimages + '"'
              print("command_line " + command_line)
              print("xmpcommandline " + xmpcommand_line)
              p = subprocess.call(command_line, shell=True)
              p = subprocess.call(xmpcommand_line, shell=True)
          self.statusbar.showMessage("Finished geotagging all images in: " + self.LineEdit_geotag_source_folder.text() + " where timestamps fit.")


#------------------------------------------------------------------------
# This is the part where your own exiftool parameters will be executed
def yourcommands_go(self, qApp):
        output_text = ""
        exiftoolparams = " " + self.yourcommands_input.text() + " "
        mysoftware = programinfo.NAME + " " + programinfo.VERSION
        ''''if self.OSplatform in ("Windows", "win32"):
           exiftoolparams = " -ProcessingSoftware=\"" + mysoftware + "\" " + exiftoolparams
        else:
           exiftoolparams = " -ProcessingSoftware='" + mysoftware + "' " + exiftoolparams
        '''
        selected_rows = self.MaintableWidget.selectedIndexes()
        if len(selected_rows) == 0:
            self.the_no_photos_messagebox()
        else:
           print('number of rows ' + str(len(selected_rows)))
           rowcounter = 0
           total_rows = len(selected_rows)
           self.progressbar.setRange(0, total_rows)
           self.progressbar.setValue(0)
           self.progressbar.show()
           rows = []
           for selected_row in selected_rows:
                selected_row = str(selected_row)
                selected_row = selected_row.replace("<PySide.QtCore.QModelIndex(",'')
                selected_row, tail = re.split(',0x0',selected_row)
                #print str(selected_row)
                row, column = re.split(',',selected_row)
                if row not in rows:
                        rows.append(row)
                        selected_image = "\"" + self.fileNames[int(row)] + "\""
                        print('exiftool ' + exiftoolparams + ' ' + selected_image)
                        rowcounter += 1
                        self.progressbar.setValue(rowcounter)
                        if self.OSplatform in ("Windows", "win32"):
                            # First write the info
                            selected_image = selected_image.replace("/", "\\")
                            args = '"' + self.exiftoolprog + '" ' + exiftoolparams + selected_image
                            try:
                                p = subprocess.check_output(args, universal_newlines=True, shell=True)
                            except:
                                p = "Your parameter(s) is/are wrong and could not be executed at all by exiftool.\nTherefore you don't get output."
                        else:
                            # First write the info
                            command_line = '"' + self.exiftoolprog + '" ' + exiftoolparams + selected_image
                            print(command_line)
                            args = shlex.split(command_line)
                            try:
                                p = subprocess.check_output(args, universal_newlines=True)
                            except:
                                p = "Your parameter(s) is/ware wrong and could not be executed at all by exiftool.\nTherefore you don't get output."
                        if p == "":
                           p = "Your parameters did not return output.\nEither there is no output or you did something wrong."
                        p = p[:-1]
                        #p_lines = re.split('\n',p)
                        self.statusbar.showMessage("Executing your parameter(s) on: " + selected_image)
                        self.yourcommands_output.insertPlainText("==== " + selected_image + " ====\n")
                        self.yourcommands_output.insertPlainText(str(p))
                        self.yourcommands_output.insertPlainText("\n\n\n")

           self.progressbar.hide()
           self.statusbar.showMessage("Finished executing your parameter(s)")

#------------------------------------------------------------------------
# Real exiftool read/write functions
def read_image_info(self, exiftool_params):
        self.statusbar.showMessage("")
        selected_row = self.MaintableWidget.currentRow()
        selected_image = "\"" + self.fileNames[selected_row] + "\""
        if self.OSplatform in ("Windows", "win32"):
                selected_image = selected_image.replace("/", "\\")
                args = '"' + self.exiftoolprog + '" ' + exiftool_params + selected_image                
                p = subprocess.check_output(args, universal_newlines=True, shell=True)
        else:
                command_line = '"' + self.exiftoolprog + '" ' + exiftool_params + selected_image
                args = shlex.split(command_line)
                p = subprocess.check_output(args, universal_newlines=True)
        return p

def write_image_info(self, exiftoolparams, qApp, backup_originals):
        mysoftware = programinfo.NAME + " " + programinfo.VERSION
        xmpexportparam = ""
        # silly if/elif/else statement. improve later
        if " -w! " in exiftoolparams:
           # exporting metadata
           print("exporting metadata")
           #exiftoolparams += " -overwrite_original_in_place "
        elif " -csv " in exiftoolparams:
           # Create args file(s) from selected images(s)
           print("Exporting metadata from selected images(s)to csv file")
           images_to_csv = exiftoolparams + ' '
        elif " -args " in exiftoolparams:
           # Create args file(s) from selected images(s)
           print("Create args file(s) from selected images(s)")
        elif " xmpexport " in exiftoolparams:
           # Create xmp file(s) from selected images(s) only for xmp data
           print("Create xmp file(s) from selected images(s) only for xmp data")
           # create extra variable otherwise exiftoolparams ovewrites original xmpexport string, bit clumsy but it works
           xmpexportparam = exiftoolparams
        elif " -FileModifyDate<DateTimeOriginal " in exiftoolparams:
           print("Only change file date/time to DateTimeOriginal")
        else:
           # writing metadata info to photos
           if backup_originals == True:
                if self.OSplatform in ("Windows", "win32"):
                   exiftoolparams = " -P -ProcessingSoftware=\"" + mysoftware + "\" " + exiftoolparams
                else:
                   exiftoolparams = " -P -ProcessingSoftware='" + mysoftware + "' " + exiftoolparams
           else:
                if self.OSplatform in ("Windows", "win32"):
                   exiftoolparams = " -P -overwrite_original_in_place -ProcessingSoftware=\"" + mysoftware + "\" " + exiftoolparams
                else:
                   exiftoolparams = " -P -overwrite_original_in_place -ProcessingSoftware='" + mysoftware + "' " + exiftoolparams

        selected_rows = self.MaintableWidget.selectedIndexes()
        print('number of rows ' + str(len(selected_rows)))
        rowcounter = 0
        total_rows = len(selected_rows)
        self.progressbar.setRange(0, total_rows)
        self.progressbar.setValue(0)
        self.progressbar.show()
        rows = []
        for selected_row in selected_rows:
                selected_row = str(selected_row)
                selected_row = selected_row.replace("<PySide.QtCore.QModelIndex(",'')
                selected_row, tail = re.split(',0x0',selected_row)
                #print str(selected_row)
                row, column = re.split(',',selected_row)
                if row not in rows:
                        rows.append(row)
                        selected_image = "\"" + self.fileNames[int(row)] + "\""
                        print('exiftool ' + exiftoolparams + ' ' + selected_image)
                        #print 'exiftool "-FileModifyDate<DateTimeOriginal" ' + selected_image
                        rowcounter += 1
                        self.progressbar.setValue(rowcounter)
                        if " -csv " in exiftoolparams:
                           # First collect images. Do not write yet
#                           if self.OSplatform in ("Windows", "win32"):
#                              images_to_csv += " " + selected_image + " "
#                           else:
                           images_to_csv += ' ' + selected_image + ' '
                           #print images_to_csv
                        else: 
                           # All other actions are performed per image.
                           if " -w " in exiftoolparams:
                              self.statusbar.showMessage("Exporting information from: " + os.path.basename(selected_image) + " to chosen export format")
                           elif " -args " in exiftoolparams:
                              self.statusbar.showMessage("Create args file from: " + os.path.basename(selected_image))
                           elif "copymetadatatoxmp" in exiftoolparams:
                              self.statusbar.showMessage("Create all metadata internally inside " + os.path.basename(selected_image) + " to xmp format")
                              if self.OSplatform in ("Windows", "win32"):
                                 exiftoolparams = " -TagsFromFile " + selected_image.replace("/", "\\") + " \"-all>xmp:all\" "
                              else:
                                 exiftoolparams = " -TagsFromFile " + selected_image + " '-all>xmp:all' "
                           else:
                              #check whether we do an xmp to xmp file export
                              if xmpexportparam == "":
                                 # no it's not an xmp to xmp file export, this means all other actions
                                 self.statusbar.showMessage("Writing information to: " + os.path.basename(selected_image))
                              else:
                                 # less frequent so put the xmp export to xmp here
                                 self.statusbar.showMessage("Create xmp file from: " + os.path.basename(selected_image))
                                 base = os.path.basename(selected_image)
                                 basexmp = os.path.splitext(base)[0] + ".xmp"
                                 #print "basexmp " + basexmp
                                 if os.path.isfile(os.path.join(self.image_folder, basexmp)):
                                    # remove xmp file first as exiftool doesn't overwrite
                                    fls = os.remove(os.path.join(self.image_folder, basexmp))
                                 exiftoolparams = " -o \"" + os.path.join(self.image_folder, basexmp) + "\" -xmp "
                           qApp.processEvents()
                           if self.OSplatform in ("Windows", "win32"):
                              # First write the info
                              selected_image = selected_image.replace("/", "\\")
                              args = '"' + self.exiftoolprog + '" ' + exiftoolparams + selected_image
                              p = subprocess.call(args, shell=True)
                              ## Now reset the file date
                              #args = self.exiftoolprog + ' "-FileModifyDate<DateTimeOriginal" ' + selected_image
                              #p = subprocess.call(args)
                           else:
                              # First write the info
                              command_line = '"' + self.exiftoolprog + '" ' + exiftoolparams + selected_image
                              print(command_line)
                              args = shlex.split(command_line)
                              p = subprocess.call(args)
                              ## Now reset the file date
                              #command_line = self.exiftoolprog + ' "-FileModifyDate<DateTimeOriginal" ' + selected_image
                              #args = shlex.split(command_line)
                              #p = subprocess.call(args)
        self.progressbar.hide()
        # csv option: After having collected the images
        if " -csv " in exiftoolparams:
           # Use self.image_folder from loading the images
           if self.OSplatform in ("Windows", "win32"):
              parameters = " " + images_to_csv + " > \"" + os.path.join(self.image_folder, "output.csv") + "\""
              #parameters = " " + images_to_csv + " > output.csv"
              parameters = parameters.replace("/", "\\")
              args = '"' + self.exiftoolprog + '" ' + parameters
              print(args)
              p = subprocess.call(args, shell=True)
           else:
              command_line = '"' + self.exiftoolprog + '" ' + images_to_csv + ' > \'' + os.path.join(self.image_folder, 'output.csv') + '\''
              #args = shlex.split(command_line)
              print(command_line)
              #p = subprocess.call(args,shell=True)
              p = subprocess.call(command_line,shell=True)
        # end of csv option
        if " -w " in exiftoolparams:
           self.statusbar.showMessage("Done exporting the metadata for the selected image(s)")
        elif " -args " in exiftoolparams:
           self.statusbar.showMessage("Done creating the args file(s) for the selected image(s)")
        elif " -csv " in exiftoolparams:
           self.statusbar.showMessage("Done creating the csv file for the selected image(s)")
        else:
           self.statusbar.showMessage("Done writing the info to the selected image(s)")
