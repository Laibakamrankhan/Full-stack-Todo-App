# Todo Console App

A feature-rich command-line interface (CLI) todo application built with Python, Typer, and Rich. The app provides an interactive menu system with persistent storage for managing your tasks efficiently.

## Features

- **Interactive Menu System**: Single command to start the app with a toggle menu for all operations
- **Task Management**: Add, list, update, delete, and toggle task completion status
- **Persistent Storage**: Tasks are saved to a JSON file for persistence between sessions
- **User-Friendly Interface**: Rich text formatting with color-coded status indicators
- **Flexible ID Matching**: Use either full task IDs or shortened versions (first 8 characters)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Laibakamrankhan/Evolution_of_Todo_Phase_1.git
   cd Evolution_of_Todo_Phase_1
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Usage

Start the interactive menu system:
```bash
todo run
```

The app provides the following options:
1. **Add Task**: Create a new task with a title and optional description
2. **List All Tasks**: Display all tasks in a formatted table
3. **Update Task**: Modify an existing task's title and description
4. **Delete Task**: Remove a task from your list
5. **Toggle Task Status**: Mark a task as completed or pending
6. **Exit**: Quit the application

## Command Line Interface

The app also supports direct command-line operations:

```bash
# Add a task
todo add "Task Title" "Optional Description"

# List all tasks
todo list

# Update a task
todo update <task-id> "New Title" "Optional New Description"

# Delete a task
todo delete <task-id>

# Toggle task status
todo toggle <task-id>
```

## Project Structure

```
todo_console_app/
├── main.py          # CLI entry point and interactive menu
├── common.py        # Shared service manager
├── models/          # Data models (Task, TaskStatus)
├── repositories/    # Data persistence (file and in-memory)
├── services/        # Business logic layer
└── ui/              # User interface components
```

## Contributing

This project was developed with the assistance of Claude AI for code implementation, bug fixes, and feature development.

## License

This project is open source and available under the MIT License.