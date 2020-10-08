# **Web Service** for Wireless Sensor Networks Management

Built with Python Flask and Celery. <br>
Web Service forms the link between the Application and Server. 
* Accepts the requests of the Application and forwards them to the Server in the required format.
* Returns to the Application the answers sent by the Server. 

### Installation
1) Install pip (pip3)
    - `sudo apt install python3-pip`
2) Install pipenv
    - `sudo -H pip3 install -U pipenv`
    - Install dependencies
        - `pipenv install` (from Pipfile)
3) Install Redis-Server
    - `sudo apt install redis-server`

### Configuration
You can adjust the project settings with the following files:
- `src/config.py`
- `src/.env`

### Run
- `./run_flask`
- `./run_celery`
