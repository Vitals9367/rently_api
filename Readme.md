# Rently REST API
Django REST API created for rental property project

API hosted on render.com
URL - https://rently-api.onrender.com/

<br/>

### Local setup

Configure variables in ```.env``` file

Example:
```
DEBUG=True
SECRET_KEY=secret
JWT_SECRET_KEY=secret
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
APPLY_MIGRATIONS=True
```
To start development server run ```docker-compose up```

For production server run ```docker-compose run api``` or remove this comand from docker-compose.yml 
```
command: start_django_development_server
```

Production server uses UWSGI, it can be configured in ```uwsgi.ini``` file.

<br/>

### Tests

To run tests, run ```docker-compose run api "pytest"```

If you want to make tests run automatically after file edits, run ```docker-compose run api "ptw"```

Pytest configuration can be found in ```pytest.ini``` file.

<br/>

### Linting
For linting, flake8 is configured. Run ```docker-compose run api "flake8"``` to use it.

Flake configuration can be found in ```setup.cfg``` file.

<br/>

## CI/CD
Render.com uses **master** branch to host the API, it automatically redeployes it on push to branch.

There is ```.git/workflows/lint-and-test.yml``` GitHub workflow which runs on PR to master branch, it performs linting and testing, PR can be merged only if that check is passed.

## Endpoints
These are the API endpoints working at the moment.

### JWT auth

&nbsp;&nbsp;&nbsp;&nbsp;POST - ```/api/token``` - obtain JWT access and refresh tokens

&nbsp;&nbsp;&nbsp;&nbsp;POST - ```/api/token/refresh``` - refresh JWT token

&nbsp;&nbsp;&nbsp;&nbsp;POST - ```/api/token/blacklist``` - blacklist JWT refresh token

&nbsp;&nbsp;&nbsp;&nbsp;POST - ```/api/token/verify``` - verify JWT tokens

---

### Properties

&nbsp;&nbsp;&nbsp;&nbsp;GET - ```/api/v1/properties``` - get list of properties

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This endpoint has search functionality. You can search for properties using **owner, city, state and rooms** arguments.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example: ```/api/v1/properties?city=Vilnius```

&nbsp;&nbsp;&nbsp;&nbsp;POST - ```/api/v1/properties``` - create new property | **Requires JWT token**

&nbsp;&nbsp;&nbsp;&nbsp;GET - ```/api/v1/properties/<str: id>``` - get property details

&nbsp;&nbsp;&nbsp;&nbsp;PUT - ```/api/v1/properties/<str: id>``` - update property details fully | **Requires JWT token**

&nbsp;&nbsp;&nbsp;&nbsp;PATCH - ```/api/v1/properties/<str: id>``` - update property partialy | **Requires JWT token**

&nbsp;&nbsp;&nbsp;&nbsp;DELETE - ```/api/v1/properties/<str: id>``` - delete property | **Requires JWT token**