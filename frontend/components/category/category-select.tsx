import { useMemo } from "react";
import { toast } from "sonner";
import { FolderTree } from "lucide-react";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  FormControl,
  FormDescription,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Category, CategoryTypeEnum } from "@/types/category";

// Constants
const MAX_CATEGORY_LEVEL = 3;
const TOP_LEVEL_CATEGORY_VALUE = "TOP_LEVEL";

// Helper type for category with children
type CategoryWithChildren = Category & { children: CategoryWithChildren[] | [] }; 

// Helper function to convert Category to CategoryWithChildren
function convertToCategoryWithChildren(
  category: Category
): CategoryWithChildren {
  return {
    ...category,
    children: category.children ? category.children.map(convertToCategoryWithChildren) : [],
  };
}

// Helper function to build category hierarchy
function buildCategoryHierarchy(
  categories: Category[]
): CategoryWithChildren[] {
  // The API already provides the tree structure, so we just need to convert it
  return categories.map(convertToCategoryWithChildren);
}

// Helper function to calculate category levels with validation
function calculateCategoryLevels(categories: Category[]): {
  levels: Map<string, number>;
  hasInvalidLevels: boolean;
} {
  const levels = new Map<string, number>();
  let hasInvalidLevels = false;

  // Recursive function to calculate levels
  function calculateLevel(category: Category, currentLevel: number) {
    levels.set(category.id, currentLevel);

    if (currentLevel > MAX_CATEGORY_LEVEL) {
      console.error(
        `Category ${category.id} exceeds maximum level of ${MAX_CATEGORY_LEVEL}`
      );
      hasInvalidLevels = true;
    }

    // Process children if they exist
    if (category.children) {
      category.children.forEach((child) => {
        calculateLevel(child, currentLevel + 1);
      });
    }
  }

  // Start with root categories at level 0
  categories.forEach((category) => {
    calculateLevel(category, 0);
  });

  return { levels, hasInvalidLevels };
}

// Helper component to render level indicator
function LevelIndicator({ level }: { level: number }) {
  if (level === 0) return null;

  return (
    <TooltipProvider>
      <Tooltip>
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

// Helper component to render category hierarchy in select
function CategoryOption({
  category,
  level = 0,
  categoryLevels,
  onSelect,
}: {
  category: CategoryWithChildren;
  level?: number;
  categoryLevels: Map<string, number>;
  onSelect?: (category: CategoryWithChildren) => void;
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
            <span className={isMaxLevel ? "text-muted-foreground" : ""}>
              {category.name}
            </span>
          </div>
        </div>
      </SelectItem>
      {category.children.map((child) => (
        <CategoryOption
          key={child.id}
          category={child as CategoryWithChildren}
          level={level + 1}
          categoryLevels={categoryLevels}
          onSelect={onSelect}
        />
      ))}
    </>
  );
}

interface CategorySelectProps {
  categories: Category[];
  value: string | undefined;
  onChange: (value: string | undefined) => void;
  onTypeChange?: (type: CategoryTypeEnum) => void;
  selectedParent?: Category | null;
  hasInvalidLevels?: boolean;
}

export function CategorySelect({
  categories,
  value,
  onChange,
  onTypeChange,
  selectedParent,
  hasInvalidLevels,
}: CategorySelectProps) {
  // Build category hierarchy
  const categoryHierarchy = useMemo(
    () => buildCategoryHierarchy(categories),
    [categories]
  );

  // Calculate category levels
  const { levels: categoryLevels } = useMemo(
    () => calculateCategoryLevels(categories),
    [categories]
  );

  return (
    <FormItem>
      <div className="flex items-center gap-2">
        <FormLabel>Category</FormLabel>
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
        onValueChange={(newValue) => {
          // Convert TOP_LEVEL_CATEGORY_VALUE to undefined for the form
          const finalValue =
            newValue === TOP_LEVEL_CATEGORY_VALUE ? undefined : newValue;
          onChange(finalValue);

          // Update type to match parent if selected
          if (newValue && newValue !== TOP_LEVEL_CATEGORY_VALUE) {
            const parent = categories.find((cat) => cat.id === newValue);
            if (parent) {
              const parentLevel = categoryLevels.get(parent.id) || 0;
              if (parentLevel >= MAX_CATEGORY_LEVEL) {
                toast.error(
                  `Cannot create subcategories at level ${MAX_CATEGORY_LEVEL}`
                );
                onChange(undefined);
                return;
              }
              onTypeChange?.(parent.type);
            }
          }
        }}
        value={value || TOP_LEVEL_CATEGORY_VALUE}
        defaultValue={value || TOP_LEVEL_CATEGORY_VALUE}
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
                  toast.error(
                    `Cannot create subcategories at level ${MAX_CATEGORY_LEVEL}`
                  );
                }
              }}
            />
          ))}
        </SelectContent>
      </Select>
      <FormDescription>
        {selectedParent
          ? `Creating a subcategory under "${selectedParent.name}" (Level ${
              categoryLevels.get(selectedParent.id) || 0
            })`
          : null}
        {hasInvalidLevels && (
          <span className="text-destructive block mt-1">
            Some categories exceed the maximum nesting level of{" "}
            {MAX_CATEGORY_LEVEL}
          </span>
        )}
      </FormDescription>
      <FormMessage />
    </FormItem>
  );
}
