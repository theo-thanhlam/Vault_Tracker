"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { useMutation } from "@apollo/client";
import { VERIFY_EMAIL_MUTATION } from "@/lib/graphql/authentication/mutations";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { Suspense } from 'react'

import { toast } from "sonner";

function Verfication(){
  const router = useRouter();
  const searchParams = useSearchParams();
  const [verificationStatus, setVerificationStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const token = searchParams.get('token');

  const [verifyEmail, { loading }] = useMutation(VERIFY_EMAIL_MUTATION, {
    onCompleted: (data) => {
      setVerificationStatus('success');
      toast.success("Email verified successfully!");
    },
    onError: (error) => {
      setVerificationStatus('error');
      toast.error(error.message || "Failed to verify email");
    },
  });

  useEffect(() => {
    const verifyToken = async () => {
      if (!token) {
        setVerificationStatus('error');
        toast.error("No verification token provided");
        return;
      }

      try {
        await verifyEmail({
          variables: {
            input: {
              token: token
            }
          }
        });
      } catch (error) {
        // Error is handled in onError callback
        console.error("Verification error:", error);
      }
    };

    verifyToken();
  }, [token, verifyEmail]);

  if (verificationStatus === 'loading') {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Card className="w-full max-w-md shadow-lg">
          <CardContent className="pt-6">
            <div className="flex flex-col items-center space-y-4">
              <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
              <p className="text-muted-foreground">Verifying your email...</p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="flex justify-center items-center min-h-screen"
    >
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader>
          <CardTitle>
            {verificationStatus === 'success' ? 'Email Verified!' : 'Verification Failed'}
          </CardTitle>
          <CardDescription>
            {verificationStatus === 'success'
              ? 'Your email has been successfully verified. You can now log in to your account.'
              : 'We were unable to verify your email. The token may be invalid or expired.'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button
            className="w-full"
            onClick={() => router.push('/auth')}
          >
            {verificationStatus === 'success' ? 'Go to Login' : 'Try Again'}
          </Button>
        </CardContent>
      </Card>
    </motion.div>
  );
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Verfication />
    </Suspense>
  )
  
  
}