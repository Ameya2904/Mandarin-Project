/**
 * Authentication context — the app's single source of truth for "who is logged in".
 *
 * It keeps the persisted JWT (in secure storage) and the in-memory `user` in
 * lockstep: every entry point (login/signup/resetPassword) writes the token and
 * sets the user together. On mount it restores a session by reading the stored
 * token and calling /auth/me. The route guard in app/_layout.tsx reacts to the
 * `user` value to redirect between the auth screens and the main tabs.
 */
import React, { createContext, useContext, useEffect, useState } from 'react';
import { api, clearAuthToken, setAuthToken, UserPublic } from '@/src/api/client';
import { storage } from '@/src/utils/storage';

const TOKEN_KEY = 'mandarin_auth_token';

type AuthContextValue = {
  user: UserPublic | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name: string) => Promise<void>;
  resetPassword: (token: string, newPassword: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserPublic | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const token = await storage.secureGet<string>(TOKEN_KEY, '');
        if (token) {
          const me = await api.me();
          setUser(me);
        }
      } catch {
        await clearAuthToken();
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const login = async (email: string, password: string) => {
    const res = await api.login(email, password);
    await setAuthToken(res.access_token);
    setUser(res.user);
  };

  const signup = async (email: string, password: string, name: string) => {
    const res = await api.signup(email, password, name);
    await setAuthToken(res.access_token);
    setUser(res.user);
  };

  const resetPassword = async (token: string, newPassword: string) => {
    const res = await api.resetPassword(token, newPassword);
    await setAuthToken(res.access_token);
    setUser(res.user);
  };

  const logout = async () => {
    await clearAuthToken();
    setUser(null);
  };

  const refreshUser = async () => {
    try {
      const me = await api.me();
      setUser(me);
    } catch {
      // ignore
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, resetPassword, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
