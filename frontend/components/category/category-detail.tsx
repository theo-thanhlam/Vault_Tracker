import React from 'react'
import { DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../ui/dialog'
import { format } from 'date-fns'
import { Category } from '@/types/category'

const CategoryDetail = ({ category }: { category: Category }) => {
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
            <hr className="my-4" />
            <div className="space-y-2 text-xs text-muted-foreground">
              <div>
                <span>Created: {created_at_display}</span>
              </div>
              {category.updatedAt && (
                <div>
                  <span>Updated: {updated_at_display}</span>
                </div>
              )}
            </div>
          
          </div>
        </DialogContent>
    </>
  )
}

export default CategoryDetail