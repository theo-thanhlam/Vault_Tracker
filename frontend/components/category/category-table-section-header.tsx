"use client";

import { CategoryForm } from "./category-form";
import { useState } from "react";
import TableSectionHeader from "../form-components/table-section-header";

interface CategoryTableSectionHeaderProps {
  refetch: () => void;
}

export default function CategoryTableSectionHeader({ refetch }: CategoryTableSectionHeaderProps) {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  return (
 
    <TableSectionHeader
      title="Categories"
      action_title="Add Category"
      formTitle="Create Category"
      formDescription="Add a new category to your account."
      open={isCreateDialogOpen}
      onOpenChange={setIsCreateDialogOpen}
      onSuccess={() => {
        setIsCreateDialogOpen(false);
        refetch();
      }}
      formComponent={
        <CategoryForm
          onSuccess={() => {
            setIsCreateDialogOpen(false);
            refetch();
          }}
        />
      }
    />
  );
} 