#!/bin/bash
# This script installs the PyKickass application automatically
# It downloads and installs the necessary dependent packages and libraries 
# It also moved files and folders to the right locations and set permissions

#Author : Wong Fei Zhu (blk_ninja)
#Date 	: December 28, 2014.


clear scr
echo "Please wait while install PyKickass"
echo ""
echo "Updating System First"
apt-get update -y
clear scr
echo "Installing SQLite 3"
apt-get install sqlite3 -y
echo ""
echo "Installing Python Setup Tools"
apt-get install python-dev -y
apt-get install python-setuptools -y
echo ""
echo "Please be patient while install some python packages"
echo "Installing ouath2"
apt-get install  python-oauth2 -y
easy_install oauth2
echo "Installing matplotlib"
apt-get install python-matplotlib -y
echo "Installing pandas"
apt-get install python-pandas -y
echo "Installing prettytable"
easy_install prettytable
echo ""
echo "Installing PyKickass"
echo "Moving files and directories"
cp -r PyKickass /opt
echo "Setting permissions"
chmod 755 /opt/PyKickass -R
chmod +x /opt/PyKickass/src/main/PyKickassMain.py
echo "Adding PyKickass to Path"
ln -s /opt/PyKickass/src/main/PyKickassMain.py /usr/bin/pykickass
echo ""
echo "Finishing Installation"

