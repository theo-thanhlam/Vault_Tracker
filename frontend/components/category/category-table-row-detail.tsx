import React from 'react'
import { DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../ui/dialog'
import { format } from 'date-fns'
import { Category } from '@/types/category'

const CategoryTableRowDetail = ({ category }: { category: Category }) => {
  const created_at_display = format(new Date(category.createdAt), "LLL wo yyyy HH:mm:ss");
  const updated_at_display = category.updatedAt ? format(new Date(category.updatedAt), "LLL wo yyyy HH:mm:ss") : null;

  return (
    <>
    <DialogContent>
          <DialogHeader>
            <DialogTitle>Category Details</DialogTitle>
            <DialogDescription>
              View detailed information about this category.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <DialogTitle className="font-bold text-xl">Name</DialogTitle>
              <span className="text-sm text-muted-foreground">{category.name}</span>
            </div>
            <div>
              <DialogTitle className="font-semibold text-xl">Type</DialogTitle>
              <span className="uppercase text-sm text-muted-foreground">{category.type}</span>
            </div>
            <div>
              <DialogTitle className="font-semibold text-xl">Description</DialogTitle>
              <span className="text-sm text-muted-foreground">{category.description || "No description"}</span>
            </div>
            <div>
              <DialogTitle className="font-semibold text-xl">Created At</DialogTitle>
              <span className="text-sm text-muted-foreground">{created_at_display}</span>
            </div>
            {
              category.updatedAt && (
                <div>
                  <DialogTitle className="font-semibold">Updated At</DialogTitle>
                  <span className="text-sm text-muted-foreground">{updated_at_display}</span>
                </div>
              )
            }
          
          </div>
        </DialogContent>
    </>
  )
}

export default CategoryTableRowDetail