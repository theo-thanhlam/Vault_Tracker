// app/(protected)/layout.tsx

import { headers } from 'next/headers'
import { redirect } from 'next/navigation'
import React, { ReactNode } from 'react'

interface ProtectedLayoutProps {
  children: ReactNode
}

export default async function ProtectedLayout({ children }: ProtectedLayoutProps) {
    const authHeader =  (await headers()).get("x-auth-status")
    
    
    if( authHeader !== "authenticated"){
        redirect("/auth")
    }



    return (
        <>
            {children}
        </>
    )
}
