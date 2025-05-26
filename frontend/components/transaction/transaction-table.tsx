"use client";

import { useState } from "react";
import { useMutation, useQuery } from "@apollo/client";
import { AnimatePresence } from "framer-motion";
import { Plus } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { TransactionForm } from "@/components/transaction/transaction-form";
import { TransactionCard } from "@/components/transaction/transaction-card";
import { GET_TRANSACTIONS_QUERY } from "@/lib/graphql/transaction/queries";
import { DELETE_TRANSACTION_MUTATION } from "@/lib/graphql/transaction/mutations";
import { Transaction } from "@/types/transaction";

interface TransactionTableProps {
  initialTransactions?: Transaction[];
}

export function TransactionTable() {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);



  const { data, loading, refetch } = useQuery(GET_TRANSACTIONS_QUERY, {
    variables:{
      input:{
        limit:10
      }
    }
  });

  const [deleteTransaction] = useMutation(DELETE_TRANSACTION_MUTATION, {
    onCompleted: () => {
      toast.success("Transaction deleted successfully");
      setIsDeleteDialogOpen(false);
      refetch();
    },
    onError: (error) => {
      toast.error(error.message || "Failed to delete transaction");
    },
  });

  const transactions = data?.transaction?.getTransactions?.transactions || [];

  const handleEdit = (transaction: Transaction) => {
    setSelectedTransaction(transaction);
    setIsEditDialogOpen(true);
  };

  const handleDelete = (transaction: Transaction) => {
    setSelectedTransaction(transaction);
    setIsDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!selectedTransaction) return;
    
    try {
      await deleteTransaction({
        variables: {
          input: {
            id: selectedTransaction.id,
          },
        },
      });
    } catch (error) {
      // Error is handled by the mutation's onError
    }
  };

  return (
    <>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
          <CardTitle className="text-md md:text-xl lg:text-2xl">Recent Transactions</CardTitle>
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button size="sm">
                <Plus className="h-4 w-4" />
                <span className="hidden md:block">Add Transaction</span>
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Create New Transaction</DialogTitle>
                <DialogDescription>
                  Add a new transaction to your account.
                </DialogDescription>
              </DialogHeader>
              <TransactionForm
                onSuccess={() => {
                  setIsCreateDialogOpen(false);
                  refetch();
                }}
              />
            </DialogContent>
          </Dialog>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[600px] pr-4">
            <AnimatePresence>
              {loading ? (
                <div className="flex items-center justify-center h-32">
                  <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
                </div>
              ) : transactions.length === 0 ? (
                <div className="text-center text-muted-foreground py-8">
                  No transactions found. Create your first transaction!
                </div>
              ) : (
                <div className="space-y-4">
                  {transactions.map((transaction: Transaction) => (
                    <TransactionCard
                      key={transaction.id}
                      transaction={transaction}
                      onEdit={handleEdit}
                      onDelete={handleDelete}
                    />
                  ))}
                </div>
              )}
            </AnimatePresence>
          </ScrollArea>
        </CardContent>
      </Card>

      {/* Edit Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Edit Transaction</DialogTitle>
            <DialogDescription>
              Update transaction details.
            </DialogDescription>
          </DialogHeader>
          {selectedTransaction && (
            <TransactionForm
              initialData={selectedTransaction}
              onSuccess={() => {
                setIsEditDialogOpen(false);
                refetch();
              }}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete the transaction.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDeleteConfirm}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
} 