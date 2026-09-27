"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { useAuth } from "@/components/auth-provider";

export default function LoginPage() {
  const router = useRouter();
  const { login, status } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (status === "authenticated") router.replace("/dashboard");
  }, [router, status]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login(email, password);
      router.replace("/dashboard");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to sign in.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="grid min-h-screen place-items-center px-5 py-10">
      <section className="w-full max-w-md rounded-3xl border border-[var(--border)] bg-white p-8 shadow-[0_24px_70px_rgba(60,40,25,0.10)]">
        <div className="mb-8">
          <p className="mb-2 text-sm font-semibold uppercase tracking-[0.18em] text-[var(--brand)]">
            Bakery POS
          </p>
          <h1 className="text-3xl font-semibold tracking-tight">Welcome back</h1>
          <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
            Sign in with your staff account to continue.
          </p>
        </div>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <label className="block text-sm font-medium">
            Email
            <input
              autoComplete="email"
              className="mt-2 w-full rounded-xl border border-[var(--border)] bg-white px-4 py-3 outline-none transition focus:border-[var(--brand)]"
              onChange={(event) => setEmail(event.target.value)}
              required
              type="email"
              value={email}
            />
          </label>
          <label className="block text-sm font-medium">
            Password
            <input
              autoComplete="current-password"
              className="mt-2 w-full rounded-xl border border-[var(--border)] bg-white px-4 py-3 outline-none transition focus:border-[var(--brand)]"
              minLength={8}
              onChange={(event) => setPassword(event.target.value)}
              required
              type="password"
              value={password}
            />
          </label>

          {error ? (
            <p aria-live="polite" className="rounded-xl bg-red-50 px-4 py-3 text-sm text-[var(--danger)]">
              {error}
            </p>
          ) : null}

          <button
            className="w-full rounded-xl bg-[var(--brand)] px-4 py-3 font-semibold text-white transition hover:bg-[var(--brand-dark)] disabled:cursor-not-allowed disabled:opacity-60"
            disabled={submitting}
            type="submit"
          >
            {submitting ? "Signing in…" : "Sign in"}
          </button>
        </form>
      </section>
    </main>
  );
}

