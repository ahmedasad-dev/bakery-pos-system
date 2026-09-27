import { afterEach, describe, expect, it, vi } from "vitest";

import { apiRequest } from "./api";

describe("apiRequest", () => {
  afterEach(() => vi.restoreAllMocks());

  it("adds bearer authorization and includes cookies", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ id: "1" }), {
        status: 200,
        headers: { "content-type": "application/json" },
      }),
    );

    await apiRequest("/auth/me/", {}, "access-token");

    const [, options] = fetchMock.mock.calls[0];
    expect(options?.credentials).toBe("include");
    expect(new Headers(options?.headers).get("Authorization")).toBe("Bearer access-token");
  });

  it("throws a typed error for unsuccessful responses", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ detail: "Unauthorized" }), {
        status: 401,
        headers: { "content-type": "application/json" },
      }),
    );

    await expect(apiRequest("/auth/me/")).rejects.toEqual(expect.objectContaining({ status: 401 }));
  });
});

