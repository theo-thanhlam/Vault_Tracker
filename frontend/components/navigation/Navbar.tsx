"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useQuery, useMutation } from "@apollo/client";
import { GET_CURRENT_USER } from "@/lib/graphql/authentication/queries";
import { LOGOUT_MUTATION } from "@/lib/graphql/authentication/mutations";
import { toast } from "sonner";
import { useState, useEffect } from "react";
import { signOut as nextAuthSignOut } from "next-auth/react";

export default function Navbar() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authStatus, setAuthStatus] = useState<'authenticated' | 'unauthenticated' | 'loading'>('loading');

  // Check auth status from middleware
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const response = await fetch(window.location.pathname);
        const status = response.headers.get('x-auth-status');
        
        setAuthStatus(status === 'authenticated' ? 'authenticated' : 'unauthenticated');
      } catch (error) {
        
        setAuthStatus('unauthenticated');
      }
    };
    
    checkAuthStatus();
  }, [authStatus]);

  // Only query for user data if middleware confirms authentication
  const { data: userData, loading: userLoading } = useQuery(GET_CURRENT_USER, {
    skip: authStatus !== 'authenticated',
    onCompleted: (data) => {
      setIsAuthenticated(true);
    },
    onError: (error) => {
      setIsAuthenticated(false);
    },
  });

  // Logout mutation
  const [logout, { loading: logoutLoading }] = useMutation(LOGOUT_MUTATION, {
    onCompleted: async () => {
      setIsAuthenticated(false);
      await nextAuthSignOut({ 
        redirect: false,
        callbackUrl: "/auth"
      });
      router.push("/auth");
      toast.success("Logged out successfully");
    },
    onError: (error) => {
      setIsAuthenticated(false);
      toast.error(error.message || "Failed to logout");
    },
  });

  const handleSignOut = async () => {
    try {
      await logout();
    } catch (error) {
      console.error("Logout error:", error);
      setIsAuthenticated(false);
    }
  };

  // Show loading state while checking auth status
  if (authStatus === 'loading' || (authStatus === 'authenticated' && userLoading)) {
    return (
      <nav className="border-b">
        <div className="flex h-16 items-center px-4 container mx-auto justify-between">
          <Link 
            href="/" 
            className="flex items-center space-x-2 font-bold text-xl hover:opacity-80 transition-opacity"
          >
            <span className="bg-primary text-primary-foreground px-2 py-1 rounded">
              VT
            </span>
          </Link>
          <div className="w-24 h-10 bg-muted animate-pulse rounded" />
        </div>
      </nav>
    );
  }

  const user = userData?.auth?.getCurrentUser?.values;
  const isLoggedIn = authStatus === 'authenticated' && isAuthenticated && user;

  return (
    <nav className="border-b">
      <div className="flex h-16 items-center px-4 container mx-auto justify-between">
        {/* Logo */}
        <Link 
          href="/" 
          className="flex items-center space-x-2 font-bold text-xl hover:opacity-80 transition-opacity"
        >
          <span className="bg-primary text-primary-foreground px-2 py-1 rounded">
            VT
          </span>
        </Link>

        {/* Auth Section */}
        <div className="flex items-center space-x-4">
          {isLoggedIn ? (
            <div className="flex items-center space-x-4">
              <span className="text-sm text-muted-foreground">
                Hello, {user.firstName} {user.lastName} !
              </span>
              <Button
                variant="outline"
                onClick={handleSignOut}
                disabled={logoutLoading}
              >
                {logoutLoading ? "Signing out..." : "Sign Out"}
              </Button>
            </div>
          ) : (
            <Button
              variant="default"
              onClick={() => router.push("/auth")}
            >
              Sign In
            </Button>
          )}
        </div>
      </div>
    </nav>
  );
}