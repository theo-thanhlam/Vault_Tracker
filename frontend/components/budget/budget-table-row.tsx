import React, { useState } from 'react'
import { Budget } from '@/types/budget'
import { TableCell, TableRow } from '../ui/table';
import { DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '../ui/dropdown-menu';
import { DropdownMenu } from '../ui/dropdown-menu';
import { Eye, MoreHorizontal, Pencil, Trash2 } from 'lucide-react';
import { Button } from '../ui/button';
import { Dialog } from '../ui/dialog';
import BudgetDetail from './budget-detail';
import { Category } from '@/types/category';
import { differenceInCalendarDays } from 'date-fns';
import { Progress } from '../ui/progress';
import { cn } from '@/lib/utils';

enum BudgetType {
  FIXED = "FIXED",
  FLEXIBLE = "FLEXIBLE",
  ROLLING = "ROLLING",
  SAVINGS = "SAVINGS"
}

enum BudgetFrequency {
  DAILY = "DAILY",
  WEEKLY = "WEEKLY",
  BI_WEEKLY = "BI_WEEKLY",
  MONTHLY = "MONTHLY",
  YEARLY = "YEARLY",
  CUSTOM = "CUSTOM"
}

const budgetTypeStyles: Record<BudgetType, { border: string; bg: string; text: string }> = {
  [BudgetType.FIXED]: {
    border: "border-blue-500",
    bg: "bg-blue-50",
    text: "text-blue-700"
  },
  [BudgetType.FLEXIBLE]: {
    border: "border-green-500",
    bg: "bg-green-50",
    text: "text-green-700"
  },
  [BudgetType.ROLLING]: {
    border: "border-purple-500",
    bg: "bg-purple-50",
    text: "text-purple-700"
  },
  [BudgetType.SAVINGS]: {
    border: "border-yellow-500",
    bg: "bg-yellow-50",
    text: "text-yellow-700"
  }
};

const budgetFrequencyStyles: Record<BudgetFrequency, { border: string; bg: string; text: string }> = {
  [BudgetFrequency.DAILY]: {
    border: "border-red-500",
    bg: "bg-red-50",
    text: "text-red-700"
  },
  [BudgetFrequency.WEEKLY]: {
    border: "border-orange-500",
    bg: "bg-orange-50",
    text: "text-orange-700"
  },
  [BudgetFrequency.BI_WEEKLY]: {
    border: "border-amber-500",
    bg: "bg-amber-50",
    text: "text-amber-700"
  },
  [BudgetFrequency.MONTHLY]: {
    border: "border-emerald-500",
    bg: "bg-emerald-50",
    text: "text-emerald-700"
  },
  [BudgetFrequency.YEARLY]: {
    border: "border-teal-500",
    bg: "bg-teal-50",
    text: "text-teal-700"
  },
  [BudgetFrequency.CUSTOM]: {
    border: "border-gray-500",
    bg: "bg-gray-50",
    text: "text-gray-700"
  }
};

interface BudgetRowProps {
  budget: Budget;
  onViewDetails?: (budget: Budget) => void;
  onEdit?: (budget: Budget) => void;
  onDelete?: (budget: Budget) => void;
}

const BudgetRow = ({budget, onViewDetails, onEdit, onDelete}: BudgetRowProps) => {
    const [isDetailsOpen, setIsDetailsOpen] = useState(false);
    const endDate = new Date(budget.endDate)
    const today = new Date()
    const remainingDays = differenceInCalendarDays(endDate, today)
    const progress = Number(((budget.amount - budget.currentAmount) / budget.amount) * 100)

    const typeStyles = budgetTypeStyles[budget.type as BudgetType];
    const frequencyStyles = budgetFrequencyStyles[budget.frequency as BudgetFrequency];

  return (
    <TableRow>
      <TableCell>{budget.name}</TableCell>
      <TableCell className="">
        <div className={`rounded-full w-fit px-2 py-1 text-sm  ${typeStyles.border} ${typeStyles.bg} ${typeStyles.text}`}>
        {budget.type}
        </div>
      </TableCell>
      <TableCell className="">
        <div className={`rounded-full w-fit px-2 py-1 text-sm  ${frequencyStyles.border} ${frequencyStyles.bg} ${frequencyStyles.text}`}>
          {budget.frequency}
        </div>
      </TableCell>
      <TableCell className='flex flex-row justify-start items-center gap-2 '>
        <Progress value={progress} className="w-[60%]" />
        <p className="text-sm text-gray-500">{progress}% ({budget.currentAmount} / {budget.amount})</p>
      </TableCell>
      <TableCell>{remainingDays} days</TableCell>
      <TableCell>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            {onViewDetails && (
              <DropdownMenuItem onClick={() => setIsDetailsOpen(true)}>
                <Eye className="mr-2 h-4 w-4" />
                View Details
              </DropdownMenuItem>
            )}
            {onEdit && (
              <DropdownMenuItem onClick={() => onEdit(budget)}>
                <Pencil className="mr-2 h-4 w-4" />
                Edit
              </DropdownMenuItem>
            )}
            {onDelete && (
              <DropdownMenuItem onClick={() => onDelete(budget)} className="text-destructive">
                <Trash2 className="mr-2 h-4 w-4" />
                Delete
              </DropdownMenuItem>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
      </TableCell>
      <Dialog open={isDetailsOpen} onOpenChange={setIsDetailsOpen}>
        <BudgetDetail budget={budget} />
      </Dialog>
    </TableRow>
  )
}

export default BudgetRow