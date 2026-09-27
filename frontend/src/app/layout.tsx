import type { Metadata } from "next";
import Script from "next/script";

import { AuthProvider } from "@/components/auth-provider";

import "./globals.css";

export const metadata: Metadata = {
  title: "Bakery POS",
  description: "Bakery operations platform",
};

const removeScribeHydrationAttribute = `
  (() => {
    const attribute = "data-scribe-recorder-ready";
    const root = document.documentElement;
    const clean = () => root.removeAttribute(attribute);

    clean();
    const observer = new MutationObserver(clean);
    observer.observe(root, { attributes: true, attributeFilter: [attribute] });

    window.addEventListener(
      "load",
      () => {
        clean();
        requestAnimationFrame(() => observer.disconnect());
      },
      { once: true },
    );
  })();
`;

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <Script id="remove-scribe-hydration-attribute" strategy="beforeInteractive">
          {removeScribeHydrationAttribute}
        </Script>
      </head>
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}

