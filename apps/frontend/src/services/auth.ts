// JWT token storage and retrieval service

const TOKEN_KEY = 'token';

export const authService = {
  // Store JWT token
  storeToken: (token: string) => {
    localStorage.setItem(TOKEN_KEY, token);
  },

  // Get JWT token
  getToken: (): string | null => {
    return localStorage.getItem(TOKEN_KEY);
  },

  // Remove JWT token
  removeToken: () => {
    localStorage.removeItem(TOKEN_KEY);
  },

  // Decode JWT token (for getting user info)
  decodeToken: (token: string): any | null => {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );

      return JSON.parse(jsonPayload);
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  },

  // Check if token is expired
  isTokenExpired: (token: string): boolean => {
    try {
      const decoded = authService.decodeToken(token);
      if (!decoded || !decoded.exp) {
        return true;
      }

      const currentTime = Math.floor(Date.now() / 1000);
      return decoded.exp < currentTime;
    } catch (error) {
      console.error('Error checking token expiration:', error);
      return true;
    }
  },

  // Get current user info from token
  getCurrentUser: () => {
    const token = authService.getToken();
    if (!token || authService.isTokenExpired(token)) {
      return null;
    }

    return authService.decodeToken(token);
  },
};