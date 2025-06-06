import React from 'react'
import { Budget } from '@/types/budget'
import { TableBody, TableCell, TableRow } from '../ui/table';
import BudgetRow from './budget-table-row';
import { differenceInCalendarDays } from 'date-fns';

interface BudgetTableBodyProps {
  sortBy: string;
  filterByTypes: string;
  filterByFrequencies: string;
  budgets: Budget[];
  onViewDetails?: (budget: Budget) => void;
  onEdit?: (budget: Budget) => void;
  onDelete?: (budget: Budget) => void;
}

const filterBudgets = (budgets: Budget[], filterByTypes: string, filterByFrequencies: string, sortBy: string) => {
  
  let filtered = budgets

  filtered = filterByTypes === "all"?
  [...filtered]:
  filtered.filter((budget: Budget) => budget.type === filterByTypes)

  filtered = filterByFrequencies === "all"?
  [...filtered]:
  filtered.filter((budget: Budget) => budget.frequency === filterByFrequencies)
 
  return [...filtered].sort((a: Budget, b: Budget) => {
    switch (sortBy) {
      case 'remaining':
        return a.currentAmount - b.currentAmount;
     
      case 'duration':
        return differenceInCalendarDays(new Date(b.endDate), new Date(b.startDate)) - differenceInCalendarDays(new Date(a.endDate), new Date(a.startDate));
      default:
        return 0;
    }
  })
}

const BudgetTableBody = ({sortBy, filterByTypes, filterByFrequencies, budgets, onViewDetails, onEdit, onDelete}: BudgetTableBodyProps) => {
  const filteredBudgets = filterBudgets(budgets, filterByTypes, filterByFrequencies, sortBy);
  return (
    <TableBody>
      {
        budgets.length === 0 ? (
          <TableRow>
            <TableCell colSpan={6} className="text-center">
              <p className="text-gray-500">Add a budget to get started</p>
            </TableCell>
          </TableRow>
        ):(
          filteredBudgets.map((budget: Budget) => (
            <BudgetRow key={budget.id} budget={budget} onViewDetails={onViewDetails} onEdit={onEdit} onDelete={onDelete} />
          ))
        )
      }
    </TableBody>
  )
}

export default BudgetTableBody