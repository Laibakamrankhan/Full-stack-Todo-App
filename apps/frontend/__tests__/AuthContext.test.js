import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { AuthProvider } from '../contexts/auth';

// Mock the auth service
jest.mock('../services/auth', () => ({
  login: jest.fn(),
  logout: jest.fn(),
  register: jest.fn(),
  getCurrentUser: jest.fn(),
  getAuthToken: jest.fn(),
}));

// Mock router
jest.mock('next/router', () => ({
  useRouter: jest.fn(),
}));

// Simple component to test the context
const TestComponent = () => {
  const context = React.useContext(require('../contexts/auth').AuthContext);

  return (
    <div>
      <div data-testid="is-authenticated">{context.isAuthenticated ? 'true' : 'false'}</div>
      <div data-testid="user-email">{context.user?.email || 'none'}</div>
      <button
        onClick={() => context.login('test@example.com', 'password')}
        data-testid="login-btn"
      >
        Login
      </button>
      <button
        onClick={() => context.logout()}
        data-testid="logout-btn"
      >
        Logout
      </button>
      <button
        onClick={() => context.register('new@example.com', 'password', 'New User')}
        data-testid="register-btn"
      >
        Register
      </button>
    </div>
  );
};

describe('Auth Context', () => {
  const mockUser = {
    id: 'user-1',
    email: 'test@example.com',
    name: 'Test User',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('provides initial auth state', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('is-authenticated')).toHaveTextContent('false');
    expect(screen.getByTestId('user-email')).toHaveTextContent('none');
  });

  test('handles login successfully', async () => {
    const { login } = require('../services/auth');
    login.mockResolvedValue({
      user: mockUser,
      access_token: 'mock-token',
    });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    // Initially not authenticated
    expect(screen.getByTestId('is-authenticated')).toHaveTextContent('false');

    // Click login button
    fireEvent.click(screen.getByTestId('login-btn'));

    await waitFor(() => {
      expect(login).toHaveBeenCalledWith('test@example.com', 'password');
      expect(screen.getByTestId('is-authenticated')).toHaveTextContent('true');
      expect(screen.getByTestId('user-email')).toHaveTextContent('test@example.com');
    });
  });

  test('handles logout', async () => {
    const { logout, login } = require('../services/auth');
    login.mockResolvedValue({
      user: mockUser,
      access_token: 'mock-token',
    });
    logout.mockResolvedValue();

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    // First login
    fireEvent.click(screen.getByTestId('login-btn'));
    await waitFor(() => {
      expect(screen.getByTestId('is-authenticated')).toHaveTextContent('true');
    });

    // Then logout
    fireEvent.click(screen.getByTestId('logout-btn'));

    await waitFor(() => {
      expect(logout).toHaveBeenCalled();
      expect(screen.getByTestId('is-authenticated')).toHaveTextContent('false');
      expect(screen.getByTestId('user-email')).toHaveTextContent('none');
    });
  });

  test('handles registration', async () => {
    const { register } = require('../services/auth');
    register.mockResolvedValue({
      user: { ...mockUser, email: 'new@example.com', name: 'New User' },
      access_token: 'mock-token',
    });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    // Initially not authenticated
    expect(screen.getByTestId('is-authenticated')).toHaveTextContent('false');

    // Click register button
    fireEvent.click(screen.getByTestId('register-btn'));

    await waitFor(() => {
      expect(register).toHaveBeenCalledWith('new@example.com', 'password', 'New User');
      expect(screen.getByTestId('is-authenticated')).toHaveTextContent('true');
      expect(screen.getByTestId('user-email')).toHaveTextContent('new@example.com');
    });
  });
});