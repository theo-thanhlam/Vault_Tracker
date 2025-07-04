import React from 'react'
import { Budget } from '@/types/budget'
import { DialogContent, DialogHeader, DialogTitle } from '../ui/dialog'
import { format } from 'date-fns'

interface BudgetDetailProps {
  budget: Budget;
}

const BudgetDetail = ({ budget }: BudgetDetailProps) => {
  const start_date_display = format(new Date(budget?.startDate), 'MMM d, yyyy')
  const end_date_display = format(new Date(budget?.endDate), 'MMM d, yyyy')
  const created_at_display = format(new Date(budget?.createdAt), 'MMM d, yyyy')
  const updated_at_display = budget?.updatedAt ? format(new Date(budget?.updatedAt), 'MMM d, yyyy') : null
  return (
    <DialogContent>
    <DialogHeader>
      <DialogTitle > Goal Details</DialogTitle>
    </DialogHeader>
    <div className="space-y-4">
      <div>
        <DialogTitle className="font-bold text-xl">Name</DialogTitle>
        <span className="text-sm text-muted-foreground">{budget?.name}</span>
      </div>
      
      <div>
        <DialogTitle className="font-bold text-xl">Type</DialogTitle>
        <span className="text-sm text-muted-foreground">{budget?.type}</span>
      </div>
      <div>
        <DialogTitle className="font-bold text-xl">Frequency</DialogTitle>
        <span className="text-sm text-muted-foreground">{budget?.frequency}</span>
      </div>
      <div>
        <DialogTitle className="font-bold text-xl">Start Date</DialogTitle>
        <span className="text-sm text-muted-foreground">{start_date_display}</span>
      </div>
      <div>
        <DialogTitle className="font-bold text-xl">End Date</DialogTitle>
        <span className="text-sm text-muted-foreground">{end_date_display}</span>
      </div>
      <div>
        <DialogTitle className="font-bold text-xl">Description</DialogTitle>
        <span className="text-sm text-muted-foreground">{budget?.description}</span>
      </div>
      <hr className="my-4" />
      <div className="space-y-2 text-xs text-muted-foreground">
        <div>
          <span>Created: {created_at_display}</span>
        </div>
        {updated_at_display && (
          <div>
            <span>Updated: {updated_at_display}</span>
          </div>
        )}
      </div>
    </div>
  </DialogContent>
  )
}

export default BudgetDetail