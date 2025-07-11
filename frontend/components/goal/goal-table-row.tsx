"use client"
import { Goal } from '@/types/goal';
import React, { useState } from 'react'
import { TableCell, TableRow } from '@/components/ui/table';
import { differenceInCalendarDays } from 'date-fns';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Eye, MoreHorizontal, Pencil, Table, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Dialog } from '@radix-ui/react-dialog';
import GoalDetail from './goal-detail';
interface GoalTableRowProps {
  goal: Goal;
  onViewDetails?: (goal: Goal) => void;
  onEdit?: (goal: Goal) => void;
  onDelete?: (goal: Goal) => void;
}
const statusConfig = {
 
  IN_PROGRESS: {
    label: "In Progress",
    borderColor: "border-blue-400",
    bgColor: "bg-blue-50",
    textColor: "text-blue-700"
  },
  COMPLETED: {
    label: "Completed",
    borderColor: "border-green-400",
    bgColor: "bg-green-50",
    textColor: "text-green-700"
  },
  FAILED: {
    label: "Failed",
    borderColor: "border-red-400",
    bgColor: "bg-red-50",
    textColor: "text-red-700"
  },
  CANCELLED: {
    label: "Cancelled",
    borderColor: "border-yellow-400",
    bgColor: "bg-yellow-50",
    textColor: "text-yellow-700"
  }
} as const;

const GoalTableRow = ({ goal, onViewDetails, onEdit, onDelete }: GoalTableRowProps) => {
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);

  const endDate = new Date(goal.endDate)
  const today = new Date()
  const remainingDays = differenceInCalendarDays(endDate, today)
  const status = statusConfig[goal.status as keyof typeof statusConfig]
  const progress = Number(((goal.currentAmount / goal.target) * 100).toFixed(2))
  

  return (
    <TableRow>
      {/* <TableCell>{goal.name}</TableCell>
      <TableCell>
        <div className={`rounded-full w-fit px-2 py-1 text-xs font-medium ${status.borderColor} ${status.bgColor} ${status.textColor}`}>
          {status.label}
        </div>
      </TableCell> */}
      <TableCell>
        <div className="flex flex-col sm:flex-row sm:items-center gap-1">
          <span> {goal.name}</span>
          <div className={`rounded-full w-fit px-2 py-1 text-xs font-medium ${status.borderColor} ${status.bgColor} ${status.textColor} md:hidden`}>
          {status.label}
        </div>

        </div>
      </TableCell>
      {/* Desktop Label Only */}
      <TableCell className='hidden md:block'>
        <div className={`rounded-full w-fit px-2 py-1 text-xs font-medium ${status.borderColor} ${status.bgColor} ${status.textColor}`}>
          {status.label}
        </div>
      </TableCell>
      <TableCell>
        <div className="flex flex-col sm:flex-row sm:items-center gap-1">
          <div className='w-1/2 hidden md:block'>
          <Progress value={progress} className="w-full" indicatorColor='bg-green-100'/>
        </div>
        
        <p className="text-sm text-gray-500">{progress}% ({goal.currentAmount} / {goal.target})</p>
        </div>
      </TableCell>

      {/* Desktop only */}
      <TableCell className='hidden md:block'>{remainingDays} days</TableCell>
      <TableCell className='flex flex-row justify-start items-center gap-2 hidden md:block'>
        <div className='w-1/2 hidden md:block'>
          <Progress value={progress} className="w-full" indicatorColor='bg-green-100'/>
        </div>
        
        <p className="text-sm text-gray-500">{progress}% ({goal.currentAmount} / {goal.target})</p>
      </TableCell>
      
       
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
              <DropdownMenuItem onClick={() => onEdit(goal)}>
                <Pencil className="mr-2 h-4 w-4" />
                Edit
              </DropdownMenuItem>
            )}
            {onDelete && (
              <DropdownMenuItem onClick={() => onDelete(goal)} className="text-destructive">
                <Trash2 className="mr-2 h-4 w-4" />
                Delete
              </DropdownMenuItem>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
      </TableCell>
      <Dialog open={isDetailsOpen} onOpenChange={setIsDetailsOpen}>
        <GoalDetail goal={goal} />
      </Dialog>
    </TableRow>
  );
};

export default GoalTableRow;