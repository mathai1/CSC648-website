# Application Folder

## Purpose
The purpose of this folder is to store all the source code and related files for your team's application. Source code MUST NOT be in any of folder. <strong>YOU HAVE BEEN WARNED</strong>

You are free to organize the contents of the folder as you see fit. But remember your team is graded on how you use Git. This does include the structure of your application. Points will be deducted from poorly structured application folders.

## Please use the rest of the README.md to store important information for your team's application.

## SET UP
### Create an environment 
Windows
```
$ py -3 -m venv venv
```
Mac
```
python3 -m venv venv
```
### Activate the environment 
Windows
```
> venv\Scripts\activate
```
Mac
```
$ . venv/bin/activate
```
### Activate the environment 
```
$ pip install Flask
```
## Install and run the application
In order to run this application, set the environment variable to this project
```
$ export FLASK_APP=application
```

# Install the dependencies
```
$ pip install -e .
```
# Run the Flask application 
```
$ flask run
```


