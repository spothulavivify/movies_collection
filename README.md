# Movie Collection API

A Django REST API that allows users to create and manage their movie collections by integrating with an external movie listing API. The application includes user authentication, collection management, and request monitoring features.

## Features

- User registration and JWT authentication
- Integration with external movie API with retry mechanism
- Create, read, update, and delete movie collections
- Add movies to collections
- View favorite genres based on collection contents
- Request counting middleware with reset capability
- Comprehensive test coverage


## Tech Stack

- Python 3.11
- Django 4.2.16
- Django REST Framework 3.15.2
- SQLite
- JWT Authentication

## Installation

### Method 1: Local Installation

1. Clone the repository:
```bash
git clone [Repo](https://github.com/spothulavivify/movies_collection)
cd movie_collection
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
DJANGO_SECRET_KEY=your_secret_key_here
MOVIE_API_USERNAME=iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0
MOVIE_API_PASSWORD=Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1
REDIS_URL=redis://localhost:6379/0
DEBUG=True
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```
