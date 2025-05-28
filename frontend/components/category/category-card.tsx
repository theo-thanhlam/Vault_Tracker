"use client";

import { useState } from "react";
import { format } from "date-fns";
import { motion } from "framer-motion";
import { MoreHorizontal, Pencil, Trash, Tag, FileText, Calendar } from "lucide-react";
import { useMutation } from "@apollo/client";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { CategoryTypeEnum, Category } from "@/types/category";
import { DELETE_CATEGORY_MUTATION } from "@/lib/graphql/category/gql";
import { CategoryForm } from "./category-form";

interface CategoryCardProps extends Omit<Category, 'userId'> {
  onEdit?: (category: Category) => void;
  onDelete?: (category: Category) => void;
  onSuccess?: () => void;
}

export function CategoryCard({
  id,
  name,
  description,
  type,
  createdAt,
  updatedAt,
  onEdit,
  onDelete,
  onSuccess,
}: CategoryCardProps) {
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  const [deleteCategory] = useMutation(DELETE_CATEGORY_MUTATION, {
    onCompleted: () => {
      toast.success("Category deleted successfully");
      setIsDeleteDialogOpen(false);
      onSuccess?.();
    },
    onError: (error) => {
      toast.error(error.message || "Failed to delete category");
    },
  });

  const handleDelete = async () => {
    if (onDelete) {
      onDelete({ id, name, description, type, createdAt, updatedAt });
    } else {
      await deleteCategory({
        variables: {
          input: { id },
        },
      });
    }
  };

  const handleEdit = () => {
    if (onEdit) {
      onEdit({ id, name, description, type, createdAt, updatedAt });
    } else {
      setIsEditDialogOpen(true);
    }
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.2 }}
      >
        <Card 
          className="cursor-pointer hover:bg-accent/50 transition-colors"
          onClick={() => setIsDetailsOpen(true)}
        >
          <CardContent className="px-4 py-3">
            <div className="flex justify-between items-start flex-col md:flex-row">
              <div className="flex-1">
                <h3 className="font-medium text-md md:text-lg lg:text-xl">{name}</h3>
                <p className="text-sm text-muted-foreground mt-1 hidden md:block">
                  {description}
                </p>
              </div>
              <div className="flex items-center gap-2 w-full md:w-auto justify-between md:justify-end" onClick={(e) => e.stopPropagation()}>
                <div className="text-right">
                  <p className="font-medium text-md md:text-lg lg:text-xl">{type}</p>
                  <p className="text-sm text-muted-foreground hidden md:block">
                    Created {format(new Date(createdAt), "MMM d, yyyy")}
                  </p>
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-8 w-8 ml-auto md:ml-0">
                      <MoreHorizontal className="h-4 w-4" />
                      <span className="sr-only">Open menu</span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={(e) => {
                      e.stopPropagation();
                      handleEdit();
                    }}>
                      <Pencil className="h-4 w-4 mr-2" />
                      Edit
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      className="text-destructive focus:text-destructive"
                      onClick={(e) => {
                        e.stopPropagation();
                        setIsDeleteDialogOpen(true);
                      }}
                    >
                      <Trash className="h-4 w-4 mr-2" />
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Details Dialog */}
      <Dialog open={isDetailsOpen} onOpenChange={setIsDetailsOpen}>
        <DialogContent className="w-[95vw] sm:w-[425px] md:w-[600px] lg:w-[800px] max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-lg sm:text-xl md:text-2xl">Category Details</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="flex items-center gap-2">
              <Tag className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Type</p>
                <p className="text-md md:text-lg font-bold">{type}</p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <FileText className="h-4 w-4 text-muted-foreground" />
              <div className="flex-1">
                <p className="text-sm font-medium">Description</p>
                <p className="text-sm md:text-base text-muted-foreground">{description}</p>
              </div>
            </div>

           <div className="pt-4 border-t">
              
              <p className="text-xs text-muted-foreground">
                Created: {format(new Date(createdAt), "PPP")}
              </p>
              {updatedAt && (
                <p className="text-xs text-muted-foreground">
                  Last Updated: {format(new Date(updatedAt), "PPP")}
                </p>
              )}
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="w-[95vw] sm:w-[425px] md:w-[600px] lg:w-[800px] max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-lg sm:text-xl md:text-2xl">Edit Category</DialogTitle>
          </DialogHeader>
          <CategoryForm
            initialData={{
              id,
              name,
              type,
              description,
            }}
            onSuccess={() => {
              setIsEditDialogOpen(false);
              onSuccess?.();
            }}
          />
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <DialogContent className="w-[95vw] sm:w-[425px] md:w-[500px]">
          <DialogHeader>
            <DialogTitle className="text-lg sm:text-xl md:text-2xl">Delete Category</DialogTitle>
          </DialogHeader>
          <div className="flex flex-col sm:flex-row justify-end gap-2 mt-4">
            <Button
              variant="outline"
              onClick={() => setIsDeleteDialogOpen(false)}
              className="w-full sm:w-auto"
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleDelete}
              className="w-full sm:w-auto"
            >
              Delete
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
} 