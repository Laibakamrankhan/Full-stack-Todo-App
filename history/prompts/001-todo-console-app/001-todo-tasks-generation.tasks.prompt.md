---
id: 001
title: "Todo Tasks Generation"
stage: "tasks"
date_iso: "2025-12-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-console-app"
branch: "001-todo-console-app"
user: "user"
command: "/sp.tasks"
labels: ["tasks", "todo-app", "console", "python", "tdd"]
links:
  spec: "specs/001-todo-console-app/spec.md"
  plan: "specs/001-todo-console-app/plan/impl.md"
  tasks: "specs/001-todo-console-app/tasks.md"
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/001-todo-console-app/tasks.md
tests_yaml: |
  - "task breakdown completed"
  - "user stories mapped to tasks"
  - "tdd approach implemented"
prompt_text: |
  Generate atomic task breakdown for Todo In-Memory Python Console App following TDD approach.

  Context: 4 prioritized user stories (P1: Create & View Tasks, P2: Mark Complete, P3: Update Details, P3: Remove Tasks), multi-layer architecture (models → storage → services → ui), Repository Pattern, mypy --strict, pytest TDD.
response_text: |
  Successfully created atomic task breakdown for Todo In-Memory Python Console App.
  - Generated 68 tasks across 8 phases
  - Organized by user story priority (US1-US5)
  - Follows TDD approach with test tasks included
  - Multi-layer architecture tasks (models, storage, services, ui)
  - Repository pattern implementation tasks
  - Type safety (mypy) and testing (pytest) tasks
  - All tasks follow checklist format with proper IDs and story labels
outcome: "Task breakdown completed successfully with all required components. Ready for implementation phase."
evaluation: "SUCCESS - All task requirements met, TDD approach followed, user stories properly mapped."
---

# Tasks: Todo In-Memory Python Console App

**Feature**: Todo In-Memory Python Console App
**Branch**: 001-todo-console-app
**Generated**: 2025-12-20
**Status**: Ready for Implementation

## Implementation Strategy

This task breakdown follows a TDD approach with multi-layer architecture (models → storage → services → ui). Tasks are organized by user story priority to enable independent implementation and testing. The MVP scope includes User Story 1 (Add/List Tasks) which provides a complete, testable increment.

## Dependencies

User stories are designed to be independent, but share foundational components:
- Models must be implemented before services
- Services must be implemented before CLI/ui
- Repository pattern provides the data layer for all operations

### Parallel Execution Opportunities

Each user story can be developed in parallel after foundational components are complete:
- [US1] Add/List Tasks: Can be developed independently
- [US2] Toggle Completion: Can be developed independently
- [US3] Update Details: Can be developed independently
- [US4] Remove Tasks: Can be developed independently

---

## Phase 1: Setup

- [ ] T001 Create project structure per implementation plan in src/
- [ ] T002 Create tests directory structure per implementation plan
- [ ] T003 [P] Create pyproject.toml with dependencies (typer, rich, pytest, python-dotenv)
- [ ] T004 [P] Create .gitignore with Python patterns
- [ ] T005 [P] Create README.md with project overview
- [ ] T006 [P] Create .env and .env.example files
- [ ] T007 [P] Configure mypy with strict settings in pyproject.toml

---

## Phase 2: Foundational Components

- [ ] T008 [P] Create Task model in src/models/task.py with id, title, description, status, timestamps
- [ ] T009 [P] Create TaskStatus enum in src/models/enums.py with PENDING and COMPLETED values
- [ ] T010 [P] Create repository protocol interface in src/repositories/base.py
- [ ] T011 [P] Create in-memory repository implementation in src/repositories/memory.py
- [ ] T012 [P] Create task service in src/services/task_service.py with business logic
- [ ] T013 [P] Create display functions in src/ui/display.py for rich table formatting
- [ ] T014 [P] Create tests for Task model in tests/test_models/test_task.py
- [ ] T015 [P] Create tests for TaskStatus enum in tests/test_models/test_enums.py
- [ ] T016 [P] Create tests for repository interface in tests/test_repositories/test_base.py
- [ ] T017 [P] Create tests for in-memory repository in tests/test_repositories/test_memory_repository.py
- [ ] T018 [P] Create tests for task service in tests/test_services/test_task_service.py
- [ ] T019 [P] Create tests for display functions in tests/test_ui/test_display.py

---

## Phase 3: [US1] Add New Task

**Story Goal**: Enable users to add new tasks with required title and optional description

**Independent Test Criteria**: User can run the add command with a title and optionally a description, and verify the task appears in the task list

**Acceptance Scenarios**:
1. Given user is at console app prompt, When user enters "add 'Buy groceries'" command, Then a new task with title "Buy groceries" is added with unique ID and "pending" status
2. Given user is at console app prompt, When user enters "add 'Buy groceries' 'Need to buy milk'" command, Then a new task with title "Buy groceries" and description "Need to buy milk" is added with unique ID and "pending" status

- [ ] T020 [US1] Create CLI add command in src/main.py with title (required) and description (optional) parameters
- [ ] T021 [US1] Implement validation for empty titles in task service
- [ ] T022 [US1] Implement task creation with UUID generation in repository
- [ ] T023 [US1] Add success response "Task added successfully with ID: {task_id}" in CLI
- [ ] T024 [US1] Add error response "Error: Task title cannot be empty" for validation
- [ ] T025 [US1] Create unit tests for add command in tests/test_cli/test_add.py
- [ ] T026 [US1] Create integration tests for add functionality
- [ ] T027 [US1] Test that added tasks appear in the task list

---

## Phase 4: [US2] List All Tasks

**Story Goal**: Enable users to view all tasks in rich table format with ID, Title, Description, and Status

**Independent Test Criteria**: User can run the list command and see all tasks displayed in a rich table format with all relevant information

**Acceptance Scenarios**:
1. Given user has added multiple tasks, When user enters "list" command, Then all tasks are displayed in rich table format showing ID, Title, Description, and Status columns
2. Given user has no tasks, When user enters "list" command, Then appropriate message "No tasks found" is displayed

- [ ] T028 [US2] Create CLI list command in src/main.py
- [ ] T029 [US2] Implement get_all_tasks method in repository
- [ ] T030 [US2] Create rich table display function in src/ui/display.py
- [ ] T031 [US2] Format success response as rich table with ID, Title, Description, Status columns
- [ ] T032 [US2] Add "No tasks found" message when no tasks exist
- [ ] T033 [US2] Create unit tests for list command in tests/test_cli/test_list.py
- [ ] T034 [US2] Create integration tests for list functionality
- [ ] T035 [US2] Test rich table formatting with multiple tasks

---

## Phase 5: [US3] Update Task Details

**Story Goal**: Enable users to modify the title or description of existing tasks by ID

**Independent Test Criteria**: User can run the update command with a task ID and new details, and verify the changes are reflected when the task is listed

**Acceptance Scenarios**:
1. Given user has a task with ID 1, When user enters "update 1 'Updated title' 'Updated description'" command, Then the task with ID 1 has its title and description updated
2. Given user attempts to update a non-existent task, When user enters "update 999 'New title'" command, Then appropriate error message "Error: Task with ID 999 not found" is displayed

- [ ] T036 [US3] Create CLI update command in src/main.py with id, title, and optional description parameters
- [ ] T037 [US3] Implement get_task_by_id validation in repository
- [ ] T038 [US3] Implement update_task method in repository
- [ ] T039 [US3] Add success response "Task updated successfully" in CLI
- [ ] T040 [US3] Add error response "Error: Task with ID {id} not found" for invalid ID
- [ ] T041 [US3] Add error response "Error: Task title cannot be empty" for validation
- [ ] T042 [US3] Create unit tests for update command in tests/test_cli/test_update.py
- [ ] T043 [US3] Create integration tests for update functionality

---

## Phase 6: [US4] Delete Task

**Story Goal**: Enable users to remove tasks from their list by ID

**Independent Test Criteria**: User can run the delete command with a task ID and verify the task no longer appears when the list is displayed

**Acceptance Scenarios**:
1. Given user has a task with ID 1, When user enters "delete 1" command, Then the task with ID 1 is removed from the list
2. Given user attempts to delete a non-existent task, When user enters "delete 999" command, Then appropriate error message "Error: Task with ID 999 not found" is displayed

- [ ] T044 [US4] Create CLI delete command in src/main.py with id parameter
- [ ] T045 [US4] Implement delete_task method in repository
- [ ] T046 [US4] Add success response "Task deleted successfully" in CLI
- [ ] T047 [US4] Add error response "Error: Task with ID {id} not found" for invalid ID
- [ ] T048 [US4] Create unit tests for delete command in tests/test_cli/test_delete.py
- [ ] T049 [US4] Create integration tests for delete functionality

---

## Phase 7: [US5] Toggle Task Completion

**Story Goal**: Enable users to mark tasks as completed or mark them as pending again by ID

**Independent Test Criteria**: User can run the toggle command with a task ID and verify the status change is reflected when the task is listed

**Acceptance Scenarios**:
1. Given user has a task with ID 1 and status "pending", When user enters "toggle 1" command, Then the task with ID 1 has its status changed to "completed"
2. Given user has a task with ID 1 and status "completed", When user enters "toggle 1" command, Then the task with ID 1 has its status changed to "pending"
3. Given user attempts to toggle a non-existent task, When user enters "toggle 999" command, Then appropriate error message "Error: Task with ID 999 not found" is displayed

- [ ] T050 [US5] Create CLI toggle command in src/main.py with id parameter
- [ ] T051 [US5] Implement toggle_task_status method in repository
- [ ] T052 [US5] Add success response "Task status toggled successfully" in CLI
- [ ] T053 [US5] Add error response "Error: Task with ID {id} not found" for invalid ID
- [ ] T054 [US5] Create unit tests for toggle command in tests/test_cli/test_toggle.py
- [ ] T055 [US5] Create integration tests for toggle functionality

---

## Phase 8: Polish & Cross-Cutting Concerns

- [ ] T056 [P] Add comprehensive error handling throughout the application
- [ ] T057 [P] Implement input validation for all commands
- [ ] T058 [P] Add type checking with mypy to all modules
- [ ] T059 [P] Create comprehensive test suite with pytest
- [ ] T060 [P] Add test coverage requirements (80%+ coverage)
- [ ] T061 [P] Add documentation strings to all public functions
- [ ] T062 [P] Implement proper logging for debugging
- [ ] T063 [P] Add command help text and usage examples
- [ ] T064 [P] Run full test suite and ensure all tests pass
- [ ] T065 [P] Run mypy type checking and ensure no errors
- [ ] T066 [P] Test all user scenarios end-to-end
- [ ] T067 [P] Update README.md with usage instructions
- [ ] T068 [P] Add quickstart guide to README.md