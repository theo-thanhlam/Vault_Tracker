import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ApolloWrapper } from "@/components/providers/apollo";
import { SessionProvider } from "@/components/providers/session";
// import { AuthProvider } from "@/lib/contexts/auth-context";
import Navbar from "@/components/navigation/Navbar";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner"


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Vault Tracker",
  description: "Track your vaults and assets",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased dark min-h-screen flex flex-col`}
      >
        <SessionProvider>
          <ApolloWrapper>
            
              <Navbar />
              <main className="flex-1">
                {children}
              </main>
            
          </ApolloWrapper>
          <Toaster />
        </SessionProvider>
      </body>
    </html>
  );
}
