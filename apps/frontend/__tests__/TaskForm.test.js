import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskForm from '../components/TaskForm';

// Mock the API service
jest.mock('../services/api', () => ({
  createTask: jest.fn(),
}));

describe('TaskForm Component', () => {
  const mockOnTaskCreated = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders form fields correctly', () => {
    render(<TaskForm onTaskCreated={mockOnTaskCreated} />);

    expect(screen.getByPlaceholderText('Task title')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Task description')).toBeInTheDocument();
    expect(screen.getByText('Add Task')).toBeInTheDocument();
  });

  test('submits form with valid data', async () => {
    const { createTask } = require('../services/api');
    createTask.mockResolvedValue({
      id: '1',
      title: 'New Task',
      description: 'New Description',
      completed: false,
      user_id: 'user-1',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });

    render(<TaskForm onTaskCreated={mockOnTaskCreated} />);

    // Fill in the form
    const titleInput = screen.getByPlaceholderText('Task title');
    fireEvent.change(titleInput, { target: { value: 'New Task' } });

    const descriptionInput = screen.getByPlaceholderText('Task description');
    fireEvent.change(descriptionInput, { target: { value: 'New Description' } });

    // Submit the form
    const submitButton = screen.getByText('Add Task');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(createTask).toHaveBeenCalledWith({
        title: 'New Task',
        description: 'New Description',
        completed: false,
      });
      expect(mockOnTaskCreated).toHaveBeenCalled();
    });
  });

  test('shows error for empty title', async () => {
    render(<TaskForm onTaskCreated={mockOnTaskCreated} />);

    // Leave title empty and submit
    const descriptionInput = screen.getByPlaceholderText('Task description');
    fireEvent.change(descriptionInput, { target: { value: 'Description' } });

    const submitButton = screen.getByText('Add Task');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    });
  });

  test('shows error when API call fails', async () => {
    const { createTask } = require('../services/api');
    createTask.mockRejectedValue(new Error('Failed to create task'));

    render(<TaskForm onTaskCreated={mockOnTaskCreated} />);

    // Fill in the form
    const titleInput = screen.getByPlaceholderText('Task title');
    fireEvent.change(titleInput, { target: { value: 'New Task' } });

    const descriptionInput = screen.getByPlaceholderText('Task description');
    fireEvent.change(descriptionInput, { target: { value: 'New Description' } });

    const submitButton = screen.getByText('Add Task');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/failed to create task/i)).toBeInTheDocument();
    });
  });

  test('resets form after successful submission', async () => {
    const { createTask } = require('../services/api');
    createTask.mockResolvedValue({
      id: '1',
      title: 'New Task',
      description: 'New Description',
      completed: false,
      user_id: 'user-1',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });

    render(<TaskForm onTaskCreated={mockOnTaskCreated} />);

    // Fill in the form
    const titleInput = screen.getByPlaceholderText('Task title');
    fireEvent.change(titleInput, { target: { value: 'New Task' } });

    const descriptionInput = screen.getByPlaceholderText('Task description');
    fireEvent.change(descriptionInput, { target: { value: 'New Description' } });

    const submitButton = screen.getByText('Add Task');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(titleInput.value).toBe('');
      expect(descriptionInput.value).toBe('');
    });
  });
});