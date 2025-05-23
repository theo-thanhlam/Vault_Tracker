import React from 'react'
import { getAuthStatus } from '@/lib/auth'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { FolderTree, Receipt } from 'lucide-react'
// import { useAuth } from '@/lib/contexts/auth-context'

const DashBoardPage = async () => {
 
  return (
    <div className="container mx-auto py-6 space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Link href="/dashboard/categories">
          <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FolderTree className="h-5 w-5" />
                Categories
              </CardTitle>
              <CardDescription>
                Manage your transaction categories
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="ghost" className="w-full border border-primary">
                View Categories
              </Button>
            </CardContent>
          </Card>
        </Link>

        <Link href="/dashboard/transactions">
          <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Receipt className="h-5 w-5" />
                Transaction
              </CardTitle>
              <CardDescription>
                Manage your transactions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="ghost" className="w-full border border-primary">
                View Transactions
              </Button>
            </CardContent>
          </Card>
        </Link>
      </div>
    </div>
  )
}

export default DashBoardPage