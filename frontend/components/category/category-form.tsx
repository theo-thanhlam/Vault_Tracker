"use client";

import { useState, useMemo, useEffect } from "react";
import { useMutation, useQuery } from "@apollo/client";
import { motion } from "framer-motion";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { toast } from "sonner";
import { ChevronRight, FolderTree } from "lucide-react";

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
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Badge } from "@/components/ui/badge";
import { CREATE_CATEGORY_MUTATION, UPDATE_CATEGORY_MUTATION } from "@/lib/graphql/category/gql";
import { GET_CATEGORIES_QUERY } from "@/lib/graphql/category/queries";
import { CategoryTypeEnum, Category } from "@/types/category";

// Helper type for category with children
type CategoryWithChildren = Category & { children: CategoryWithChildren[] };

// Constants for category levels
const MAX_CATEGORY_LEVEL = 3; // Maximum allowed nesting level

// Base form schema without validation
const baseFormSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  type: z.nativeEnum(CategoryTypeEnum),
  description: z.string().min(2, "Description must be at least 2 characters"),
  parentId: z.string().optional(),
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

// Helper component to render level indicator
function LevelIndicator({ level }: { level: number }) {
  if (level === 0) return null;
  
  return (
    <TooltipProvider>
      <Tooltip>
        {/* <TooltipTrigger asChild>
          <span className="text-xs text-muted-foreground ml-1">
            ({level})
          </span>
        </TooltipTrigger> */}
        <TooltipContent>
          <p>Subcategory Level {level}</p>
          <p className="text-xs text-muted-foreground mt-1">
            {level === MAX_CATEGORY_LEVEL
              ? "Maximum nesting level reached"
              : `Can create subcategories up to level ${MAX_CATEGORY_LEVEL}`}
          </p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}

// Helper function to build category hierarchy
function buildCategoryHierarchy(categories: Category[]): CategoryWithChildren[] {
  const categoryMap = new Map<string, CategoryWithChildren>();
  const rootCategories: CategoryWithChildren[] = [];

  // First pass: create map of all categories with empty children arrays
  categories.forEach(category => {
    categoryMap.set(category.id, { ...category, children: [] });
  });

  // Second pass: build hierarchy
  categories.forEach(category => {
    const categoryWithChildren = categoryMap.get(category.id)!;
    if (category.parentId && categoryMap.has(category.parentId)) {
      const parent = categoryMap.get(category.parentId)!;
      parent.children.push(categoryWithChildren);
    } else {
      rootCategories.push(categoryWithChildren);
    }
  });

  return rootCategories;
}

// Helper function to calculate category levels with validation
function calculateCategoryLevels(categories: Category[]): {
  levels: Map<string, number>;
  hasInvalidLevels: boolean;
} {
  const levels = new Map<string, number>();
  const categoryMap = new Map<string, Category>();
  let hasInvalidLevels = false;
  
  // First, create a map of all categories for easy lookup
  categories.forEach(category => {
    categoryMap.set(category.id, category);
    levels.set(category.id, 0);
  });

  // Then, calculate the actual level for each category
  categories.forEach(category => {
    let currentCategory = category;
    let level = 0;
    const visited = new Set<string>(); // To detect cycles
    
    // Traverse up the parent chain until we reach a root category
    while (currentCategory.parentId && categoryMap.has(currentCategory.parentId)) {
      // Check for cycles
      if (visited.has(currentCategory.id)) {
        console.error(`Cycle detected in category hierarchy: ${currentCategory.id}`);
        hasInvalidLevels = true;
        break;
      }
      
      visited.add(currentCategory.id);
      level++;
      
      // Check if level exceeds maximum
      if (level > MAX_CATEGORY_LEVEL) {
        console.error(`Category ${currentCategory.id} exceeds maximum level of ${MAX_CATEGORY_LEVEL}`);
        hasInvalidLevels = true;
        break;
      }
      
      currentCategory = categoryMap.get(currentCategory.parentId)!;
    }
    
    levels.set(category.id, level);
  });

  return { levels, hasInvalidLevels };
}

// Helper component to render category hierarchy in select
function CategoryOption({ 
  category, 
  level = 0,
  categoryLevels,
  onSelect
}: { 
  category: CategoryWithChildren, 
  level?: number,
  categoryLevels: Map<string, number>,
  onSelect?: (category: CategoryWithChildren) => void
}) {
  const actualLevel = categoryLevels.get(category.id) || 0;
  const isMaxLevel = actualLevel >= MAX_CATEGORY_LEVEL;
  const indentSize = 12; // pixels of indentation per level
  
  return (
    <>
      <SelectItem 
        value={category.id}
        disabled={isMaxLevel}
        onSelect={() => onSelect?.(category)}
      >
        <div className="flex items-center">
          <div style={{ marginLeft: `${actualLevel * indentSize}px` }}>
            <span className={isMaxLevel ? "text-muted-foreground" : ""} >
              {category.name}
            </span>
            {/* <LevelIndicator level={actualLevel} /> */}
          </div>
        </div>
      </SelectItem>
      {category.children.map((child) => (
        <CategoryOption 
          key={child.id} 
          category={child} 
          level={level + 1} 
          categoryLevels={categoryLevels}
          onSelect={onSelect}
        />
      ))}
    </>
  );
}

// Add a constant for the top-level category value
const TOP_LEVEL_CATEGORY_VALUE = "TOP_LEVEL";

export function CategoryForm({ initialData, onSuccess }: CategoryFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // Fetch existing categories for parent selection
  const { data: categoriesData } = useQuery(GET_CATEGORIES_QUERY);
  const categories = categoriesData?.category?.getCategory?.values || [];
  
  // Create form schema with validation
  const formSchema = useMemo(() => 
    baseFormSchema.refine((data) => {
      // Additional validation to ensure parent category type matches
      if (data.parentId && data.type) {
        const parentCategory = categories.find((cat: Category) => cat.id === data.parentId);
        if (parentCategory && parentCategory.type !== data.type) {
          return false;
        }
      }
      return true;
    }, {
      message: "Subcategory type must match parent category type",
      path: ["type"],
    }),
    [categories]
  );
  
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: initialData || {
      name: "",
      type: CategoryTypeEnum.EXPENSE,
      description: "",
      parentId: undefined,
    },
  });

  // Build category hierarchy
  const categoryHierarchy = useMemo(() => buildCategoryHierarchy(categories), [categories]);

  // Calculate category levels
  const { levels: categoryLevels, hasInvalidLevels } = useMemo(
    () => calculateCategoryLevels(categories),
    [categories]
  );

  // Show warning if there are invalid levels
  useEffect(() => {
    if (hasInvalidLevels) {
      toast.warning(
        `Some categories exceed the maximum nesting level of ${MAX_CATEGORY_LEVEL}. Please reorganize your categories.`
      );
    }
  }, [hasInvalidLevels]);

  // Get selected parent category for type validation
  const selectedParentId = form.watch("parentId");
  const selectedParent = useMemo(() => 
    categories.find((cat: Category) => cat.id === selectedParentId),
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
                  <Input placeholder="Category name" {...field} />
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
                  onValueChange={(value) => {
                    field.onChange(value);
                    // Clear parent if type doesn't match
                    if (selectedParent && selectedParent.type !== value) {
                      form.setValue("parentId", undefined);
                    }
                  }}
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
                    Type is locked to match parent category type ({selectedParent.type})
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
              <FormItem>
                <div className="flex items-center gap-2">
                  <FormLabel>Parent Category</FormLabel>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <span className="cursor-help">
                          <FolderTree className="h-4 w-4 text-muted-foreground" />
                        </span>
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>Select a parent category to create a hierarchy</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          Subcategories must match their parent's type
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
                <Select
                  onValueChange={(value) => {
                    // Convert TOP_LEVEL_CATEGORY_VALUE to undefined for the form
                    field.onChange(value === TOP_LEVEL_CATEGORY_VALUE ? undefined : value);
                    // Update type to match parent if selected
                    if (value && value !== TOP_LEVEL_CATEGORY_VALUE) {
                      const parent = categories.find((cat: Category) => cat.id === value);
                      if (parent) {
                        const parentLevel = categoryLevels.get(parent.id) || 0;
                        if (parentLevel >= MAX_CATEGORY_LEVEL) {
                          toast.error(`Cannot create subcategories at level ${MAX_CATEGORY_LEVEL}`);
                          field.onChange(undefined);
                          return;
                        }
                        form.setValue("type", parent.type);
                      }
                    }
                  }}
                  defaultValue={field.value || TOP_LEVEL_CATEGORY_VALUE}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select a parent category (optional)" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value={TOP_LEVEL_CATEGORY_VALUE}>
                      <div className="flex items-center gap-2">
                        None
                        <LevelIndicator level={0} />
                      </div>
                    </SelectItem>
                    {categoryHierarchy.map((category) => (
                      <CategoryOption 
                        key={category.id} 
                        category={category} 
                        categoryLevels={categoryLevels}
                        onSelect={(selectedCategory) => {
                          const level = categoryLevels.get(selectedCategory.id) || 0;
                          if (level >= MAX_CATEGORY_LEVEL) {
                            toast.error(`Cannot create subcategories at level ${MAX_CATEGORY_LEVEL}`);
                          }
                        }}
                      />
                    ))}
                  </SelectContent>
                </Select>
                <FormDescription>
                  {selectedParent 
                    ? `Creating a subcategory under "${selectedParent.name}" (Level ${categoryLevels.get(selectedParent.id) || 0})`
                    : "Optional: Select a parent category to create a subcategory"}
                  {hasInvalidLevels && (
                    <span className="text-destructive block mt-1">
                      Some categories exceed the maximum nesting level of {MAX_CATEGORY_LEVEL}
                    </span>
                  )}
                </FormDescription>
                <FormMessage />
              </FormItem>
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
            ) : (
              initialData ? "Update Category" : "Create Category"
            )}
          </Button>
        </form>
      </Form>
    </motion.div>
  );
} 