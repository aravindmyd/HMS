# HOSPITAL MANAGEMENT SYSTEM!

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/aravindmyd/HMS)
### Installation

HMS requires [Python](https://www.python.org/downloads/) 3.6+  to run.

Clone the Project,unzip it and Enter the Following commands:

```sh
$ cd HMS
$ pip install -r requirements.txt
$ set FLASK_APP="main.py" (FOR LINUX/MAC USERS)
$ $env:FLASK_APP = "main.py" (FOR WINDOWS USERS)
$ flask run
```
This will start the Flask Server but we need to start the MySQL database and create necessary tables.
To do that:
```sh
$ cd DB
```
Copy the **HMS** sql file and run it on your sql Server and start the server.
Once you start the MySQL database you need to update your **User Name**, **Password** and **Port Number** on your main.py file
