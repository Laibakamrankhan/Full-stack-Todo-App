# Quickstart Guide: Todo In-Memory Python Console App

## Prerequisites

- Python 3.13+
- uv package manager

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Run the application**:
   ```bash
   uv run python -m src.main
   ```

## Usage

### Add a new task
```bash
python -m src.main add "Buy groceries" "Need to buy milk and bread"
```

### List all tasks
```bash
python -m src.main list
```

### Update a task
```bash
python -m src.main update "task-uuid-here" "Updated title" "Updated description"
```

### Delete a task
```bash
python -m src.main delete "task-uuid-here"
```

### Toggle task completion
```bash
python -m src.main toggle "task-uuid-here"
```

## Development

### Run tests
```bash
uv run pytest
```

### Run tests with coverage
```bash
uv run pytest --cov=src
```

### Type checking
```bash
uv run mypy src/
```

### Format code
```bash
uv run black src/
uv run ruff check src/
```

## Project Structure

- `src/main.py` - CLI entry point
- `src/models/` - Data models (Task, TaskStatus)
- `src/repositories/` - Data access layer
- `src/services/` - Business logic
- `src/ui/` - Display formatting
- `tests/` - Test suite