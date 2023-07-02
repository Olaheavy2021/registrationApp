# registrationApp
A Django-based web application that follows the Model View Controller (MVC) paradigm. This application allows students to conveniently register and unregister for modules offered within their respective courses. Enjoy streamlined module management and an intuitive user experience.

## Requirements
- Python (3.10 or higher)
- Python Package Installer
- Virtual Environment
- Python Development Tools

## Setting up the Project
- Clone the repository from GitHub `git clone URL`
- Press enter to start the clone process
- Navigate to the cloned repository

### Ubuntu
- Create the virtual environment `python3 -m venv .venv`
- Active the virtual environment for example ubuntu `source .venv/bin/activate`
- Install django in the virtual environment `pip3 install django`
- Run the application `python3 manage.py runserver`

### Windows
- Install the virtual environment `pip install virtualenv`
- Create the virtual environment `virtualenv .venv`
- Navigate into the created virtual environment directory `cd .venv/Scripts`
- Activate the virtual environment `activate`
- Install django in the virtual environment `pip install django`
- Run the application `python manage.py runserver`

## Contributing to the Project
- Checkout to the main branch of the repo `git checkout main`
- Pull the latest changes from the repo `git pull origin main`
- Checkout to a new branch `git checkout -b branch_name`
- Add changes in the working directory to the staging area `git add .`
- Commit changes `git commit -m "commit_message"`
- Push the branch upstream `git push --set-upstream origin branch_name`

## Linting
- [Flake8](https://pypi.org/project/flake8/)
  - Linting : `flake8`
- [Black](https://pypi.org/project/black/)
  - Usage: `black source_file_or_directory`

## Unit Tests
- [Coverage](https://coverage.readthedocs.io/en/7.2.7/)
  - Run the unit tests in the project `coverage run manage.py test`
  - Generate coverage report in the Terminal  `coverage report`
  - Generate HTML coverage report `coverage html`


