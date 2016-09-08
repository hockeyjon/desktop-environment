#! /bin/bash


# MUST assume that we have cloned the repo and it is the current working directory
#mkdir git
#cd git
#git clone git@github.com:hockeyjon/ubuntu.git myUbuntu
cp bashrc $HOME/.bashrc


#Install desktop image
cp BlueOrangePeel.jpg $HOME/Pictures/.
gsettings set org.gnome.desktop.background picture-uri file://$HOME/Pictures/BlueOrangePeel.jpg

# DEBUG:
# This computer isn't linked to any Dropbox account...
# Please visit https://www.dropbox.com/cli_link_nonce?nonce=335808286e520b06a09b7bdda6142a40 to link this device.
#    
#Install Dropbox
#if [ `uname -a | grep x86_64 | wc -l` -eq "1" ]; then 
#    echo "Installing 64 bit drop box"
#    cd ~ && wget -O - "https://www.dropbox.com/download?plat=lnx.x86_64" | tar xzf -
#else 
#    echo "Installing 32 bit drop box"
#    cd ~ && wget -O - "https://www.dropbox.com/download?plat=lnx.x86" | tar xzf -
#fi
# ~/.dropbox-dist/dropboxd

#Configure VNC to use Ubuntu desktop
mkdir ~/.vnc
cp xstartup ~/.vnc/.

echo "Set VNC password with 'vncpasswd' command."
