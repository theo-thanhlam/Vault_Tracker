import React, { useState } from 'react'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import { TransactionForm } from './transaction-form';

const TransactionTableHeader = ({ refetch }: { refetch: () => void }) => {
    const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
    const handleTransactionSuccess = () => {
        setIsCreateDialogOpen(false);
        refetch();
      };
  return (
    <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Recent Transactions</h2>
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-2 w-2 md:h-4 md:w-4" />
              <span className="hidden md:block">Add Transaction</span>
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create Transaction</DialogTitle>
              <DialogDescription>
                Add a new transaction to your account.
              </DialogDescription>
            </DialogHeader>
            <TransactionForm
              onSuccess={handleTransactionSuccess}
            />
          </DialogContent>
        </Dialog>
      </div>
  )
}

export default TransactionTableHeader