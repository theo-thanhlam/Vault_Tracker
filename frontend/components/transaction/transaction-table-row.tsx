"use client";

import { formatDistanceToNow, format } from "date-fns";
import { MoreHorizontal, Pencil, Trash2, Eye } from "lucide-react";
import { Checkbox } from "@/components/ui/checkbox";
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
import { Transaction } from "@/types/transaction";
import { useState } from "react";
import TransactionDetail from "./transaction-detail";

interface TransactionTableRowProps {
  transaction: Transaction;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onEdit?: (transaction: Transaction) => void;
  onDelete?: (transaction: Transaction) => void;
}

export function TransactionTableRow({
  transaction,
  isSelected,
  onSelect,
  onEdit,
  onDelete,
}: TransactionTableRowProps) {
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const amount_display =
    transaction.categoryType === "expense"
      ? `- \$${transaction.amount.toFixed(2)}`
      : `\$${transaction.amount.toFixed(2)}`;
  const date_display = format(new Date(transaction.date), "LLL do yyyy HH:mm:ss");
  return (
    <>
      <TableRow>
        <TableCell className="hidden sm:table-cell">
          <Checkbox
            checked={isSelected}
            onCheckedChange={() => onSelect(transaction.id)}
            aria-label={`Select ${transaction.description}`}
          />
        </TableCell>
        <TableCell className="font-medium">
          <div className="flex flex-col sm:flex-row sm:items-center gap-1">
            <span>{transaction.categoryName}</span>
            <span className="text-sm text-muted-foreground sm:hidden">
              {date_display}
            </span>
          </div>
        </TableCell>
        <TableCell className="hidden uppercase md:table-cell">{transaction.categoryType}</TableCell>
        <TableCell className="hidden sm:table-cell text-muted-foreground">
          {date_display}
        </TableCell>
        <TableCell className="text-right">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-end gap-1">
            <span>{amount_display}</span>
            <span className="text-sm text-muted-foreground sm:hidden uppercase">
              {transaction.categoryType}
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
                <DropdownMenuItem onClick={() => onEdit(transaction)}>
                  <Pencil className="mr-2 h-4 w-4" />
                  Edit
                </DropdownMenuItem>
              )}
              {onDelete && (
                <DropdownMenuItem
                  onClick={() => onDelete(transaction)}
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

      <Dialog open={isDetailsOpen} onOpenChange={setIsDetailsOpen}>
        <TransactionDetail transaction={transaction} />
      </Dialog>
    </>
  );
} 