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
import { Menu, X } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export default function Navbar() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authStatus, setAuthStatus] = useState<'authenticated' | 'unauthenticated' | 'loading'>('loading');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

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

  const AuthButtons = () => (
    <>
      {isLoggedIn ? (
        <div className="flex flex-col lg:flex-row items-center gap-4">
          <Button
            variant="ghost"
            onClick={() => {
              // router.push("/dashboard");
              setIsMobileMenuOpen(false);
            }}
            className="w-full lg:w-auto border border-primary bg-primary/10 text-primary"
          >
            Go to Dashboard
          </Button>
          <Button
            variant="outline"
            onClick={() => {
              handleSignOut();
              setIsMobileMenuOpen(false);
            }}
            disabled={logoutLoading}
            className="w-full lg:w-auto border border-primary bg-primary/30"
          >
            {logoutLoading ? "Signing out..." : "Sign Out"}
          </Button>
        </div>
      ) : (
        <Button
          variant="default"
          onClick={() => {
            // router.push("/auth");
            setIsMobileMenuOpen(false);
          }}
          className="w-full lg:w-auto"
        >
          Sign In
        </Button>
      )}
    </>
  );

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

        {/* Desktop Auth Section */}
        <div className="hidden lg:flex items-center space-x-4">
          <AuthButtons />
        </div>

        {/* Mobile Menu Button */}
        <div className="lg:hidden">
          <Dialog open={isMobileMenuOpen} onOpenChange={setIsMobileMenuOpen}>
            <DialogTrigger asChild>
              <Button variant="ghost" size="icon" className="h-9 w-9">
                <Menu className="h-5 w-5" />
                <span className="sr-only">Toggle menu</span>
              </Button>
            </DialogTrigger>
            <DialogContent className="w-[95vw] sm:w-[425px] p-0 gap-0">
              <DialogHeader className="px-6 py-4 border-b">
                <DialogTitle className="text-lg">Menu</DialogTitle>
              </DialogHeader>
              <div className="p-6 space-y-4">
                <AuthButtons />
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>
    </nav>
  );
}