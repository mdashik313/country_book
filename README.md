<h2> A simple country finding application using Django and PostgreSQL database. Features : find countries by name, view same regional countreis and languages, REST apis to fetch,create,update,delete countreis. </h2>

## Installation
Before starting you need Python installed on your system. [Python Installation guideline](https://packaging.python.org/en/latest/tutorials/installing-packages/)

1. Clone the repository

```
git clone "https://github.com/mdashik313/country_book.git"
```
2. Navigate to the project folder
```
cd country_book
```
3. Create virtual environment
```
python3 -m venv .venv
```
4. Activate virtual environment

For Windows:
```
.venv\Scripts\activate
```
For Linux:
```
source .venv/bin/activate
```
5. Install project dependencies
```
pip install -r requirements.txt
```
6. To migrate the database models. Run the following commands
```
python manage.py makemigrations
python manage.py migrate
```
## Required dependencies and versions
```
Django==5.1.8
djangorestframework==3.16.0
psycopg2-binary==2.9.10
python=3.10.12 or later
gunicorn==23.0.0
```

## Database setup and configuration

1. Create a PostgreSQL database at [Railway](https://railway.com/) or manually setup your prefered database.

2. Setup environment variables: create a '.env' file in the project directory and fill the below variables.
```
DB_NAME = <your_db_name>
DB_USER = <db_user_name>
DB_PASSWORD = <pasword>
DB_HOST = <host>
DB_PORT = <port>
```
## Running the application

1. python manage.py runserver
