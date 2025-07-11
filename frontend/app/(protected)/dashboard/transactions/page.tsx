import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TransactionTable } from "@/components/transaction/transaction-table";
import { getTransactions } from "@/lib/graphql/transaction/queries";
import PageWrapper from "@/components/dashboard/page-wrapper";

export default async function TransactionsPage() {
  const transactions = await getTransactions()
  
  
  
  return (
    <PageWrapper>
      <TransactionTable initialTransactions={transactions}/>
    </PageWrapper>
  );
} 