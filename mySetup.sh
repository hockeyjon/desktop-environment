#! /bin/bash

cd $HOME

mkdir git
cd git
git clone git@github.com:hockeyjon/ubuntu.git myUbuntu
cp myUbuntu/bashrc $HOME/.bashrc


#Install desktop image
cp myUbuntu/BlueOrangePeel.jpg $HOME/Pictures/.
gsettings set org.gnome.desktop.background picture-uri file://$HOME/Pictures/BlueOrangePeel.jpg

#Install Dropbox
rc = `uname -a | grep x86_64 | wc -l`
if [ $rc -eq "1" ]; then 
    cd ~ && wget -O - "https://www.dropbox.com/download?plat=lnx.x86_64" | tar xzf -
    ~/.dropbox-dist/dropboxd
fi

