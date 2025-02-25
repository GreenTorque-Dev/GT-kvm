#!/bin/bash

# Assuming this script is in a directory within your Django project
current_script_path="$( cd "$(dirname "$0")" ; pwd -P )"

# Get the project path by going up one level from the script's directory
project_path="$(dirname "$current_script_path")"


echo "The project path is: $project_path"

cd $project_path

#file path
startwebapp_path="$project_path/startwebapp.sh"

# Install Python 3.6
sudo apt-get update

#download anaconda
sudo apt install curl
curl https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh --output anaconda.sh
bash anaconda.sh
export PATH="$HOME/anaconda3/bin:$PATH"
conda env create -f $project_path/env.yml
export PYTHON_PATH="$HOME/anaconda3/envs/venv/bin/python"
export PIP_PATH="$HOME/anaconda3/envs/venv/bin/pip"
export ENV_BIN_PATH="$HOME/anaconda3/envs/venv/bin"

sudo apt install unicorn

# Change into the cloned directory
cd $project_path

# Install build-essential and Python development tools
sudo apt-get update
sudo apt-get install -y build-essential python3-dev

# Apply migrations
$PYTHON_PATH manage.py migrate

# Create a superuser (non-interactive)
$PYTHON_PATH manage.py createsuperuser

# Create a crontab
# Inform the user that the script has completed
echo "Installation and setup completed successfully!"

# Add cron job to start the web app on reboot
sudo rm -rf $startwebapp_path
sudo touch $startwebapp_path
sudo chmod +x $startwebapp_path
echo "cd $project_path" | sudo tee -a $startwebapp_path
echo "$ENV_BIN_PATH/python manage.py runserver 0.0.0.0:8000 &" | sudo tee -a $startwebapp_path
echo "@reboot $startwebapp_path" | crontab -
$PYTHON_PATH manage.py crontab add
echo "### Below are the added cronjob! ###"
crontab -l
sudo service cron reload

# Inform the user that the script has completed
echo "Cron job added successfully!"

# Run the program
$PYTHON_PATH manage.py collectstatic
cd $project_path

#$PYTHON_PATH manage.py runserver 0.0.0.0:8000 &
echo "###"
echo "Green Cloud Services UP, Please Restart VM"
echo "###"
