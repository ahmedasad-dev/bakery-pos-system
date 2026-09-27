"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useAuth } from "@/components/auth-provider";
import { HealthStatus } from "@/components/health-status";

export default function DashboardPage() {
  const router = useRouter();
  const { logout, status, user } = useAuth();

  useEffect(() => {
    if (status === "anonymous") router.replace("/login");
  }, [router, status]);

  if (status !== "authenticated" || !user) {
    return (
      <main className="grid min-h-screen place-items-center">
        <p className="text-sm text-[var(--muted)]">Loading your workspace…</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen p-5 md:p-8">
      <header className="mx-auto flex max-w-6xl items-center justify-between rounded-2xl border border-[var(--border)] bg-white px-5 py-4 shadow-sm">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--brand)]">
            Bakery POS
          </p>
          <p className="mt-1 font-semibold">Platform foundation</p>
        </div>
        <button
          className="rounded-xl border border-[var(--border)] px-4 py-2 text-sm font-semibold hover:bg-stone-50"
          onClick={async () => {
            await logout();
            router.replace("/login");
          }}
          type="button"
        >
          Sign out
        </button>
      </header>

      <section className="mx-auto mt-6 grid max-w-6xl gap-5 md:grid-cols-[1.5fr_1fr]">
        <article className="rounded-3xl border border-[var(--border)] bg-white p-7 shadow-sm">
          <p className="text-sm text-[var(--muted)]">Signed in as</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">
            {user.full_name || user.email}
          </h1>
          <p className="mt-1 text-[var(--muted)]">{user.email}</p>

          <div className="mt-8">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-[var(--muted)]">
              Organizations
            </h2>
            <div className="mt-3 space-y-3">
              {user.memberships.length ? (
                user.memberships.map((membership) => (
                  <div
                    className="rounded-2xl border border-[var(--border)] bg-[var(--background)] p-4"
                    key={membership.id}
                  >
                    <p className="font-semibold">{membership.organization_name}</p>
                    <p className="mt-1 text-sm text-[var(--muted)]">
                      {membership.role_names.length
                        ? membership.role_names.join(", ")
                        : "No role assigned"}
                    </p>
                  </div>
                ))
              ) : (
                <p className="rounded-2xl bg-amber-50 p-4 text-sm text-amber-900">
                  Your account has no active organization membership.
                </p>
              )}
            </div>
          </div>
        </article>

        <aside className="space-y-5">
          <HealthStatus />
          <div className="rounded-3xl border border-[var(--border)] bg-white p-6 shadow-sm">
            <p className="text-sm font-semibold">Phase 1 scope</p>
            <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
              Identity, organization tenancy, location foundations, permissions, and system health are ready. POS features are intentionally not included yet.
            </p>
          </div>
        </aside>
      </section>
    </main>
  );
}

