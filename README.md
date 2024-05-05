# CADTech-TV
A Flask app for displaying lab availability on the front desk CADTech TV.

## Prepare your dev environment

Create and open a Python virtual environment:

`python3 -m venv .venv`
`source venv/bin/activate`


All of the required packages live in requrements.txt. To install packages from there:

`pip3 install -r requirements.txt`


Before pushing to GitHub, make sure to save packages to requirements.txt:

`pip3 freeze > requirements.txt`


## Run the project

To run the project, you need to have both Flask and pywebview running:

`flask --app flask_app run`
`python3 pywebviewer.py`


# Members
* Garrett Templar
* Matthew Incardona
* May Jiang
