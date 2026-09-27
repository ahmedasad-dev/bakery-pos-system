"use client";

import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from "react";

import { apiRequest, ApiError } from "@/lib/api";
import type { AuthResponse, User } from "@/lib/types";

type AuthStatus = "loading" | "authenticated" | "anonymous";

interface AuthContextValue {
  status: AuthStatus;
  user: User | null;
  accessToken: string | null;
  login(email: string, password: string): Promise<void>;
  logout(): Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

interface RestoredSession {
  access: string;
  user: User;
}

let sessionRestorePromise: Promise<RestoredSession | null> | null = null;

function restoreSessionOnce(): Promise<RestoredSession | null> {
  if (!sessionRestorePromise) {
    sessionRestorePromise = (async () => {
      await apiRequest<{ csrfToken: string }>("/auth/csrf/");
      const refresh = await apiRequest<{ access: string } | null>("/auth/refresh/", {
        method: "POST",
      });
      if (!refresh) return null;

      const user = await apiRequest<User>("/auth/me/", {}, refresh.access);
      return { access: refresh.access, user };
    })();
  }
  return sessionRestorePromise;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<AuthStatus>("loading");
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function restoreSession() {
      try {
        const restoredSession = await restoreSessionOnce();
        if (active) {
          if (restoredSession) {
            setAccessToken(restoredSession.access);
            setUser(restoredSession.user);
            setStatus("authenticated");
          } else {
            setStatus("anonymous");
          }
        }
      } catch {
        if (active) setStatus("anonymous");
      }
    }

    void restoreSession();
    return () => {
      active = false;
    };
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      status,
      user,
      accessToken,
      async login(email, password) {
        try {
          const response = await apiRequest<AuthResponse>("/auth/login/", {
            method: "POST",
            body: JSON.stringify({ email, password }),
          });
          setAccessToken(response.access);
          setUser(response.user);
          setStatus("authenticated");
        } catch (error) {
          if (error instanceof ApiError && error.status === 400) {
            throw new Error("The email or password is incorrect.");
          }
          throw new Error("Sign in is unavailable. Please try again.");
        }
      },
      async logout() {
        try {
          await apiRequest<void>("/auth/logout/", { method: "POST" });
        } finally {
          setAccessToken(null);
          setUser(null);
          setStatus("anonymous");
        }
      },
    }),
    [accessToken, status, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}

