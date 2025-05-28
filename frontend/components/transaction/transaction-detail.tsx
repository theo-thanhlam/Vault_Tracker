import React from 'react'
import { Transaction } from '@/types/transaction';
import { DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';

interface TransactionDetailProps {
    transaction: Transaction;
}

const TransactionDetail = ({ transaction }: TransactionDetailProps) => {
  return (
    <DialogContent className="sm:max-w-[425px]">
    <DialogHeader>
            <DialogTitle>Transaction Details</DialogTitle>
            <DialogDescription>
              View the complete details of this transaction.
            </DialogDescription>
    </DialogHeader>
    </DialogContent>
          
  )
}

export default TransactionDetail