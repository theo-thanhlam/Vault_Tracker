"use client";

import { useState } from "react";
import { useMutation, useQuery } from "@apollo/client";
import { toast } from "sonner";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
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
import { Checkbox } from "@/components/ui/checkbox";
import { CategoryForm } from "./category-form";
import { CategoryTableRow } from "./category-table-row";
import { GET_CATEGORY_TREE } from "@/lib/graphql/category/gql";
import { DELETE_CATEGORY_MUTATION } from "@/lib/graphql/category/gql";
import { Category } from "@/types/category";
import CategoryTableHeader from "./category-table-header";

interface CategoryTableProps {
  initialCategories?: Category[];
}

const DEFAULT_PAGE_SIZE = 10;

export function CategoryTable(props: CategoryTableProps) {
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(null);
  const [selectedRows, setSelectedRows] = useState<string[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(DEFAULT_PAGE_SIZE);

  const { data, loading, refetch } = useQuery(GET_CATEGORY_TREE, {
    fetchPolicy: "network-only",
  });

  const [deleteCategory] = useMutation(DELETE_CATEGORY_MUTATION, {
    onCompleted: () => {
      toast.success("Category deleted successfully");
      setIsDeleteDialogOpen(false);
      refetch();
    },
    onError: (error) => {
      toast.error(error.message || "Failed to delete category");
    },
  });

  const categories = data?.category?.getAllCategories?.treeViews || [];
  const totalCount = categories.length;
  const totalPages = Math.ceil(totalCount / pageSize);

  const toggleRow = (id: string) => {
    setSelectedRows((prev) =>
      prev.includes(id)
        ? prev.filter((rowId) => rowId !== id)
        : [...prev, id]
    );
  };

  const toggleAll = () => {
    if (selectedRows.length === categories.length) {
      setSelectedRows([]);
    } else {
      setSelectedRows(categories.map((c: Category) => c.id));
    }
  };

  const handleEdit = (category: Category) => {
    setSelectedCategory(category);
    setIsEditDialogOpen(true);
  };

  const handleDelete = (category: Category) => {
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

  const handleCategorySuccess = () => {
    setIsEditDialogOpen(false);
    refetch();
  };

 

  return (
    <div className="space-y-4">
      <CategoryTableHeader refetch={refetch} />

      <div className="rounded-md border">
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[50px]">
                 
                </TableHead>
                {/* Name */}
                <TableHead className="font-bold text-md md:text-lg lg:text-xl">Name</TableHead>
                {/* Type */}
                <TableHead className="font-bold text-md md:text-lg lg:text-xl hidden md:table-cell ">Type</TableHead>
                {/* Description */}
                <TableHead className="font-bold text-md md:text-lg lg:text-xl hidden xl:table-cell ">Description</TableHead>
                {/* Extra Actions */}
                <TableHead className="w-[50px]"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center">
                    Loading...
                  </TableCell>
                </TableRow>
              ) : categories.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center">
                    No categories found.
                  </TableCell>
                </TableRow>
              ) : (
                categories.map((category: Category) => (
                  <CategoryTableRow
                    key={category.id}
                    category={category}
                    isSelected={selectedRows.includes(category.id)}
                    onSelect={toggleRow}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                  />
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </div>

      {/* Edit Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Edit Category</DialogTitle>
            <DialogDescription>
              Update category details.
            </DialogDescription>
          </DialogHeader>
          {selectedCategory && (
            <CategoryForm
              initialData={selectedCategory}
              onSuccess={handleCategorySuccess}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete the category and all its subcategories.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDeleteConfirm}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
} 