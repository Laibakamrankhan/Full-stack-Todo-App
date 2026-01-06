'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/router';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (email: string, password: string, name: string) => Promise<void>;
  checkAuthStatus: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Check auth status on initial load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setToken(token);
      try {
        // Decode token to get user info (in a real app, you'd validate the token)
        const tokenPayload = token.split('.')[1];
        // Add proper padding for base64 decoding
        let base64 = tokenPayload.replace(/-/g, '+').replace(/_/g, '/');
        // Add padding if needed
        while (base64.length % 4) {
          base64 += '=';
        }
        const decoded = JSON.parse(atob(base64));

        setUser({
          id: decoded.sub,
          email: decoded.email,
          name: decoded.name || decoded.sub,
        });
      } catch (error) {
        console.error('Error decoding token:', error);
        // Fallback to setting user as null
        setUser(null);
      }
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      // For FastAPI login endpoint, we need to send form data
      const formData = new FormData();
      formData.append('email', email);
      formData.append('password', password);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      const { access_token } = data;

      // Store token
      localStorage.setItem('token', access_token);
      setToken(access_token);

      // Decode token to get user info
      const tokenPayload = access_token.split('.')[1];
      // Add proper padding for base64 decoding
      let base64 = tokenPayload.replace(/-/g, '+').replace(/_/g, '/');
      // Add padding if needed
      while (base64.length % 4) {
        base64 += '=';
      }
      const decoded = JSON.parse(atob(base64));
      const userInfo = {
        id: decoded.sub,
        email: decoded.email,
        name: decoded.name || decoded.sub,
      };

      setUser(userInfo);
      router.push('/dashboard');
    } catch (error: any) {
      throw new Error(error.message || 'Login failed');
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          name,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      const userData = await response.json();

      // Automatically log in after registration
      await login(email, password);
    } catch (error: any) {
      throw new Error(error.message || 'Registration failed');
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    router.push('/login');
  };

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        // Verify token by making a simple request
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error('Token invalid');
        }

        // Decode token to get user info
        const tokenPayload = token.split('.')[1];
        // Add proper padding for base64 decoding
        let base64 = tokenPayload.replace(/-/g, '+').replace(/_/g, '/');
        // Add padding if needed
        while (base64.length % 4) {
          base64 += '=';
        }
        const decoded = JSON.parse(atob(base64));
        const userInfo = {
          id: decoded.sub,
          email: decoded.email,
          name: decoded.name || decoded.sub,
        };

        setUser(userInfo);
        setToken(token);
      } catch (error) {
        // Token is invalid, clear it
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
      }
    }
    setLoading(false);
  };

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    register,
    checkAuthStatus,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};