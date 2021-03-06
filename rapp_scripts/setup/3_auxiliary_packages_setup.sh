#!/bin/bash -i

##

#Copyright 2015 RAPP

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

    #http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# Authors: Manos Tsardoulias
# Contact: etsardou@iti.gr
##

##
#  Install required external auxiliary packages.
##


echo -e "\e[1m\e[103m\e[31m [RAPP] Installing auxiliary packages \e[0m"
# Allow remote secure connections to the RAPP-Platform.
sudo apt-get install -y openssh-server
# Remove this? Let developers choose their editor.
sudo apt-get install -y vim
# Remove this?
sudo apt-get install -y git gitg
# Rapp-Text-To-Speech module depends on this.
sudo apt-get install -y espeak
# Rapp-Text-To-Speech module depends on this.
sudo apt-get install -y mbrola*
# Python package manager.
sudo apt-get install -y python-pip
#
sudo apt-get install -y npm nodejs
