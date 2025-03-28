import axios, { AxiosError } from 'axios';
import { User, LoginResponse, RegisterResponse, AuthError } from '../types/auth';

const API_URL = 'http://localhost:5000/api';

class AuthService {
  private static instance: AuthService;
  private tokenRefreshTimeout?: NodeJS.Timeout;

  private constructor() {
    // Initialize axios interceptors
    axios.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config;
        if (error.response?.status === 401 && originalRequest && !originalRequest.headers['retry']) {
          originalRequest.headers['retry'] = true;
          try {
            const refreshToken = this.getRefreshToken();
            if (refreshToken) {
              const newTokens = await this.refreshToken(refreshToken);
              originalRequest.headers['Authorization'] = `Bearer ${newTokens.access_token}`;
              return axios(originalRequest);
            }
          } catch (refreshError) {
            this.logout();
            throw refreshError;
          }
        }
        throw error;
      }
    );
  }

  static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  private getRefreshToken(): string | null {
    const user = this.getCurrentUser();
    return user?.refresh_token || null;
  }

  private setupTokenRefresh(expiresIn: number): void {
    if (this.tokenRefreshTimeout) {
      clearTimeout(this.tokenRefreshTimeout);
    }
    // Refresh 1 minute before token expires
    this.tokenRefreshTimeout = setTimeout(async () => {
      const refreshToken = this.getRefreshToken();
      if (refreshToken) {
        try {
          await this.refreshToken(refreshToken);
        } catch (error) {
          this.logout();
        }
      }
    }, (expiresIn - 60) * 1000);
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      const response = await axios.post<LoginResponse>(`${API_URL}/auth/login`, {
        email,
        password,
      });
      const { access_token, refresh_token, user } = response.data;
      localStorage.setItem('user', JSON.stringify({ ...user, access_token, refresh_token }));
      this.setupTokenRefresh(3600); // Assuming 1-hour token expiry
      return response.data;
    } catch (error) {
      const authError: AuthError = {
        message: error instanceof Error ? error.message : 'An error occurred during login',
        status: (error as AxiosError)?.response?.status,
      };
      throw authError;
    }
  }

  async register(email: string, password: string): Promise<RegisterResponse> {
    try {
      const response = await axios.post<RegisterResponse>(`${API_URL}/auth/register`, {
        email,
        password,
      });
      return response.data;
    } catch (error) {
      const authError: AuthError = {
        message: error instanceof Error ? error.message : 'An error occurred during registration',
        status: (error as AxiosError)?.response?.status,
      };
      throw authError;
    }
  }

  async refreshToken(refresh_token: string): Promise<{ access_token: string }> {
    try {
      const response = await axios.post<{ access_token: string }>(`${API_URL}/auth/refresh`, {
        refresh_token,
      });
      const user = this.getCurrentUser();
      if (user && response.data.access_token) {
        user.access_token = response.data.access_token;
        localStorage.setItem('user', JSON.stringify(user));
        this.setupTokenRefresh(3600); // Reset refresh timer
      }
      return response.data;
    } catch (error) {
      const authError: AuthError = {
        message: error instanceof Error ? error.message : 'An error occurred while refreshing token',
        status: (error as AxiosError)?.response?.status,
      };
      throw authError;
    }
  }

  logout(): void {
    localStorage.removeItem('user');
    if (this.tokenRefreshTimeout) {
      clearTimeout(this.tokenRefreshTimeout);
    }
  }

  getCurrentUser(): User | null {
    try {
      const userStr = localStorage.getItem('user');
      return userStr ? JSON.parse(userStr) : null;
    } catch (error) {
      console.error('Error parsing user from localStorage:', error);
      return null;
    }
  }
}

export const authService = AuthService.getInstance();
