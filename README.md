# DocuGen

A full-stack application with React + TypeScript frontend and Python FastAPI backend.

## Project Structure

```
DocuGen/
├── client/                 # React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── api/           # API integration layer
│   │   ├── components/    # React components
│   │   ├── features/      # Feature-based modules
│   │   ├── hooks/         # Custom React hooks
│   │   ├── pages/         # Page components
│   │   ├── services/      # Business logic
│   │   ├── styles/        # Global styles
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utility functions
│   └── public/            # Static assets
│
└── server/                # Python FastAPI backend
    ├── app/
    │   ├── api/           # API routes
    │   ├── core/          # Core configuration
    │   ├── db/            # Database layer
    │   ├── schemas/       # Pydantic schemas
    │   ├── services/      # Business logic
    │   ├── repositories/  # Data access layer
    │   └── utils/         # Utility functions
    └── tests/             # Test files
```

## Tech Stack

### Frontend
- **React 18+** - UI library
- **TypeScript 5+** - Type safety
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **React Router** - Routing

### Backend
- **Python 3.11+** - Programming language
- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Uvicorn** - ASGI server

## Prerequisites

### Client
- Node.js 18+ and npm 9+

### Server
- Python 3.11+
- Poetry (for dependency management)

## Getting Started

### Client Setup

1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

### Server Setup

1. Navigate to the server directory:
   ```bash
   cd server
   ```

2. Install Poetry:
   
   Follow the instructions at [Poetry's official website](https://python-poetry.org/docs/#installation)
   
   **Windows (PowerShell):**
   ```powershell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```
   
   **Mac/Linux:**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Activate the virtual environment:
   ```bash
   poetry shell
   ```

5. Start development server:
   ```bash
   poetry run python run.py --env local
   ```
   
   Or for other environments:
   ```bash
   poetry run python run.py --env dev    # Development
   poetry run python run.py --env prod   # Production
   ```
   
   Or use the startup scripts:
   ```bash
   ./start_server.sh local    # Mac/Linux/Git Bash
   start_server.bat local     # Windows
   ```

   The API will be available at `http://localhost:8080`
   
   API documentation: `http://localhost:8080/docs`

## Available Scripts

### Client

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Server

- `poetry run python run.py --env local` - Start development server (local)
- `poetry run python run.py --env dev` - Start development server (dev)
- `./start_server.sh local` - Start using script (Mac/Linux/Git Bash)
- `poetry run pytest` - Run tests
- `poetry run pytest --cov=app` - Run tests with coverage
- `poetry run black app/ tests/` - Format code
- `poetry run flake8 app/ tests/` - Lint code
- `poetry run alembic revision --autogenerate -m "message"` - Create migration
- `poetry run alembic upgrade head` - Apply migrations

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Swagger UI documentation
- `GET /api/v1/example` - Example endpoint

## Environment Variables

### Client (.env)
```
VITE_API_BASE_URL=http://localhost:8080
VITE_APP_NAME=DocuGen
```

### Server (env/.env.local, env/.env.dev, env/.env.prod)
```
APP_NAME=DocuGen API
DEBUG=true
DATABASE_URL=sqlite:///./docugen.db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS_STR=http://localhost:5173,http://localhost:3000
```

**Note:** Server uses environment-specific config files in the `env/` directory.

## Architecture

### Frontend Architecture
- **Feature-based structure** - Organized by business domains
- **Colocation principle** - Related files stay together
- **Path aliases** - Clean imports with `@/` prefix
- **API layer separation** - Centralized HTTP client configuration

### Backend Architecture
- **Layered architecture** - Clear separation of concerns
- **Routers** - HTTP endpoint handlers
- **Services** - Business logic layer
- **Repositories** - Data access layer
- **Schemas** - Request/response validation

## Development Guidelines

1. **Type Safety** - Use TypeScript types and Python type hints
2. **Code Quality** - Follow ESLint and Black formatting rules
3. **Testing** - Write tests for critical functionality
4. **API Design** - Follow RESTful conventions
5. **Security** - Never commit `.env` files

## License

MIT