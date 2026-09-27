"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useAuth } from "@/components/auth-provider";

export default function HomePage() {
  const router = useRouter();
  const { status } = useAuth();

  useEffect(() => {
    if (status === "authenticated") router.replace("/dashboard");
    if (status === "anonymous") router.replace("/login");
  }, [router, status]);

  return (
    <main className="grid min-h-screen place-items-center">
      <p className="text-sm text-[var(--muted)]">Loading Bakery POS…</p>
    </main>
  );
}

