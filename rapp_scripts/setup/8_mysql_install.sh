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

# Authors: Manos Tsardoulias, Aris Thallas
# Contact: etsardou@iti.gr, aris.thallas@{iti.gr, gmail.com}
##

##
#  Install mysql.
##

echo -e "\e[1m\e[103m\e[31m [RAPP] MySQL install \e[0m"
if [ $# -eq 1 ]; then
  if [ $1 == 'travis' ]; then
    sudo debconf-set-selections <<< 'mysql-server mysql-server/password password travis'
    sudo debconf-set-selections <<< 'mysql-server mysql-server/password_again password travis'
  fi
fi

# Setup sources list
sudo apt-get -y install mysql-client mysql-server
sudo apt-get -y install python-mysqldb

if [ $# -eq 1 ]; then
  if [ $1 == 'travis' ]; then
    echo PURGE | sudo debconf-communicate mysql-server
  fi
fi
