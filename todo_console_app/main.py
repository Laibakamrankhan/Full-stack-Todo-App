"""Main CLI entry point for the Todo Console App."""

import typer
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from todo_console_app.repositories.memory import InMemoryTaskRepository
from todo_console_app.services.task_service import TaskService
from todo_console_app.ui.display import display_success_message, display_error_message, display_tasks_table, display_info_message
from typing import Optional

from todo_console_app.common import service_manager

# Create Typer app
app = typer.Typer()


def interactive_menu() -> None:
    """Interactive menu system for the todo app."""
    console = Console()
    service = service_manager.get_service()

    while True:
        console.clear()
        display_info_message("TODO CONSOLE APP", console)
        console.print("\n[bold]Select an option:[/bold]")
        console.print("1. Add Task")
        console.print("2. List All Tasks")
        console.print("3. Update Task")
        console.print("4. Delete Task")
        console.print("5. Toggle Task Status")
        console.print("6. Exit")

        try:
            choice = IntPrompt.ask("\n[bold blue]Enter your choice (1-6)[/bold blue]", choices=["1", "2", "3", "4", "5", "6"])

            if choice == 1:
                # Add Task
                title = Prompt.ask("[bold]Enter task title[/bold]")
                description = Prompt.ask("[bold]Enter task description (optional)[/bold]", default="")
                if description.strip() == "":
                    description = None

                try:
                    task = service.add_task(title, description)
                    display_success_message(f"Task added successfully with ID: {task.id[:8]}", console)
                except ValueError as e:
                    display_error_message(str(e), console)

            elif choice == 2:
                # List All Tasks
                tasks = service.list_tasks()
                display_tasks_table(tasks, console)

            elif choice == 3:
                # Update Task
                if not service.list_tasks():
                    display_info_message("No tasks available to update", console)
                else:
                    tasks = service.list_tasks()
                    display_tasks_table(tasks, console)
                    task_id = Prompt.ask("[bold]Enter task ID to update (use full ID or first 8 chars)[/bold]")
                    title = Prompt.ask("[bold]Enter new title[/bold]")
                    description = Prompt.ask("[bold]Enter new description (optional)[/bold]", default="")
                    if description.strip() == "":
                        description = None

                    try:
                        updated_task = service.update_task(task_id, title, description)
                        if updated_task:
                            display_success_message("Task updated successfully", console)
                        else:
                            # Try to match by short ID if full ID didn't work
                            matched_task = next((t for t in tasks if t.id.startswith(task_id)), None)
                            if matched_task:
                                # Try with the full ID
                                updated_task = service.update_task(matched_task.id, title, description)
                                if updated_task:
                                    display_success_message("Task updated successfully", console)
                                else:
                                    display_error_message(f"Error: Task with ID {task_id} not found", console)
                            else:
                                display_error_message(f"Error: Task with ID {task_id} not found", console)
                    except ValueError as e:
                        display_error_message(str(e), console)

            elif choice == 4:
                # Delete Task
                if not service.list_tasks():
                    display_info_message("No tasks available to delete", console)
                else:
                    tasks = service.list_tasks()
                    display_tasks_table(tasks, console)
                    task_id = Prompt.ask("[bold]Enter task ID to delete (use full ID or first 8 chars)[/bold]")

                    success = service.delete_task(task_id)
                    if success:
                        display_success_message("Task deleted successfully", console)
                    else:
                        # Try to match by short ID if full ID didn't work
                        matched_task = next((t for t in tasks if t.id.startswith(task_id)), None)
                        if matched_task:
                            success = service.delete_task(matched_task.id)
                            if success:
                                display_success_message("Task deleted successfully", console)
                            else:
                                display_error_message(f"Error: Task with ID {task_id} not found", console)
                        else:
                            display_error_message(f"Error: Task with ID {task_id} not found", console)

            elif choice == 5:
                # Toggle Task Status
                if not service.list_tasks():
                    display_info_message("No tasks available to toggle", console)
                else:
                    tasks = service.list_tasks()
                    display_tasks_table(tasks, console)
                    task_id = Prompt.ask("[bold]Enter task ID to toggle status (use full ID or first 8 chars)[/bold]")

                    toggled_task = service.toggle_task_status(task_id)
                    if toggled_task:
                        status = "completed" if toggled_task.status.value == "completed" else "pending"
                        display_success_message(f"Task status toggled successfully to {status}", console)
                    else:
                        # Try to match by short ID if full ID didn't work
                        matched_task = next((t for t in tasks if t.id.startswith(task_id)), None)
                        if matched_task:
                            toggled_task = service.toggle_task_status(matched_task.id)
                            if toggled_task:
                                status = "completed" if toggled_task.status.value == "completed" else "pending"
                                display_success_message(f"Task status toggled successfully to {status}", console)
                            else:
                                display_error_message(f"Error: Task with ID {task_id} not found", console)
                        else:
                            display_error_message(f"Error: Task with ID {task_id} not found", console)

            elif choice == 6:
                # Exit
                console.print("\n[bold green]Thank you for using Todo Console App![/bold green]")
                break

        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]Exiting...[/bold yellow]")
            break
        except Exception as e:
            display_error_message(f"An unexpected error occurred: {str(e)}", console)
            # Set choice to a default value to avoid the UnboundLocalError
            choice = None

        # Pause to let user see the result if choice was successfully obtained
        if choice is not None and choice != 6:
            Prompt.ask("\nPress Enter to continue")


@app.command()
def add(title: str, description: Optional[str] = typer.Argument(None, help="Optional description for the task")) -> None:
    """Add a new task with required title and optional description."""
    service = service_manager.get_service()
    console = Console()

    try:
        task = service.add_task(title, description)
        display_success_message(f"Task added successfully with ID: {task.id}", console)
    except ValueError as e:
        display_error_message(str(e), console)


@app.command()
def list() -> None:
    """List all tasks in rich table format."""
    from todo_console_app.ui.display import display_tasks_table

    service = service_manager.get_service()
    console = Console()

    tasks = service.list_tasks()
    display_tasks_table(tasks, console)


@app.command()
def update(
    task_id: str,
    title: str,
    description: Optional[str] = typer.Argument(None, help="Optional new description for the task")
) -> None:
    """Update an existing task by ID with new title and optional description."""
    service = service_manager.get_service()
    console = Console()

    try:
        updated_task = service.update_task(task_id, title, description)
        if updated_task:
            display_success_message("Task updated successfully", console)
        else:
            display_error_message(f"Error: Task with ID {task_id} not found", console)
    except ValueError as e:
        display_error_message(str(e), console)


@app.command()
def delete(task_id: str) -> None:
    """Delete a task by ID."""
    service = service_manager.get_service()
    console = Console()

    success = service.delete_task(task_id)
    if success:
        display_success_message("Task deleted successfully", console)
    else:
        display_error_message(f"Error: Task with ID {task_id} not found", console)


@app.command()
def toggle(task_id: str) -> None:
    """Toggle the completion status of a task by ID."""
    service = service_manager.get_service()
    console = Console()

    toggled_task = service.toggle_task_status(task_id)
    if toggled_task:
        status = "completed" if toggled_task.status.value == "completed" else "pending"
        display_success_message(f"Task status toggled successfully to {status}", console)
    else:
        display_error_message(f"Error: Task with ID {task_id} not found", console)


@app.command()
def run() -> None:
    """Start the interactive menu system for the todo app."""
    interactive_menu()


if __name__ == "__main__":
    app()