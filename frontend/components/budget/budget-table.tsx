"use client"
import React, { useState } from 'react'
import BudgetTableSectionHeader from './budget-table-section-header'
import BudgetTableFilter from './budget-table-filter'
import { EditDialog } from '../form-components/edit-dialog'
import { DeleteDialog } from '../form-components/delete-dialog'
import { Table, TableBody, TableCell, TableRow } from '../ui/table'
import BudgetTableHeader from './budget-table-header'
import BudgetTableBody from './budget-table-body'
import BudgetSkeleton from './budget-skeleton'
import { Budget } from '@/types/budget'
import { useMutation, useQuery } from '@apollo/client'
import { GET_ALL_BUDGETS } from '@/lib/graphql/budget/gql'
import { Goal } from '@/types/goal'
import BudgetForm from './budget-form'
import { DELETE_BUDGET } from '@/lib/graphql/budget/gql'
import { toast } from 'sonner'

const BudgetTable = () => {
  const [sortBy, setSortBy] = useState("amount");
  const [filterByTypes, setFilterByTypes] = useState("all");
  const [filterByFrequencies, setFilterByFrequencies] = useState("all");
  const [selectedBudget, setSelectedBudget] = useState<Budget | null>(null);
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false);

  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const {data, loading, error, refetch} = useQuery(GET_ALL_BUDGETS,{
    fetchPolicy: "network-only",
  } )
  const budgets = data?.budget.getAllBudgets.values || [];
  const handleSortChange = (value: string) => {
    setSortBy(value);
  };

  const handleFilterByTypes = (value: string) => {
    setFilterByTypes(value);
  };

  const handleFilterByFrequencies = (value: string) => {
    setFilterByFrequencies(value);
  };

  const handleViewDetails = (budget: Budget) => {
    setSelectedBudget(budget);
    setIsDetailDialogOpen(true);
  };

  const handleEdit = (budget: Budget) => {

    setSelectedBudget(budget);
    setIsEditDialogOpen(true);
  };

  const handleDelete = (budget: Budget) => {
    setSelectedBudget(budget);
    setIsDeleteDialogOpen(true);
  };
  const [deleteBudget] = useMutation(DELETE_BUDGET, {
    onCompleted: () => {
      toast.success("Budget deleted successfully");
      refetch();
    },
    onError: (error) => {
      toast.error("Failed to delete budget");
    },
  });

  const handleDeleteConfirm = async () => {
      if (!selectedBudget) return;
      
      await deleteBudget({
        variables: {
          input: {
            id: selectedBudget.id,
          },
        },
      });
      setIsDeleteDialogOpen(false);
      setSelectedBudget(null);
  }


  return (
    <div className='flex flex-col gap-4'>
        <BudgetTableSectionHeader refetch={refetch} />
        <BudgetTableFilter
          handleSortChange={handleSortChange}
          handleFilterByTypes={handleFilterByTypes}
          handleFilterByFrequencies={handleFilterByFrequencies}
        />
        <div className='overflow-x-auto'>
          <Table>
            <BudgetTableHeader />
            {loading ? (
            <TableBody>
              <TableRow>
                <TableCell colSpan={6} className="text-center">
                  <BudgetSkeleton />
                </TableCell>
              </TableRow>
            </TableBody>
          ) : error ? (
            <TableBody>
              <TableRow>
                <TableCell colSpan={6} className="text-center">
                  Something went wrong. Please try again.
                </TableCell>
              </TableRow>
            </TableBody>
          ) : (
            <BudgetTableBody 
              sortBy={sortBy} 
              filterByTypes={filterByTypes} 
              filterByFrequencies={filterByFrequencies} 
              budgets={budgets} 
              onViewDetails={handleViewDetails}
              onEdit={handleEdit} 
              onDelete={handleDelete}
            />
          )}
          </Table>
        </div>
        <EditDialog
          title="Edit Budget"
          description="Update budget details"
          open={isEditDialogOpen}
          onOpenChange={setIsEditDialogOpen}
          formComponent={selectedBudget && <BudgetForm initialData={selectedBudget} onSuccess={() => {
            setIsEditDialogOpen(false);
            refetch();
          }} />} 
        />

        <DeleteDialog
          
          open={isDeleteDialogOpen}
          onOpenChange={setIsDeleteDialogOpen}
          onDelete={handleDeleteConfirm}
        />
    </div>
  )
}

export default BudgetTable