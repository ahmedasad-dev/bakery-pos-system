import { StrictMode } from "react";
import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { AuthProvider, useAuth } from "./auth-provider";

function AuthStatus() {
  const { status } = useAuth();
  return <span>{status}</span>;
}

describe("AuthProvider", () => {
  afterEach(() => vi.restoreAllMocks());

  it("restores an anonymous session only once during Strict Mode effect replay", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockImplementation(async (input) => {
      const url = String(input);
      if (url.endsWith("/auth/csrf/")) {
        return new Response(JSON.stringify({ csrfToken: "token" }), {
          status: 200,
          headers: { "content-type": "application/json" },
        });
      }
      if (url.endsWith("/auth/refresh/")) return new Response(null, { status: 204 });
      throw new Error(`Unexpected request: ${url}`);
    });

    render(
      <StrictMode>
        <AuthProvider>
          <AuthStatus />
        </AuthProvider>
      </StrictMode>,
    );

    await screen.findByText("anonymous");
    await waitFor(() => {
      const refreshCalls = fetchMock.mock.calls.filter(([input]) =>
        String(input).endsWith("/auth/refresh/"),
      );
      expect(refreshCalls).toHaveLength(1);
    });
  });
});
