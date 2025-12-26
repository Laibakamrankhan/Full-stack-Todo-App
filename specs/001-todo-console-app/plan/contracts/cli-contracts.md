# CLI Contracts: Todo In-Memory Python Console App

## Command Interface Specification

### Add Command
**Signature**: `add <title> [description]`

**Parameters**:
- `title` (required): String, task title (min 1 character)
- `description` (optional): String, task description

**Behavior**:
- Creates a new task with provided title and description
- Assigns a unique UUID to the task
- Sets status to "pending"
- Sets creation and update timestamps
- Returns success message with task ID

**Success Response**:
```
Task added successfully with ID: {task_id}
```

**Error Responses**:
- Empty title: `Error: Task title cannot be empty`
- Invalid input: `Error: Invalid command format`

### List Command
**Signature**: `list`

**Parameters**: None

**Behavior**:
- Retrieves all tasks from repository
- Displays tasks in rich table format
- Shows ID, Title, Description, and Status columns

**Success Response**:
```
┌─────┬─────────────────┬────────────────────────┬──────────┐
│ ID  │ Title           │ Description            │ Status   │
├─────┼─────────────────┼────────────────────────┼──────────┤
│ 1   │ Buy groceries   │ Need to buy milk       │ pending  │
│ 2   │ Walk the dog    │ Daily exercise         │ completed│
└─────┴─────────────────┴────────────────────────┴──────────┘
```

**Error Responses**:
- No tasks: `No tasks found`

### Update Command
**Signature**: `update <id> <title> [description]`

**Parameters**:
- `id` (required): String, valid task UUID
- `title` (required): String, new task title (min 1 character)
- `description` (optional): String, new task description

**Behavior**:
- Updates existing task with new title and description
- Updates the `updated_at` timestamp
- Returns success message

**Success Response**:
```
Task updated successfully
```

**Error Responses**:
- Invalid ID: `Error: Task with ID {id} not found`
- Empty title: `Error: Task title cannot be empty`

### Delete Command
**Signature**: `delete <id>`

**Parameters**:
- `id` (required): String, valid task UUID

**Behavior**:
- Removes task from repository
- Returns success message

**Success Response**:
```
Task deleted successfully
```

**Error Responses**:
- Invalid ID: `Error: Task with ID {id} not found`

### Toggle Command
**Signature**: `toggle <id>`

**Parameters**:
- `id` (required): String, valid task UUID

**Behavior**:
- Switches task status between "pending" and "completed"
- Updates the `updated_at` timestamp
- Returns success message

**Success Response**:
```
Task status toggled successfully
```

**Error Responses**:
- Invalid ID: `Error: Task with ID {id} not found`