"use client";

import { useState, useMemo } from "react";
import { useMutation, useQuery } from "@apollo/client";
import { motion } from "framer-motion";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormDescription,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import {
  CREATE_CATEGORY_MUTATION,
  GET_CATEGORY_TREE,
  UPDATE_CATEGORY_MUTATION,
} from "@/lib/graphql/category/gql";
import { GET_CATEGORIES_QUERY } from "@/lib/graphql/category/gql";
import { CategoryTypeEnum, Category } from "@/types/category";
import { CategorySelect } from "./category-select";

// Base form schema without validation
const baseFormSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  type: z.nativeEnum(CategoryTypeEnum),
  description: z.string().min(2, "Description must be at least 2 characters"),
  parentId: z.string().optional().nullable(),
});

type FormValues = z.infer<typeof baseFormSchema>;

interface CategoryFormProps {
  initialData?: {
    id: string;
    name: string;
    type: CategoryTypeEnum;
    description: string;
    parentId?: string;
  };
  onSuccess?: () => void;
}

export function CategoryForm({ initialData, onSuccess }: CategoryFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Fetch existing categories for parent selection
  const { data: categoriesData } = useQuery(GET_CATEGORY_TREE);
  const categories = categoriesData?.category?.getAllCategories?.treeViews || [];

  
  // Create form schema with validation
  const formSchema = useMemo(
    () =>
      baseFormSchema.refine(
        (data) => {
          // Additional validation to ensure parent category type matches
          if (data.parentId && data.type) {
            const parentCategory = categories.find(
              (cat: Category) => cat.id === data.parentId
            );
            if (parentCategory && parentCategory.type !== data.type) {
              return false;
            }
          }
          return true;
        },
        {
          message: "Subcategory type must match parent category type",
          path: ["type"],
        }
      ),
    [categories]
  );

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: initialData
      ? {
          name: initialData.name,
          type: initialData.type,
          description: initialData.description || "",
          parentId: initialData.parentId || null,
        }
      : {
          name: "",
          type: CategoryTypeEnum.EXPENSE,
          description: "",
          parentId: null,
        },
  });

  // Get selected parent category for type validation
  const selectedParentId = form.watch("parentId");
  const selectedParent = useMemo(
    () => categories.find((cat: Category) => cat.id === selectedParentId),
    [categories, selectedParentId]
  );

  const [createCategory] = useMutation(CREATE_CATEGORY_MUTATION, {
    onCompleted: (data) => {
      toast.success("Category created successfully");
      form.reset();
      onSuccess?.();
    },
    onError: (error) => {
      toast.error(error.message || "Failed to create category");
    },
  });

  const [updateCategory] = useMutation(UPDATE_CATEGORY_MUTATION, {
    onCompleted: (data) => {
      toast.success("Category updated successfully");
      onSuccess?.();
    },
    onError: (error) => {
      toast.error(error.message || "Failed to update category");
    },
  });

  const onSubmit = async (values: FormValues) => {
    setIsSubmitting(true);
    try {
      if (initialData) {
        await updateCategory({
          variables: {
            input: {
              id: initialData.id,
              ...values,
            },
          },
        });
      } else {
        await createCategory({
          variables: {
            input: values,
          },
        });
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <FormField
            control={form.control}
            name="name"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Name</FormLabel>
                <FormControl>
                  <Input
                    placeholder="Category name"
                    {...field}
                    value={field.value}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="type"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Type</FormLabel>
                <Select
                  onValueChange={field.onChange}
                  value={field.value}
                  defaultValue={field.value}
                  disabled={!!selectedParent}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select a type" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {Object.values(CategoryTypeEnum).map((type) => (
                      <SelectItem key={type} value={type}>
                        {type}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {selectedParent && (
                  <FormDescription>
                    Type is locked to match parent category type (
                    {selectedParent.type})
                  </FormDescription>
                )}
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="parentId"
            render={({ field }) => (
              <CategorySelect
                categories={categories}
                value={field.value || undefined}
                onChange={(value) => field.onChange(value || null)}
                onTypeChange={(type) => form.setValue("type", type)}
                selectedParent={selectedParent}
              />
            )}
          />

          <FormField
            control={form.control}
            name="description"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Description</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="Category description"
                    className="resize-none"
                    {...field}
                    value={field.value}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <Button type="submit" className="w-full" disabled={isSubmitting}>
            {isSubmitting ? (
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                {initialData ? "Updating..." : "Creating..."}
              </div>
            ) : initialData ? (
              "Update Category"
            ) : (
              "Create Category"
            )}
          </Button>
        </form>
      </Form>
    </motion.div>
  );
}
