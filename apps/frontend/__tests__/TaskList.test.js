import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskList from '../components/TaskList';

// Mock the API service
jest.mock('../services/api', () => ({
  getTasks: jest.fn(),
}));

// Mock the TaskItem component
jest.mock('../components/TaskItem', () => {
  return ({ task, onUpdate, onDelete }) => (
    <div data-testid="task-item" data-task-id={task.id}>
      {task.title} - {task.description}
      <button onClick={() => onUpdate(task)}>Update</button>
      <button onClick={() => onDelete(task.id)}>Delete</button>
    </div>
  );
});

describe('TaskList Component', () => {
  const mockTasks = [
    {
      id: '1',
      title: 'Task 1',
      description: 'Description 1',
      completed: false,
      user_id: 'user-1',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      id: '2',
      title: 'Task 2',
      description: 'Description 2',
      completed: true,
      user_id: 'user-1',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders loading state initially', async () => {
    const { getTasks } = require('../services/api');
    getTasks.mockImplementation(() => new Promise(() => {})); // Never resolves to test loading state

    render(<TaskList userId="user-1" />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test('renders tasks when data is loaded', async () => {
    const { getTasks } = require('../services/api');
    getTasks.mockResolvedValue(mockTasks);

    render(<TaskList userId="user-1" />);

    await waitFor(() => {
      expect(getTasks).toHaveBeenCalledWith();
      expect(screen.getByText('Task 1 - Description 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2 - Description 2')).toBeInTheDocument();
    });
  });

  test('filters tasks based on completion status', async () => {
    const { getTasks } = require('../services/api');
    getTasks.mockResolvedValue(mockTasks);

    render(<TaskList userId="user-1" showCompleted={false} />);

    await waitFor(() => {
      expect(getTasks).toHaveBeenCalledWith();
      // Should only show incomplete tasks when showCompleted is false
      expect(screen.getByText('Task 1 - Description 1')).toBeInTheDocument();
    });
  });

  test('shows empty state when no tasks exist', async () => {
    const { getTasks } = require('../services/api');
    getTasks.mockResolvedValue([]);

    render(<TaskList userId="user-1" />);

    await waitFor(() => {
      expect(getTasks).toHaveBeenCalledWith();
      expect(screen.getByText(/no tasks found/i)).toBeInTheDocument();
    });
  });

  test('refreshes tasks when refresh prop changes', async () => {
    const { getTasks } = require('../services/api');
    getTasks.mockResolvedValue(mockTasks);

    const { rerender } = render(<TaskList userId="user-1" refresh={false} />);

    // Initially should not call getTasks since refresh is false
    expect(getTasks).not.toHaveBeenCalled();

    // Update the refresh prop to true
    rerender(<TaskList userId="user-1" refresh={true} />);

    await waitFor(() => {
      expect(getTasks).toHaveBeenCalledWith();
    });
  });
});