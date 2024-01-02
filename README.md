# User Management API

## Description
This is a simple Flask application which provides a collection of REST APIs for a user management.
Each user has a username, first name, last name, and email address. 
The application validates emails based on [RFC standards](https://pypi.org/project/email-validator/) and checks that usernames are alphanumeric and unique username. 

## Dependencies
- Flask
- Flask-SQLAlchemy
- email-validator

## Setup and Installation
1. Ensure that Python 3.8 (or later) is installed on your system.
2. Clone the repository to your local system.
3. Navigate into the project directory and create a virtual environment by running `python3 -m venv venv`.
4. Activate the virtual environment. On Unix or MacOS, use `source venv/bin/activate`; On Windows, use `venv\Scripts\activate`.
5. Install the required dependencies by running `pip3 install -r requirements.txt`.
6. Run the Flask application with the command `python3 app.py`.

Note: The application is configured to use a SQLite database. If you wish to use a different database, you can change the `SQLALCHEMY_DATABASE_URI` variable in app.py.

### Example Usage with a clean venv
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

## API Usage

### Create a new user

Endpoint: `POST /users`

Request body should be a JSON object with the keys `username`, `first_name`, `last_name`, and `email`.

Example:

```bash
curl --location '127.0.0.1:5000/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"userA",
    "first_name": "Afirstname",
    "last_name": "Alastname",
    "email":"userA@example.com"
}'
```
### Get a user
Endpoint: `GET /users/<username>` where `<username>` is the username of the user you want to get.

Example:

```bash
curl --location '127.0.0.1:5000/users/userA' 
```

### Get all users
Endpoint: `GET /users`

You can add a `sort_by` query parameter to sort the users by a specific field. The default is `username`.

Example:

```bash
curl --location --request GET '127.0.0.1:5000/users?sort_by=first_name' \
--header 'Content-Type: application/json'
```

### Update an existing user
Endpoint: `PUT /users/<username>` where `<username>` is the username of the user you want to update.

Request body should be a JSON object with any of the keys `first_name`, `last_name`, and `email` that you want to update.

Example:

```bash
curl --location --request PUT '127.0.0.1:5000/users/userA' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"userA",
    "first_name": "new_firstname",
    "email": "new_userA@example.com"
}'
```

## Responses

All endpoints return a JSON response. In case of successful operations, you can expect the following responses:

- `POST /users`: A successful operation will return a JSON object with a `message` key stating "New user created" and a `user` key containing the data of the newly created user.

- `GET /users/<username>`: A successful operation will return a JSON object with a `user` key containing the data of the requested user.

- `GET /users`: A successful operation will return a JSON object with a `users` key containing a list of all users in the database.

- `PUT /users/<username>`: A successful operation will return a JSON object with a `message` key stating "User updated" and a `user` key containing the updated username.

In case of an error, the response will have a `message` key with a description of the error. 
For example, if you attempt to create a user with a username that already exists, the response will be a JSON object with the `message: "Username already exists"`. 
Similarly, if the required data is missing in the request, the response will have the `message: "Missing data"`.

## Testing
To run the unit tests and genrate a coverage report, use the following command in venv:
```bash
coverage run -m pytest test_app.py . && coverage report -m
```


