"use client";

import { MoreHorizontal, Pencil, Trash2, Eye, ChevronRight } from "lucide-react";
import { TableCell, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Category } from "@/types/category";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { format } from "date-fns";
import CategoryDetail from "./category-detail";

interface CategoryTableRowProps {
  category: Category;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onEdit?: (category: Category) => void;
  onDelete?: (category: Category) => void;
  level?: number;
}

export function CategoryTableRow({
  category,
  isSelected,
  onSelect,
  onEdit,
  onDelete,
  level = 0,
}: CategoryTableRowProps) {
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);
  const indentSize = Math.min(level * 8, 48); // Maximum indent of 48px (4 levels)
  const hasChildren = category.children && category.children.length > 0;
  

  const handleChevronClick = () => {
    if (hasChildren) {
      setIsExpanded(!isExpanded);
    }
    onSelect(category.id);
  };

  

  return (
    <>
      <TableRow>
        <TableCell className="w-[50px]">
          {hasChildren && (
            <Button
            variant="ghost"
            size="icon"
            className={cn(
              "h-6 w-6 p-0 hover:bg-transparent",
              isSelected && "text-primary"
            )}
            onClick={handleChevronClick}
          >
            <ChevronRight
              className={cn(
                "h-4 w-4 transition-transform duration-200",
                isExpanded && hasChildren && "rotate-90",
                !hasChildren && "opacity-50"
              )}
            />
          </Button>
          )}
          
        </TableCell>
        <TableCell className="font-medium">
          <div 
            className="flex flex-col sm:flex-row sm:items-center gap-1"
            style={{ paddingLeft: `${indentSize}px` }}
          >
            <span>{category.name}</span>
            <span className="text-sm text-muted-foreground sm:hidden">
              {category.type}
            </span>
            
          </div>
        </TableCell>
        <TableCell className="hidden uppercase md:table-cell">{(level === 0) ? category.type : null}</TableCell>
        <TableCell className="hidden text-muted-foreground hidden xl:table-cell text-xs">
          {category.description || "No description"}
        </TableCell>
        <TableCell className="text-right hidden md:table-cell">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-end gap-1">
            <span className="text-sm text-muted-foreground sm:hidden">
              {category.description || "No description"}
            </span>
          </div>
        </TableCell>
        <TableCell className="w-[50px]">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <span className="sr-only">Open menu</span>
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => setIsDetailsOpen(true)}>
                <Eye className="mr-2 h-4 w-4" />
                View Details
              </DropdownMenuItem>
              {onEdit && (
                <DropdownMenuItem onClick={() => onEdit(category)}>
                  <Pencil className="mr-2 h-4 w-4" />
                  Edit
                </DropdownMenuItem>
              )}
              {onDelete && (
                <DropdownMenuItem
                  onClick={() => onDelete(category)}
                  className="text-destructive"
                >
                  <Trash2 className="mr-2 h-4 w-4" />
                  Delete
                </DropdownMenuItem>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        </TableCell>
      </TableRow>

      {/* Render children recursively if expanded */}
      {isExpanded && category.children?.map((child) => (
        <CategoryTableRow
          key={child.id}
          category={child}
          isSelected={isSelected}
          onSelect={onSelect}
          onEdit={onEdit}
          onDelete={onDelete}
          level={level + 1}
        />
      ))}

      <Dialog open={isDetailsOpen} onOpenChange={setIsDetailsOpen}>
        <CategoryDetail category={category} />
      </Dialog>
    </>
  );
} 