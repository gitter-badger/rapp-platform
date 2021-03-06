#!/bin/bash

###
# MIT License (MIT)
#
# Copyright (c) <2014> <Rapp Project EU>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Authors: Konstantinos Panayiotou, Manos Tsardoulias
# contact: klpanagi@gmail.com
#
###


# color list
colors ()
{
  RESET='\e[0m'
  BLACK='\e[1;30m'
  RED='\e[0;31m'
  GREEN='\e[0;32m'
  YELLOW='\e[0;33m'
  BLUE='\e[0;34m'
  PURPLE='\e[0;35m'
  CYAN='\e[0;36m'
  WHITE='\e[0;37m'

  BOIBLACK='\e[1;100m'
  BRED='\e[1;31m'
  BGREEN='\e[1;32m'
  BYELLOW='\e[1;33m'
  BBLUE='\e[1;34m'
  BPURPLE='\e[1;35m'
  BCYAN='\e[1;36m'
  BWHITE='\e[1;37m'
}; colors


################################################################################
############################# Configure HOP Server #############################
################################################################################

## Get this script file directory name
CURRENTDIR=$(dirname ${BASH_SOURCE[0]})

## Set executable paths ##
SERVICEDIR=${CURRENTDIR}/services
JSFILE=init.js
JSEXECPATH=${SERVICEDIR}/${JSFILE}
CFG_DIR=${CURRENTDIR}/config

## Hop Web Server run on this port
PORT=9001

## Define the scheduler type to be used
SCHEDULER="accept-many"

## Maximum number of handling HTTP requests.
MAXTHREADS=100

## Logging definitions
# Timestamp to be added onto log file name
TIMESTAMP=`date -d "today" +"%Y%m%d%H%M"`
LOGDIR="/home/${USER}/.hop/log/server"
LOGFILENAME="hop-server-${TIMESTAMP}.log"
LOGFILE="${LOGDIR}/${LOGFILENAME}"
CAPTUREFILE="/home/${USER}/capturefile.log"
CLIENTOUTPUT="/home/${USER}/client-output.log"
USE_CAPTUREFILE=false
USE_CLIENTOUTPUT=false

## File caching configurations
CACHEDIR="/home/${USER}/.hop/cache/server"
CLEARCACHE=true

## HOP Server Configurations.
FAST_SERVER_EVENT=false
REPORT_EXECTIME=false

## Verbosity ##
VERB_LEVEL=1 #10 Default
DEBUG_LEVEL=1 #10 Default
WARN_LEVEL=1 #10 Default
SECURITY_LEVEL=0

##      HOP RC      ##
RC_FILENAME="hoprc.js"
RC_FILE="${CFG_DIR}/${RC_FILENAME}"


################################################################################
########################## Assign HOP Server parameters ########################
################################################################################

FLAGS=" -v${VERB_LEVEL} "
FLAGS+=" -g${DEBUG_LEVEL} "
FLAGS+=" -w${WARN_LEVEL} "
FLAGS+=" -s${SECURITY_LEVEL} "

if [ ${CLEARCACHE} == true ]; then
  FLAGS+=" --clear-cache "
else
  FLAGS+=" --no-clear-cache "
fi

if [ ${FAST_SERVER_EVENT} == true ]; then
  FLAGS+=" --fast-server-event"
else
  FLAGS+=" --no-fast-server-event"
fi

FLAGS+=" --cache-dir ${CACHEDIR} "
FLAGS+=" --http-port ${PORT} "
FLAGS+=" --log-file ${LOGFILE} "
if [ ${USE_CAPTUREFILE} == true ]; then
  FLAGS+=" --capture-file ${CAPTUREFILE}"
fi
if [ ${USE_CLIENTOUTPUT} == true ]; then
  FLAGS+=" --client-output ${CLIENTOUTPUT}"
fi
FLAGS+=" --scheduler ${SCHEDULER}"
FLAGS+=" --max-threads ${MAXTHREADS}"

if [ ${REPORT_EXECTIME} = true ]; then
  FLAGS+=" --time "
fi

FLAGS+=" --rc-file ${RC_FILE} "

################################################################################
################################################################################

## If log directory does not exist... Maybe create it?!! ##
if [ ! -d ${LOGDIR} ]; then
  echo -e "--- Log Directory [${LOGDIR}] does not exist. Creating now."
  mkdir -p ${LOGDIR}
fi

## If log file does not exists create it. ##
if [ ! -f ${LOGFILE} ]; then
  touch ${LOGFILE}
fi

# If file caching directory does not exist... Maybe create it?!! ##
# Hop server creates it for us!!!!
#if [ ! -d ${CACHEDIR} ]; then
  #echo -e "--- Cache Directory [${CACHEDIR}] does not exist. Creating now."
  #mkdir -p ${CACHEDIR}
#fi


################# [ Inform on HOP registered configurations ] ##################
################################################################################

echo -e "${BYELLOW}Hop configuration parameters passed:${BLUE}"
echo -e "  * Http-Port: ${PORT}"
echo -e "  * Server Cache directory: ${CACHEDIR}"
echo -e "  * Clear cache directory: ${CLEARCACHE}"
echo -e "  * Server log directory: ${LOGDIR}"
echo -e "  * Scheduler policy: ${SCHEDULER}"
echo -e "  * Max threads: ${MAXTHREADS}"
echo -e "  * Report execution time: ${REPORT_EXECTIME}"
echo -e "  * Verbosity level: ${VERB_LEVEL}"
echo -e "  * Debug level: ${DEBUG_LEVEL}"
echo -e "  * Warning level: ${WARN_LEVEL}"
echo -e "  * Security level: ${SECURITY_LEVEL}"
echo -e "${RESET}"

################################################################################
################################################################################


echo -e "${BYELLOW}Initialing Hop Web Server and registering Web Services${RESET}"
set -o xtrace
# Do not detach!!
hop ${FLAGS} ${JSEXECPATH}
set +o xtrace
##### ...
