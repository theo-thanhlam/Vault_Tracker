import { Check } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Badge } from "@/components/ui/badge";
import { Category } from "@/types/category";

interface CategoryMultiSelectProps {
  categories: Category[];
  value: string[];
  onChange: (value: string[]) => void;
}

export function CategoryMultiSelect({
  categories,
  value,
  onChange,
}: CategoryMultiSelectProps) {
  // Helper function to find all selected categories including children
  const findSelectedCategories = (categories: Category[]): Category[] => {
    return categories.reduce((acc: Category[], category) => {
      if (value.includes(category.id)) {
        acc.push(category);
      }
      if (category.children) {
        acc.push(...findSelectedCategories(category.children));
      }
      return acc;
    }, []);
  };

  const selectedCategories = findSelectedCategories(categories);

  const renderCategoryItem = (category: Category, level: number = 0) => {
    return (
      <div key={category.id}>
        <CommandItem
          onSelect={() => {
            const newValue = value.includes(category.id)
              ? value.filter((id) => id !== category.id)
              : [...value, category.id];
            onChange(newValue);
          }}
          className="pl-4"
          style={{ paddingLeft: `${level * 20 + 16}px` }}
        >
          <div
            className={cn(
              "mr-2 flex h-4 w-4 items-center justify-center rounded-sm border border-primary",
              value.includes(category.id)
                ? "bg-primary text-primary-foreground"
                : "opacity-50 [&_svg]:invisible"
            )}
          >
            <Check className="h-4 w-4" />
          </div>
          {category.name}
        </CommandItem>
        {category.children?.map((child) => renderCategoryItem(child, level + 1))}
      </div>
    );
  };

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          className="w-full justify-between"
        >
          {selectedCategories.length > 0 ? (
            <div className="flex gap-1 flex-wrap">
              {selectedCategories.map((category) => (
                <Badge
                  variant="secondary"
                  key={category.id}
                  className="mr-1"
                >
                  {category.name}
                </Badge>
              ))}
            </div>
          ) : (
            "Select categories..."
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full p-0">
        <Command>
          <CommandInput placeholder="Search categories..." />
          <CommandEmpty>No categories found.</CommandEmpty>
          <CommandGroup>
            {categories.map((category) => renderCategoryItem(category))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  );
} 