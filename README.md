# Edu Hub
Unified National Education Platform that integrates all Kenyan universities and higher education institutions. The core of this system would be a Single Student ID, a centralized identifier linked to a student’s records, courses, and academic history.
Edu Hub is a Django-based RESTful API project designed to manage various educational and career-related functionalities. The project is structured into multiple Django apps, each responsible for a specific domain such as academics, career guidance, exam registration, and user authentication.

## Goal
Develop a unified national education platform that not only simplifies and streamlines access to educational services across institutions but also integrates an AI-powered career guidance module. Such a system would leverage advanced data analytics and AI to provide students with tailored career advice based on their unique strengths, academic profiles, and aspirations. This would empower students to make informed decisions, maximize opportunities for scholarships and internships, and achieve their full potential in Kenya’s evolving job market

## Features

- **Academics**: Manage educational institutions, programs, courses, and units.
- **Career**: Provide career assessment and recommendation services.
- **Exam Registration**: Handle exam registration processes.
- **Users**: User registration, login, and JWT-based authentication.

## Technologies Used

- Django 4.x
- Django REST Framework
- Simple JWT for authentication
- drf-yasg for API documentation (Swagger/OpenAPI)
- PostgreSQL and MySQL database support
- OpenAI API integration
- python-decouple for environment variable management
- Whitenoise for static file serving

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd edu_hub
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   Create a `.env` file in the project root and add necessary environment variables such as database credentials, secret keys, and OpenAI API keys.

5. Set up the database:

   Apply migrations to create the database schema:

   ```bash
   python manage.py migrate
   ```

6. (Optional) Create a superuser for admin access:

   ```bash
   python manage.py createsuperuser
   ```

## Running the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will be accessible at `http://localhost:8000/`.

## API Endpoints Overview

### Academics

- `/institutions/` - Manage institutions
- `/programs/` - Manage programs
- `/courses/` - Manage courses
- `/units/` - Manage units

### Career

- `/assess/` - Career assessment endpoint
- `/recommendations/` - Career recommendations endpoint

### Exam Registration

- `/registrations/` - Manage exam registrations

### Users

- `/register/` - User registration
- `/login/` - Obtain JWT token
- `/refresh/` - Refresh JWT token

## Testing

Run tests for all apps using:

```bash
python manage.py test
```

## API Documentation

Swagger/OpenAPI documentation is available via drf-yasg integration. Access the docs at the configured URL (commonly `/swagger/` or `/docs/`).

## License

This project is licensed under the MIT License.

## Contact

For any inquiries or support, please contact the project maintainer.
