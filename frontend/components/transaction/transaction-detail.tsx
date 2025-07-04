import React from 'react'
import { Transaction } from '@/types/transaction';
import { DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { format } from 'date-fns';
import { DollarSign, Tag, FileText, Calendar, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';

interface TransactionDetailProps {
    transaction: Transaction;
}

const TransactionDetail = ({ transaction }: TransactionDetailProps) => {
  const amount_display =
    transaction.categoryType === "expense"
      ? `- \$${transaction.amount.toFixed(2)}`
      : `\$${transaction.amount.toFixed(2)}`;

  return (
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Transaction Details</DialogTitle>
        <DialogDescription>
          View the complete details of this transaction.
        </DialogDescription>
      </DialogHeader>
      <div className="space-y-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <DollarSign className="h-5 w-5 text-primary" />
            <DialogTitle className="font-bold text-xl">Amount</DialogTitle>
          </div>
          <span className={cn(
            "text-2xl font-semibold",
            transaction.categoryType === "expense" ? "text-destructive" : "text-green-600"
          )}>
            {amount_display}
          </span>
        </div>
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Tag className="h-5 w-5 text-primary" />
            <DialogTitle className="font-semibold text-xl">Type</DialogTitle>
          </div>
          <span className="uppercase text-sm font-bold">{transaction.categoryType}</span>
        </div>
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Tag className="h-5 w-5 text-primary" />
            <DialogTitle className="font-semibold text-xl">Category</DialogTitle>
          </div>
          <span className="text-sm ">{transaction.categoryName}</span>
        </div>
        
        <div>
          <div className="flex items-center gap-2 mb-2">
            <FileText className="h-5 w-5 text-primary" />
            <DialogTitle className="font-semibold text-xl">Description</DialogTitle>
          </div>
          <span className="text-sm font-light">{transaction.description || "No description"}</span>
        </div>
        <hr className="my-4" />
        <div className="space-y-2 text-xs text-muted-foreground">
          <div>
            <span>Created: {format(new Date(transaction.createdAt), "LLL wo yyyy HH:mm:ss")}</span>
          </div>
          {transaction.updatedAt && ( 
          <div>
            <span>Updated: {format(new Date(transaction.updatedAt), "LLL wo yyyy HH:mm:ss")}</span>
          </div>
          )}
        </div>
       
      </div>
    </DialogContent>
  )
}

export default TransactionDetail