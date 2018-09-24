#! /usr/bin/env bash

echo " __________  __       __ __    __     __"
echo "|__________| ||\      || ||\   \\\     //"
echo "     ||      || \     || || \   \\\   //"
echo "     ||      ||  \    || ||  \   \\\ //"
echo "     ||      ||   \   || ||   |    //"
echo "     ||      ||    \  || ||  /    //"
echo " ____||____  ||     \ || || /    //"
echo "|__________| ||      \|| ||/    //"

echo -e "\n ----- Running the DEMO ------- \n"

# if you forget to supply virtual environment name
if [ -z "$1" ]
then
    echo "No argument supplied"
    exit 1
fi

# to check whether the script is run from the correct directory
cur_dir=$( pwd | grep "/indy-sdk/samples/python$" )

if [ $(echo $?) -eq 1 ]
then
  echo "Change your directory to /indy-sdk/samples/python and then run the script"
  exit 1
fi

# name of the environment
virtual_env_name=$1
# cannot run workon without this
source /usr/local/bin/virtualenvwrapper.sh

echo "Switching to the virtual environment ${virtual_env_name}"
# switch to the virtual environment
workon ${virtual_env_name}

echo "Starting the pool of indy-nodes"
# start the indy nodes
docker run -itd -p 9701-9708:9701-9708 indy_pool

echo "Running the demo python script"
# run the demo python script
python -m src.getting_started

echo "The demo was successfull"
echo -e "\n\n\n"

echo "Stopping the containers"
# stop the running containers
docker stop $(docker ps -q)

echo "Removing the containers"
# delete the containers
docker rm $(docker ps -a -q)

echo "Exiting the virtual environment"
# exit the virtual environment
deactivate $1
