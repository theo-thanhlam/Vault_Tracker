import React, { useState } from 'react'
import { Goal } from '@/types/goal'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '../ui/dialog'
import { format } from 'date-fns'

interface GoalDetailProps {
  goal: Goal | null;

}

const GoalDetail = ({ goal }: GoalDetailProps) => {
  const start_date_display = format(new Date(goal?.startDate || ""), "LLL wo yyyy ")
  const end_date_display = format(new Date(goal?.endDate || ""), "LLL wo yyyy ")
  const created_at_display = format(new Date(goal?.createdAt || ""), "LLL wo yyyy ")
  const updated_at_display = goal?.updatedAt ? format(new Date(goal?.updatedAt), "LLL wo yyyy") : null;
  const progress = Number(((goal?.currentAmount || 0) / (goal?.target || 0) * 100).toFixed(2))

  return (
      <DialogContent>
        <DialogHeader>
          <DialogTitle > Goal Details</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <DialogTitle className="font-bold text-xl">Name</DialogTitle>
            <span className="text-sm text-muted-foreground">{goal?.name}</span>
          </div>
          
          <div>
            <DialogTitle className="font-bold text-xl">Status</DialogTitle>
            <span className="text-sm text-muted-foreground">{goal?.status}</span>
          </div>
          <div>
            <DialogTitle className="font-bold text-xl">Progress</DialogTitle>
            <span className="text-sm text-muted-foreground">{progress}% ({goal?.currentAmount} / {goal?.target})</span>
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
            <span className="text-sm text-muted-foreground">{goal?.description}</span>
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

export default GoalDetail