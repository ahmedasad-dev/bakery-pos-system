import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  skipTrailingSlashRedirect: true,
  async rewrites() {
    const backendUrl = process.env.BACKEND_INTERNAL_URL ?? "http://localhost:8000";
    return [
      {
        source: "/backend-api/:path*/",
        destination: `${backendUrl}/api/v1/:path*/`,
      },
      {
        source: "/backend-api/:path*",
        destination: `${backendUrl}/api/v1/:path*`,
      },
    ];
  },
};

export default nextConfig;

