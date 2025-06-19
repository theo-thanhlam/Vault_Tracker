"use client";

import React, { useState } from "react";
import LoginForm from "@/components/auth/loginForm";
import RegisterForm from "@/components/auth/registerForm";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { motion, AnimatePresence } from "framer-motion";

export default function AuthPage() {
  const [tab, setTab] = useState<"login" | "register">("login");
  console.log(process.env.NEXT_PUBLIC_API_URL)

  return (
    <div className="flex justify-center items-center min-h-screen  bg-background">
      
      <Card className="w-full max-w-md flex flex-col justify-center shadow-lg ">
        <CardHeader className="flex flex-col items-center gap-2">
          <CardTitle className="justify-center pb-4 text-2xl">Vault Tracker</CardTitle>

          <CardTitle>
            <div className="flex gap-2">
              <Button
                variant={tab === "login" ? "default" : "outline"}
                onClick={() => setTab("login")}
                className="rounded-b-none"
              >
                Login
              </Button>
              <Button
                variant={tab === "register" ? "default" : "outline"}
                onClick={() => setTab("register")}
                className="rounded-b-none"
              >
                Register
              </Button>
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 flex flex-col justify-center">
          <AnimatePresence mode="wait" >
            <motion.div
              key={tab}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -30 }}
              transition={{ duration: 0.3 }}
            >
              {tab === "login" ? <LoginForm /> : <RegisterForm />}
            </motion.div>
          </AnimatePresence>
        </CardContent>
      </Card>
    </div>
  );
}