#! /bin/bash

cd $HOME

mkdir git
cd git
git clone git@github.com:hockeyjon/ubuntu.git myUbuntu
cp myUbuntu/bashrc $HOME/.bashrc
cp myUbuntu/BlueOrangePeel.jpg $HOME/Pictures/.
gsettings set org.gnome.desktop.background picture-uri file://$HOME/Pictures/BlueOrangePeel.jpg
