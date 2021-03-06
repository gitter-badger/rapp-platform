#!/bin/bash -ie

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
#  Build Rapp Platform onto the system.
##


RappPlatformWs="${HOME}/rapp_platform/rapp-platform-catkin-ws"

# Install libzbar used by the qr_detection module.
sudo apt-get install -y libzbar-dev
sudo ldconfig

echo -e "\e[1m\e[103m\e[31m [RAPP] Create Github folders \e[0m"
# Create folder for RAPP platform repo
if [ -d "${RappPlatformWs}" ]; then
  rm -rf ${RappPlatformWs}
fi

mkdir -p ${RappPlatformWs} && cd ${RappPlatformWs}
mkdir src && cd src

# Initialize Rapp Platform catkin workspace
catkin_init_workspace

echo -e "\e[1m\e[103m\e[31m [RAPP] Cloning the rapp-platform repo \e[0m"
# Clone the repository (public key should have been setup)
git clone --recursive git@github.com:rapp-project/rapp-platform.git
git clone git@github.com:rapp-project/rapp-api.git

## [Fetch ]
cd rapp-api/python
# Insrall Python
sudo pip install -r dependencies.txt

# Append to user's .bashrc file.
append="source ~/rapp_platform/rapp-platform-catkin-ws/devel/setup.bash --extend"
grep -q "${append}" ~/.bashrc || echo -e          \
  "\n# Rapp Platform\n${append}"                        \
  >> ~/.bashrc
echo 'export PYTHONPATH=$PYTHONPATH:~/rapp_platform/rapp-platform-catkin-ws/src/rapp-api/python' >> ~/.bashrc

# catkin_make rapp-platform
cd ${RappPlatformWs} && catkin_make -j1
