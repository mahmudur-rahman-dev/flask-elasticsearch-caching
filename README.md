# query-service
Requirement for QueryService
Install Python 3.7

sudo yum update -y
sudo yum install gcc openssl-devel bzip2-devel libffi-devel -y
wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
tar xzf Python-3.7.9.tgz
cd Python-3.7.9
./configure --enable-optimizations
sudo make altinstall


Install Flask in virtual ENV

***Make venv***
python3.7 -m venv queryServiceEnv

*** Start VENV ***

source ./queryServiceEnv/bin/activate

pip install Flask

pip install -r requirements.txt





