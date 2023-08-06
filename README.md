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
- Create a file named `.env` in the root directory of the project (registrationapps)
- Paste in the details of the .env file provided.

### Ubuntu

- Create the virtual environment `python3 -m venv .venv`
- Active the virtual environment for example ubuntu `source .venv/bin/activate`
- Install requirements in the virtual environment `pip3 install -r requirements.txt`
- Run the application `python3 manage.py runserver`

### Windows

- Install the virtual environment `pip install virtualenv`
- Create the virtual environment `virtualenv .venv`
- Navigate into the created virtual environment directory `cd .venv/Scripts`
- Activate the virtual environment `activate`
- Install requirements in the virtual environment `pip install -r requirements.txt`
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
  - Generate coverage report in the Terminal `coverage report`
  - Generate HTML coverage report `coverage html`
## Additional Features Implemented
- Implemented additional model (Job) to store graduate job information
- Users can reset password 
- Implemented Django REST framework to create RESTful API
- Made use of Azure Functions to fetch Graduate Job Listings from an external API, store them in the database and also delete them daily
- Integrated with Google API to fetch list and details of books based on user search.
