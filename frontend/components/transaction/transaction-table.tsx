"use client";

import { useState } from "react";
import { useMutation, useQuery } from "@apollo/client";
import { toast } from "sonner";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
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
import { Checkbox } from "@/components/ui/checkbox";
import { TransactionForm } from "@/components/transaction/transaction-form";
import { TransactionTableRow } from "@/components/transaction/transaction-table-row";
import { TransactionPagination } from "@/components/transaction/transaction-pagination";
import { GET_TRANSACTIONS_QUERY } from "@/lib/graphql/transaction/queries";
import { DELETE_TRANSACTION_MUTATION } from "@/lib/graphql/transaction/mutations";
import { Transaction } from "@/types/transaction";
import TransactionTableHeader from "./transaction-table-header";

interface TransactionTableProps {
  initialTransactions?: Transaction[];
}

const DEFAULT_PAGE_SIZE = 10;

export function TransactionTable(props: TransactionTableProps) {
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);
  const [selectedRows, setSelectedRows] = useState<string[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(DEFAULT_PAGE_SIZE);

  const { data, loading, refetch } = useQuery(GET_TRANSACTIONS_QUERY, {
    variables: {
      input: {
        limit: pageSize,
        offset: (currentPage - 1) * pageSize
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
    update: (cache, { data }) => {
      const deletedId = data?.transaction?.deleteTransaction?.id;
      if (!deletedId) return;

      // Read the existing transactions from cache
      const existingTransactions = cache.readQuery({
        query: GET_TRANSACTIONS_QUERY,
        variables: {
          input: {
            limit: pageSize,
            offset: (currentPage - 1) * pageSize
          }
        }
      });

      if (!existingTransactions) return;
      
    }
  });

  const transactions = data?.transaction?.getTransactions?.transactions || [];  
  const totalCount = data?.transaction?.getTransactions?.totalCount || 0;
  const totalPages = Math.ceil(totalCount / pageSize);

  const toggleRow = (id: string) => {
    setSelectedRows((prev) =>
      prev.includes(id)
        ? prev.filter((rowId) => rowId !== id)
        : [...prev, id]
    );
  };

  const toggleAll = () => {
    if (selectedRows.length === transactions.length) {
      setSelectedRows([]);
    } else {
      setSelectedRows(transactions.map((t: Transaction) => t.id));
    }
  };

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

  const handleTransactionSuccess = () => {
    setIsEditDialogOpen(false);
    refetch();
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    setSelectedRows([]); // Clear selection when changing pages
  };

  const handlePageSizeChange = (size: number) => {
    setPageSize(size);
    setCurrentPage(1); // Reset to first page when changing page size
    setSelectedRows([]); // Clear selection
  };

  return (
    <div className="space-y-4">
      <TransactionTableHeader refetch={refetch} />

      <div className="rounded-md border">
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[50px] hidden sm:table-cell">
                  <Checkbox
                    checked={
                      transactions.length > 0 &&
                      selectedRows.length === transactions.length
                    }
                    onCheckedChange={toggleAll}
                    aria-label="Select all"
                  />
                </TableHead>
                <TableHead className="font-bold text-lg">Category</TableHead>
                <TableHead className="font-bold text-lg hidden sm:table-cell">Type</TableHead>
                <TableHead className="font-bold text-lg hidden sm:table-cell">Date</TableHead>
                <TableHead className="text-right font-bold text-lg">Amount</TableHead>
                <TableHead className="w-[50px]"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center">
                    Loading...
                  </TableCell>
                </TableRow>
              ) : transactions.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center">
                    No transactions found.
                  </TableCell>
                </TableRow>
              ) : (
                transactions.map((transaction: Transaction) => (
                  <TransactionTableRow
                    key={transaction.id}
                    transaction={transaction}
                    isSelected={selectedRows.includes(transaction.id)}
                    onSelect={toggleRow}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                  />
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </div>

      {/* Pagination Controls */}
      <div className="mt-4">
        {loading ? (
          <div className="text-center text-muted-foreground">Loading pagination...</div>
        ) : (
          <TransactionPagination
            currentPage={currentPage}
            totalPages={totalPages}
            totalItems={totalCount}
            pageSize={pageSize}
            onPageChange={handlePageChange}
            onPageSizeChange={handlePageSizeChange}
          />
        )}
      </div>

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
              onSuccess={handleTransactionSuccess}
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
    </div>
  );
}
  