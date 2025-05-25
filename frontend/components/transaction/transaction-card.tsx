"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { format } from "date-fns";
import {
  MoreHorizontal,
  Pencil,
  Trash,
  Calendar,
  DollarSign,
  Tag,
  FileText,
} from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { Transaction } from "@/types/transaction";

interface TransactionCardProps {
  transaction: Transaction;
  onEdit?: (transaction: Transaction) => void;
  onDelete?: (transaction: Transaction) => void;
}

export function TransactionCard({
  transaction,
  onEdit,
  onDelete,
}: TransactionCardProps) {
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);

  const amount_display =
    transaction.categoryType === "expense"
      ? `- \$${transaction.amount.toFixed(2)}`
      : `\$${transaction.amount.toFixed(2)}`;

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.2 }}
      >
        <Card
          className="cursor-pointer hover:bg-accent/50 transition-colors"
          onClick={() => setIsDetailsOpen(true)}
        >
          <CardContent className="px-4 py-3">
            <div className="flex justify-between items-start flex-col md:flex-row">
              <div className="flex-1">
                <h3 className="font-medium text-md md:text-lg lg:text-xl">
                  {transaction.description}
                </h3>
                <p className="text-sm text-muted-foreground mt-1 hidden md:block">
                  {format(new Date(transaction.date), "PPP")}
                </p>
              </div>
              <div
                className="flex items-center gap-2 w-full md:w-auto justify-between md:justify-end"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="text-right">
                  <p className="font-medium text-md md:text-lg lg:text-xl">
                    {amount_display}
                  </p>
                  <p className="text-sm text-muted-foreground hidden md:block">
                    {transaction.categoryName}
                  </p>
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 ml-auto md:ml-0"
                    >
                      <MoreHorizontal className="h-4 w-4" />
                      <span className="sr-only">Open menu</span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    {onEdit && (
                      <DropdownMenuItem
                        onClick={(e) => {
                          e.stopPropagation();
                          onEdit(transaction);
                        }}
                      >
                        <Pencil className="h-4 w-4 mr-2" />
                        Edit
                      </DropdownMenuItem>
                    )}
                    {onDelete && (
                      <DropdownMenuItem
                        onClick={(e) => {
                          e.stopPropagation();
                          onDelete(transaction);
                        }}
                        className="text-destructive focus:text-destructive"
                      >
                        <Trash className="h-4 w-4 mr-2" />
                        Delete
                      </DropdownMenuItem>
                    )}
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      <Dialog open={isDetailsOpen} onOpenChange={setIsDetailsOpen}>
        <DialogContent className="w-[95vw] sm:w-[425px] md:w-[600px] lg:w-[800px] max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-lg sm:text-xl md:text-2xl">
              Transaction Details
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="flex items-center gap-2">
              <DollarSign className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Amount</p>
                <p className="text-md md:text-lg font-bold">{amount_display}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Tag className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Transaction Type</p>
                <p className="text-md md:text-lg font-bold uppercase">
                  {transaction.categoryType}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <FileText className="h-4 w-4 text-muted-foreground" />
              <div className="flex-1">
                <p className="text-sm font-medium">Description</p>
                <p className="text-sm md:text-base text-muted-foreground">
                  {transaction.description}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Date</p>
                <p className="text-sm md:text-base text-muted-foreground">
                  {format(new Date(transaction.date), "PPP")}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Tag className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Category</p>
                <p className="text-sm md:text-base text-muted-foreground">
                  {transaction.categoryName}
                </p>
              </div>
            </div>

            <div className="pt-4 border-t">
              <p className="text-xs text-muted-foreground">
                Transaction ID: {transaction.id}
              </p>
              <p className="text-xs text-muted-foreground">
                Created: {format(new Date(transaction.createdAt), "PPP")}
              </p>
              {transaction.updatedAt && (
                <p className="text-xs text-muted-foreground">
                  Last Updated: {format(new Date(transaction.updatedAt), "PPP")}
                </p>
              )}
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}
