import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TransactionTable } from "@/components/transaction/transaction-table";
import { getTransactions } from "@/lib/graphql/transaction/queries";

export default async function TransactionsPage() {
  const transactions = await getTransactions()
  
  
  
  return (
    <div className="container mx-auto py-6 space-y-6 w-auto">
      <div className="flex items-start gap-4 flex-col">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/dashboard" className="flex items-start gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
        </Button>
        {/* <h1 className="text-3xl font-bold">Transactions</h1> */}
      </div>
      <TransactionTable initialTransactions={transactions}/>
   </div>
  );
} 