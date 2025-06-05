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
  const selectedCategories = categories.filter((category) =>
    value.includes(category.id)
  );

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
            {categories.map((category) => (
              <CommandItem
                key={category.id}
                onSelect={() => {
                  const newValue = value.includes(category.id)
                    ? value.filter((id) => id !== category.id)
                    : [...value, category.id];
                  onChange(newValue);
                }}
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
            ))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  );
} 