import { getAuthStatus } from '@/lib/auth'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { FolderTree, Receipt, Target, Wallet } from 'lucide-react'
import FeatureCard from '@/components/dashboard/feature-card'
// import { useAuth } from '@/lib/contexts/auth-context'

const DashBoardPage = async () => {
 
  return (
    <div className="container mx-auto py-6 space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <FeatureCard
          title="Categories"
          description="Manage your transaction categories"
          icon={<FolderTree className="h-5 w-5" />}
          href="/dashboard/categories"
        />
        <FeatureCard
          title="Transactions"
          description="Manage your transactions"
          icon={<Receipt className="h-5 w-5" />}
          href="/dashboard/transactions"
        />
        <FeatureCard
          title="Goals"
          description="Manage your goals"
          icon={<Target className="h-5 w-5" />}
          href="/dashboard/goals"
        />
        <FeatureCard
          title="Budget"
          description="Manage your budget"
          icon={<Wallet className="h-5 w-5" />}
          href="/dashboard/budgets"
        />
       
      </div>
    </div>
  )
}

export default DashBoardPage