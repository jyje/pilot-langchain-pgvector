# pgVector and LangChain Example Project

This project demonstrates how to store documents in a vector database and perform similarity searches using pgVector and LangChain.

## 🚀 Getting Started

### 1. Prerequisites

- Docker & Docker Compose
- [uv](https://docs.astral.sh/uv/) (recommended) or Python 3.8+ with pip
- Git

### 2. Infrastructure Setup

```bash
# Navigate to docker directory and start pgVector database
cd docker
docker-compose up -d

# Check database status
docker-compose ps

# Return to project root
cd ..
```

### 3. Python Environment Setup

#### Option A: Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and navigate to the project
git clone <your-repo-url>
cd pilot-langchain-pgvector

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
```

#### Option B: Using pip

```bash
# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 4. Run Example

⚠️ **Important**: Make sure Docker containers are running before executing the example!

```bash
# Check if containers are running
cd docker
docker-compose ps

# If containers are not running, start them
docker-compose up -d
cd ..
```

#### Using uv

```bash
# Run the example script directly
uv run vector-example

# Or run with Python
uv run python app/vector_example.py

# Run Jupyter Notebook
uv run jupyter notebook app/pgvector_example.ipynb

# Run Jupyter Lab
uv run jupyter lab app/pgvector_example.ipynb
```

#### Using pip

```bash
# Run vector storage and search example
python app/vector_example.py
```

## 📁 Project Structure

```
.
├── docker/
│   ├── docker-compose.yml # pgVector infrastructure setup
│   └── init.sql          # Database initialization script
├── pyproject.toml        # Project configuration and dependencies (uv)
├── requirements.txt      # Python dependencies (pip fallback)
├── uv.lock              # Dependency lock file (auto-generated)
├── app/
│   ├── vector_example.py # Main example script
│   └── config.py        # Configuration management
└── README.md
```

## 🔧 Components

### Docker Services

- **postgres**: PostgreSQL 16 with pgVector extension
- **adminer**: Web-based database management tool (http://localhost:18080)

### Database Information

- **Host**: localhost:15432
- **Database**: vectordb
- **User**: postgres
- **Password**: password

### Python Example Features

1. **Random Vector Embeddings**: Generate random vectors for testing without OpenAI API
2. **Document Storage**: Store LangChain Document objects in pgVector
3. **Similarity Search**: Search for documents similar to query text
4. **Metadata Filtering**: Filter search results by specific conditions
5. **Direct Vector Search**: Search directly using vector values

## 🛠 Usage

### Basic Vector Search

```python
from langchain_community.vectorstores import PGVector
from app.vector_example import RandomEmbeddings

# Initialize embedding model
embeddings = RandomEmbeddings(dimension=1536)

# Connect to vector store
vector_store = PGVector(
    connection_string="postgresql://postgres:password@localhost:15432/vectordb",
    embedding_function=embeddings,
    collection_name="documents"
)

# Perform similarity search
results = vector_store.similarity_search("text to search", k=3)
```

### Using OpenAI Embeddings (Optional)

To use actual OpenAI embeddings:

1. Set OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

2. Modify code:
```python
from langchain_community.embeddings import OpenAIEmbeddings

# Use OpenAI embeddings
embeddings = OpenAIEmbeddings()
```

## 📦 Package Management

### Using uv (Recommended)

```bash
# Add new dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Remove dependency
uv remove package-name

# Update dependencies
uv lock --upgrade

# Install specific version
uv add "package-name>=1.0.0,<2.0.0"

# Run commands in virtual environment
uv run python script.py
uv run pytest
```

### Development Tools

This project includes optional development dependencies:

```bash
# Install with development dependencies
uv sync --dev

# Run code formatting
uv run black .
uv run isort .

# Run linting
uv run flake8 .

# Run type checking
uv run mypy .

# Run tests
uv run pytest
```

## 🔍 Web Management Tool

You can manage the database through Adminer:

1. Access http://localhost:18080 in your browser
2. Login information:
   - System: PostgreSQL
   - Server: postgres
   - Username: postgres
   - Password: password
   - Database: vectordb

## 🧹 Cleanup

```bash
# Navigate to docker directory and stop containers
cd docker
docker-compose down

# Remove volumes as well (complete data deletion)
docker-compose down -v

# Return to project root
cd ..
```

## 🔧 Troubleshooting

### Connection Refused Error

If you get `connection to server at "localhost", port 15432 failed: Connection refused`:

```bash
# 1. Check if Docker containers are running
cd docker
docker-compose ps

# 2. If containers are not running, start them
docker-compose up -d

# 3. Wait a few seconds for the database to initialize
sleep 5

# 4. Check logs if there are issues
docker-compose logs postgres
docker-compose logs adminer

# 5. Try running the example again
cd ..
uv run vector-example
```

### LangChain Deprecation Warnings

The warnings about deprecated imports are normal and don't affect functionality. The code has been updated to use the new `langchain_community` imports.

### Port Conflicts

If ports 15432 or 18080 are already in use:

1. Edit `docker/docker-compose.yml`
2. Change the port mappings (e.g., `"16432:5432"` and `"19080:8080"`)
3. Update `app/config.py` and `app/vector_example.py` accordingly

## 📚 References

- [uv Documentation](https://docs.astral.sh/uv/)
- [pgVector Official Documentation](https://github.com/pgvector/pgvector)
- [LangChain Official Documentation](https://python.langchain.com/)
- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)

## 🤝 Contributing

Issues and pull requests are always welcome!
