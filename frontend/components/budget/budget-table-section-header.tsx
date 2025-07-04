import { RefreshCcwIcon } from 'lucide-react'
import React, { useState } from 'react'
import { Button } from '../ui/button'
import TableSectionHeader from '../form-components/table-section-header';
import BudgetForm from './budget-form';

const BudgetTableSectionHeader = ({refetch}: {refetch: () => void}) => {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const handleCreateSuccess = () => {
    setIsCreateDialogOpen(false);
    refetch();
  };
  return (
    <TableSectionHeader
      title="Budgets"
      action_title="Add Budget"
      formTitle="Create Budget"
      formDescription="Create a new budget"
      open={isCreateDialogOpen}
      onOpenChange={setIsCreateDialogOpen}
      onSuccess={handleCreateSuccess}
      formComponent={<BudgetForm onSuccess={handleCreateSuccess} />}
    />
  )
}

export default BudgetTableSectionHeader