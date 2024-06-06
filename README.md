# Job Hunter

Job Hunter is a Django-based project for job searching.
It provides functionality for managing users, job listings, applications, and more.

## Check it out

[Job Hunter deployed to Render](https://job-hunter-g5au.onrender.com/)

## Installed

Python must be already installed.

```shell
git clone https://github.com/SashaKisliy/job-hunter.git
cd job-hunter

python -m venv venv
source venv/bin/activate  # on macOS/Linux
venv\Scripts\activate  # on Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser to access the admin panel
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

## Features

* Registration and Authentication: Users can register and login.
* View Vacancies: Users can view a list of available job vacancies.
* View Resumes: Users can view resumes of candidates.
* Job Application: Registered users can apply for job vacancies.
* Favorites: Users can add job vacancies to their favorites list for later review.
* Admin Panel: Admins can manage users, vacancies, and applications through a powerful admin panel.

## Demo

![Wedsite Interface](demo.png)

## Test user for test my website:

* login: test_user1
* password: test123123



