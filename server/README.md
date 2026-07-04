# DocuGen Server - FastAPI Backend

A production-ready FastAPI backend with Poetry, environment-based configuration, and best practices.

## Prerequisites

- Python 3.11+
- Poetry (for dependency management)

## Setup

### 1. Install Poetry

Follow the instructions at [Poetry's official website](https://python-poetry.org/docs/#installation) to install Poetry.

**Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

**Mac/Linux:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Activate the Virtual Environment

```bash
poetry shell
```

## Running the Server

To start the FastAPI server with the desired environment, use the following command:

```bash
poetry run python run.py --env <environment>
```

Replace `<environment>` with the appropriate environment name (`local`, `dev`, `prod`, etc.).

### Examples

**Local development:**
```bash
poetry run python run.py --env local
```

**Development environment:**
```bash
poetry run python run.py --env dev
```

**Production environment:**
```bash
poetry run python run.py --env prod
```

**Or use the startup scripts:**
```bash
# Windows
start_server.bat local

# Mac/Linux/Git Bash
./start_server.sh local
```

### Environment Configuration

Environment-specific configuration files are located in the `env` directory:

- `env/.env.local` - Local development
- `env/.env.dev` - Development server
- `env/.env.prod` - Production server

The application will load the appropriate configuration file based on the environment specified in the command.

## Available Commands

### Development

```bash
# Start server (local environment)
poetry run python run.py --env local

# Start server (development environment)
poetry run python run.py --env dev

# Or use startup script
./start_server.sh local  # Mac/Linux/Git Bash
start_server.bat local   # Windows
```

### Testing

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_api/test_example.py

# Run with verbose output
poetry run pytest -v
```

### Linting and Formatting

```bash
# Check code for linting issues
poetry run flake8 app/ tests/

# Format code
poetry run black app/ tests/

# Check formatting without applying
poetry run black --check app/ tests/
```

### Pre-Commit Hooks

To ensure code quality before committing changes, install pre-commit hooks:

```bash
# Install pre-commit hooks
poetry run pre-commit install

# Run hooks on all files
poetry run pre-commit run --all-files

# Update hooks to latest version
poetry run pre-commit autoupdate
```

### Database Migrations

```bash
# Create a new migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Rollback one migration
poetry run alembic downgrade -1

# View migration history
poetry run alembic history
```

## Project Structure

```
server/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── server.py            # Server entry point
│   ├── api/
│   │   ├── dependencies.py  # Common dependencies
│   │   └── v1/
│   │       ├── endpoints/   # API endpoints
│   │       └── router.py    # API router
│   ├── core/
│   │   ├── config.py        # Settings and configuration
│   │   └── security.py      # Security utilities
│   ├── db/
│   │   ├── base.py          # SQLAlchemy base
│   │   ├── session.py       # Database session
│   │   └── models/          # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── repositories/        # Data access layer
│   └── utils/               # Utility functions
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   └── api/                 # API tests
├── env/
│   ├── .env.local           # Local environment config
│   ├── .env.dev             # Dev environment config
│   └── .env.prod            # Prod environment config
├── alembic/                 # Database migrations
├── pyproject.toml           # Poetry configuration
├── .flake8                  # Flake8 configuration
├── .pre-commit-config.yaml  # Pre-commit hooks
└── README.md                # This file
```

## API Documentation

Once the server is running, access the interactive API documentation at:

- **Swagger UI:** http://localhost:8080/docs
- **ReDoc:** http://localhost:8080/redoc

## Environment Variables

Each environment file (`.env.local`, `.env.dev`, `.env.prod`) should contain:

```env
# Application
APP_NAME=DocuGen API
APP_VERSION=0.1.0
DEBUG=true
ENVIRONMENT=local

# Server
HOST=0.0.0.0
PORT=8080

# Database
DATABASE_URL=sqlite:///./docugen.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS_STR=http://localhost:5173,http://localhost:3000
```

## Running with Docker

### Build and run:

```bash
docker-compose build
docker-compose up
```

The server will be accessible at http://localhost:8080.

### Environment Configuration with Docker

Ensure the appropriate environment configuration files (`.env.local`, `.env.dev`, `.env.prod`) are available in the `env` directory.

## Development Workflow

### 1. Create a new feature

```bash
# Create a new branch
git checkout -b feature/my-new-feature

# Make changes to the code
# ...

# Run tests
poetry run pytest

# Format and lint
poetry run black app/ tests/
poetry run flake8 app/ tests/

# Commit changes (pre-commit hooks will run automatically)
git commit -m "Add new feature"
```

### 2. Adding a new endpoint

1. Create a new file in `app/api/v1/endpoints/`
2. Define your endpoint using FastAPI decorators
3. Add the router to `app/api/v1/router.py`
4. Create corresponding tests in `tests/api/`

### 3. Adding a new model

1. Create model in `app/db/models/`
2. Create Pydantic schema in `app/schemas/`
3. Create migration: `poetry run alembic revision --autogenerate -m "add new model"`
4. Apply migration: `poetry run alembic upgrade head`

## Troubleshooting

### Poetry not found

```bash
# Add Poetry to PATH (Windows)
# Add %APPDATA%\Python\Scripts to your PATH

# Add Poetry to PATH (Mac/Linux)
export PATH="$HOME/.local/bin:$PATH"
```

### Module not found errors

```bash
# Ensure you're in the poetry shell
poetry shell

# Or reinstall dependencies
poetry install
```

### Port already in use

```bash
# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8080 | xargs kill -9
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

## License

MIT
