import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskItem from '../components/TaskItem';

// Mock the API service
jest.mock('../services/api', () => ({
  updateTask: jest.fn(),
  deleteTask: jest.fn(),
  toggleTaskCompletion: jest.fn(),
}));

const mockTask = {
  id: '1',
  title: 'Test Task',
  description: 'Test Description',
  completed: false,
  user_id: 'user-1',
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
};

describe('TaskItem Component', () => {
  const mockOnUpdate = jest.fn();
  const mockOnDelete = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders task information correctly', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByRole('checkbox')).not.toBeChecked();
  });

  test('toggles completion status when checkbox is clicked', async () => {
    const { updateTask } = require('../services/api');
    updateTask.mockResolvedValue({ ...mockTask, completed: true });

    render(
      <TaskItem
        task={{ ...mockTask, completed: false }}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    await waitFor(() => {
      expect(updateTask).toHaveBeenCalledWith(mockTask.id, {
        title: mockTask.title,
        description: mockTask.description,
        completed: true,
      });
      expect(mockOnUpdate).toHaveBeenCalled();
    });
  });

  test('shows edit form when edit button is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    expect(screen.getByDisplayValue('Test Task')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Test Description')).toBeInTheDocument();
  });

  test('deletes task when delete button is clicked', async () => {
    const { deleteTask } = require('../services/api');
    deleteTask.mockResolvedValue({ message: 'Task deleted successfully' });

    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const deleteButton = screen.getByText('Delete');
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(deleteTask).toHaveBeenCalledWith(mockTask.id);
      expect(mockOnDelete).toHaveBeenCalledWith(mockTask.id);
    });
  });

  test('updates task when form is submitted', async () => {
    const { updateTask } = require('../services/api');
    updateTask.mockResolvedValue({ ...mockTask, title: 'Updated Task' });

    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    // Click edit to show form
    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    // Update the form fields
    const titleInput = screen.getByDisplayValue('Test Task');
    fireEvent.change(titleInput, { target: { value: 'Updated Task' } });

    const descriptionInput = screen.getByDisplayValue('Test Description');
    fireEvent.change(descriptionInput, { target: { value: 'Updated Description' } });

    // Submit the form
    const saveButton = screen.getByText('Save');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(updateTask).toHaveBeenCalledWith(mockTask.id, {
        title: 'Updated Task',
        description: 'Updated Description',
        completed: mockTask.completed,
      });
      expect(mockOnUpdate).toHaveBeenCalled();
    });
  });
});