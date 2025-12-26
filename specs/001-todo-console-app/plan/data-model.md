# Data Model: Todo In-Memory Python Console App

## Task Entity

**Attributes**:
- `id: str` - Unique identifier (UUID string)
- `title: str` - Required task title (min length: 1 character)
- `description: Optional[str]` - Optional task description
- `status: TaskStatus` - Task status enum (pending or completed)
- `created_at: datetime` - Timestamp of creation
- `updated_at: datetime` - Timestamp of last update

**Validation Rules**:
- Title must not be empty (required field)
- ID must be a valid UUID format
- Status must be one of the allowed enum values

**State Transitions**:
- `pending` → `completed` (via toggle operation)
- `completed` → `pending` (via toggle operation)

## TaskStatus Enum

**Values**:
- `PENDING = "pending"` - Task is not yet completed
- `COMPLETED = "completed"` - Task has been completed

## Repository Interface

**Methods**:
- `add_task(task: Task) -> Task` - Add a new task to the repository
- `get_all_tasks() -> List[Task]` - Retrieve all tasks
- `get_task_by_id(task_id: str) -> Optional[Task]` - Retrieve task by ID
- `update_task(task_id: str, title: str, description: Optional[str]) -> Optional[Task]` - Update task details
- `delete_task(task_id: str) -> bool` - Delete task by ID
- `toggle_task_status(task_id: str) -> Optional[Task]` - Toggle task completion status

**Behavior**:
- All operations must be thread-safe for future multi-threading support
- Methods returning Optional will return None if the requested task doesn't exist
- Update and toggle operations return the updated Task object or None if not found
- Delete returns True if task was found and deleted, False otherwise