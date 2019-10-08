
[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger) [![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

# Rescue habit

A conversational based habit tracker

## Setup

### clone it
```bash
git clone https://github.com/functioncall/rescue-habit
```

### Install dependencies
```
pip install -r requirements.txt
```

### Start development live-reload server
```
python manage.py runserver
```

### Start production server:
```
<add command here>
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Instructions on how to start working on an assigned issue/bug:

* Create a separate issue/bug in the issue tracking system and assign it to a contributor.
* Take a pull from remote origin:  **(IMPORTANT STEP)**

```bash
git pull origin master
```

* Create a separate branch for your issue/bug: 
  
```bash
git checkout -b issue <issue_number>
```
```
Convention for creating branch name:
- if you are going to work on issue number 42, then your branch name should be "issue42" and, 
- if its a bug number 10, then branch name should be named as "bug10"
```

* Resolve the issue/bug and commit in local using below 2 commands: 
	
```
git add <path_of_required_files> 	
git commit -m "appropriate message goes here"
```

* push it to the remote branch : 
```
git push -u origin <branch_name>
```

* Create a pull request from bitbucket and assign it to a reviewer.
