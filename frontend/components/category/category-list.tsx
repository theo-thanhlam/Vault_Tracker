"use client";

import { useState } from "react";
import { useMutation, useQuery } from "@apollo/client";
import { AnimatePresence } from "framer-motion";
import { Plus } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

import { GET_CATEGORIES_QUERY } from "@/lib/graphql/category/queries";
import { CategoryCard } from "./category-card";
import { Category } from "@/types/category";
import { DELETE_CATEGORY_MUTATION } from "@/lib/graphql/category/gql";
import { CategoryForm } from "./category-form";

type CategoryWithoutUserId = Omit<Category, 'userId'>;

export function CategoryList() {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<CategoryWithoutUserId | null>(null);

  const { data, loading, error, refetch } = useQuery(GET_CATEGORIES_QUERY, {
    fetchPolicy: 'network-only', // Don't cache the results
  });

  const categories = data?.category?.getCategory?.values || [];

  const [deleteCategory] = useMutation(DELETE_CATEGORY_MUTATION, {
    onCompleted: () => {
      toast.success("Category deleted successfully");
      setIsDeleteDialogOpen(false);
      refetch(); // Refetch categories after deletion
    },
    onError: (error) => {
      toast.error(error.message || "Failed to delete category");
    },
  });

  const handleEdit = (category: CategoryWithoutUserId) => {
    setSelectedCategory(category);
    setIsEditDialogOpen(true);
  };

  const handleDelete = (category: CategoryWithoutUserId) => {
    setSelectedCategory(category);
    setIsDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!selectedCategory) return;
    
    try {
      await deleteCategory({
        variables: {
          input: {
            id: selectedCategory.id,
          },
        },
      });
    } catch (error) {
      // Error is handled by the mutation's onError
    }
  };

  if (error) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="text-center text-destructive">
            Error loading categories: {error.message}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <>
      <Card className="w-full">
        <CardHeader className="flex flex-row items-center justify-between pb-4">
          <CardTitle className="text-md md:text-xl lg:text-2xl">Recent Categories</CardTitle>
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button size="sm">
                <Plus className="h-4 w-4" />
                <span className="hidden md:block">Add Category</span>
              </Button>
            </DialogTrigger>
            <DialogContent className="w-[95vw] sm:w-[425px] md:w-[600px] lg:w-[800px] max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle className="text-lg sm:text-xl md:text-2xl">Create New Category</DialogTitle>
                <DialogDescription className="text-sm md:text-base">
                  Add a new category to your account.
                </DialogDescription>
              </DialogHeader>
              <CategoryForm
                onSuccess={() => {
                  setIsCreateDialogOpen(false);
                  refetch();
                }}
              />
            </DialogContent>
          </Dialog>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-fit pr-4">
            <AnimatePresence>
              {loading ? (
                <div className="text-center text-muted-foreground py-8">
                  Loading categories...
                </div>
              ) : categories.length === 0 ? (
                <div className="text-center text-muted-foreground py-8">
                  No categories found. Create your first category!
                </div>
              ) : (
                <div className="space-y-4">
                  {categories.map((category: Category) => (
                    <CategoryCard
                      key={category.id}
                      {...category}
                      onEdit={handleEdit}
                      onDelete={handleDelete}
                      onSuccess={refetch}
                    />
                  ))}
                </div>
              )}
            </AnimatePresence>
          </ScrollArea>
        </CardContent>
      </Card>

      {/* Edit Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="w-[95vw] sm:w-[425px] md:w-[600px] lg:w-[800px] max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-lg sm:text-xl md:text-2xl">Edit Category</DialogTitle>
            <DialogDescription className="text-sm md:text-base">
              Update category details.
            </DialogDescription>
          </DialogHeader>
          {selectedCategory && (
            <CategoryForm
              initialData={selectedCategory}
              onSuccess={() => {
                setIsEditDialogOpen(false);
                refetch();
              }}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent className="w-[95vw] sm:w-[425px] md:w-[500px]">
          <AlertDialogHeader>
            <AlertDialogTitle className="text-lg sm:text-xl md:text-2xl">Are you sure?</AlertDialogTitle>
            <AlertDialogDescription className="text-sm md:text-base">
              This action cannot be undone. This will permanently delete the category.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter className="flex-col sm:flex-row gap-2 sm:gap-0">
            <AlertDialogCancel className="w-full sm:w-auto mt-0">Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDeleteConfirm}
              className="w-full sm:w-auto bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
} 