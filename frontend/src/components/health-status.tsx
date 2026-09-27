"use client";

import { useEffect, useState } from "react";

import { apiRequest } from "@/lib/api";

type Health = { status: "ok" | "unhealthy"; database: string };

export function HealthStatus() {
  const [health, setHealth] = useState<Health | null>(null);

  useEffect(() => {
    apiRequest<Health>("/health/")
      .then(setHealth)
      .catch(() => setHealth({ status: "unhealthy", database: "unavailable" }));
  }, []);

  const healthy = health?.status === "ok";
  return (
    <div className="rounded-3xl border border-[var(--border)] bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold">System status</p>
        <span
          aria-label={health ? health.status : "checking"}
          className={`h-3 w-3 rounded-full ${
            health ? (healthy ? "bg-emerald-500" : "bg-red-500") : "animate-pulse bg-amber-400"
          }`}
        />
      </div>
      <p className="mt-3 text-2xl font-semibold">
        {health ? (healthy ? "Operational" : "Unavailable") : "Checking…"}
      </p>
      <p className="mt-1 text-sm text-[var(--muted)]">
        Database: {health?.database ?? "checking"}
      </p>
    </div>
  );
}

