import React, { useState } from 'react'

import { TransactionForm } from './transaction-form';
import TableSectionHeader from '../form-components/table-section-header';

const TransactionTableSectionHeader = ({ refetch }: { refetch: () => void }) => {
    const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
    const handleTransactionSuccess = () => {
        setIsCreateDialogOpen(false);
        refetch();
      };
  return (
    <TableSectionHeader
      title="Recent Transactions"
      action_title="Add Transaction"
      formTitle="Create Transaction"
      formDescription="Add a new transaction to your account."
      open={isCreateDialogOpen}
      onOpenChange={setIsCreateDialogOpen}
      onSuccess={handleTransactionSuccess}
      formComponent={
        <TransactionForm
          onSuccess={handleTransactionSuccess}
        />
      }
    />
  )
}

export default TransactionTableSectionHeader