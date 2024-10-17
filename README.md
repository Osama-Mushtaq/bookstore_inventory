# Bookstore Inventory Management API

Welcome to the Bookstore Inventory Management API! This application is built using FastAPI and MongoDB to manage a bookstore's inventory, including books and user authentication.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Authentication Flow](#authentication-flow)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features
- User Registration and Authentication: Secure user registration and login using JWT tokens.
- Role-Based Access Control: Admin and regular user roles with appropriate permissions.
- Book Management: Create, read, update, and delete book records.
- Inventory Management: Manage stock quantities and pricing.
- Secure Password Hashing: Passwords are hashed using bcrypt for security.
- Interactive API Documentation: Automatically generated documentation with Swagger UI.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.8+: This application is developed using Python 3.8 or higher.
- MongoDB: A running instance of MongoDB is required.
- Git: For cloning the repository.
- Virtual Environment: Recommended to manage dependencies.

## Installation

1. Clone the Repository
   ```bash
   git clone https://github.com/your-username/bookstore-inventory.git
   cd bookstore-inventory
   ```

2. Create a Virtual Environment
   ```bash
   python -m venv .venv
   ```
   Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source .venv/bin/activate
     ```

3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables
Create a `.env` file in the root directory of the project to store environment variables:

```bash
touch .env
```

Add the following configurations to the `.env` file:

```dotenv
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=bookstore

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- `MONGODB_URI`: MongoDB connection string.
- `DATABASE_NAME`: Name of your MongoDB database.
- `SECRET_KEY`: A secret key for JWT token encoding. Replace with a secure, randomly generated string.
- `ALGORITHM`: Algorithm used for JWT tokens (default is HS256).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes.

## Running the Application
Ensure your MongoDB instance is running.

1. Start the Application
   ```bash
   uvicorn app.main:app --reload
   ```
   The `--reload` flag enables hot-reloading, which restarts the server when code changes are detected.

2. Access the Application
   Open your web browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

## API Documentation
Interactive API documentation is available via Swagger UI.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Authentication Flow

### Register a User
- Endpoint: `POST /users/register`
- Description: Register a new user.
- Request Body:
  ```json
  {
    "username": "adminuser",
    "email": "admin@example.com",
    "full_name": "Admin User",
    "password": "securepassword",
    "role": "admin"
  }
  ```

### Log In
- Endpoint: `POST /users/login`
- Description: Authenticate the user and obtain a JWT token.
- Form Data:
  - username: adminuser
  - password: securepassword
- Response:
  ```json
  {
    "access_token": "your_jwt_token_here",
    "token_type": "bearer"
  }
  ```

### Access Protected Endpoints
To access protected endpoints, include the JWT token in the Authorization header:
```
Authorization: Bearer your_jwt_token_here
```
Example: Accessing the `POST /books` endpoint to create a new book.

## Project Structure
```
bookstore-inventory/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── books.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   └── user.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── security.py
│   └── database/
│       ├── __init__.py
│       └── connection.py
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

- `app/main.py`: Entry point of the application.
- `app/routers/`: Contains route handlers for books and users.
- `app/schemas/`: Pydantic models for data validation.
- `app/core/`: Core utilities like security functions.
- `app/database/`: Database connection setup.

## Dependencies
Key dependencies used in this project:
- FastAPI: Web framework for building APIs.
- Uvicorn: ASGI server for running FastAPI.
- Pydantic: Data validation and settings management.
- Motor: Asynchronous MongoDB driver.
- Passlib: Password hashing library.
- Python-JOSE: JWT encoding and decoding.
- python-dotenv: Loads environment variables from a `.env` file.
- bcrypt: Password hashing algorithm.

Install all dependencies using:
```bash
pip install -r requirements.txt
```

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the Repository: Create a personal fork of the project.

2. Clone Your Fork:
   ```bash
   git clone https://github.com/your-username/bookstore-inventory.git
   ```

3. Create a Feature Branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. Commit Your Changes:
   ```bash
   git commit -m "Add your descriptive commit message"
   ```

5. Push to Your Fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request: Open a pull request to the main repository.

## License
This project is licensed under the MIT License.

## Additional Information

### Error Handling
- HTTP Exceptions: The application uses `fastapi.HTTPException` for error handling with appropriate status codes and messages.
- Validation Errors: Pydantic models ensure that data conforms to the required schema.

### Security Considerations
- Password Hashing: Passwords are hashed using bcrypt before storing in the database.
- JWT Tokens: Ensure the `SECRET_KEY` is kept secure and not exposed publicly.
- HTTPS: In a production environment, always use HTTPS to protect data in transit.

### Testing
While this guide doesn't include automated tests, it's recommended to implement unit and integration tests using frameworks like pytest.

### Contact
For questions or support, please contact:
- Email: your-email@example.com
- GitHub: your-username

Thank you for using the Bookstore Inventory Management API! We hope this application helps you manage your bookstore effectively.

Happy Coding! 🚀
