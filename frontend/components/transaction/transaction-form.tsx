"use client";

import { useState, useMemo } from "react";
import { useMutation, useQuery } from "@apollo/client";
import { motion } from "framer-motion";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { toast } from "sonner";
import { format } from "date-fns";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
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
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { CalendarIcon } from "lucide-react";
import {
  CREATE_TRANSACTION_MUTATION,
  UPDATE_TRANSACTION_MUTATION,
} from "@/lib/graphql/transaction/mutations";
import { GET_CATEGORIES_QUERY, GET_CATEGORY_TREE } from "@/lib/graphql/category/gql";
import { Category } from "@/types/category";
import { Transaction } from "@/types/transaction";
import { CategorySelect } from "../category/category-select";

const formSchema = z.object({
  amount: z.number().min(0.01, "Amount must be greater than 0"),
  description: z.string().min(2, "Description must be at least 2 characters"),
  categoryId: z.string().uuid("Please select a valid category"),
  date: z.date().optional(),
});

type FormValues = z.infer<typeof formSchema>;

interface TransactionFormProps {
  initialData?: Transaction;
  onSuccess?: () => void;
}



export function TransactionForm({
  initialData,
  onSuccess,
}: TransactionFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Fetch categories for the dropdown
  const { data: categoriesData } = useQuery(GET_CATEGORY_TREE);
  const categories = categoriesData?.category?.getAllCategories?.treeViews || [];

  // Build category hierarchy and calculate levels
  

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: initialData
      ? {
          amount: initialData.amount,
          description: initialData.description || "",
          categoryId: initialData.categoryId,
          date: new Date(initialData.date),
        }
      : {
          amount: 0,
          description: "",
          categoryId: "",
          date: new Date(),
        },
  });

  const [createTransaction] = useMutation(CREATE_TRANSACTION_MUTATION, {
    onCompleted: (data) => {
      toast.success("Transaction created successfully");
      form.reset();
      onSuccess?.();
    },
    onError: (error) => {
      toast.error("Failed to create transaction");
      console.log(error.message);
    },
  });

  const [updateTransaction] = useMutation(UPDATE_TRANSACTION_MUTATION, {
    onCompleted: (data) => {
      toast.success("Transaction updated successfully");
      onSuccess?.();
    },
    onError: (error) => {
      toast.error(error.message || "Failed to update transaction");
    },
  });

  const onSubmit = async (values: FormValues) => {
    setIsSubmitting(true);
    try {
      if (initialData) {
        await updateTransaction({
          variables: {
            input: {
              id: initialData.id,
              ...values,
              amount: parseFloat(values.amount.toString()),
            },
          },
        });
      } else {
        await createTransaction({
          variables: {
            input: {
              ...values,
              amount: parseFloat(values.amount.toString()),
            },
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
            name="amount"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Amount</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    step="0.01"
                    placeholder="0.00"
                    {...field}
                    onChange={(e) => field.onChange(parseFloat(e.target.value))}
                    value={field.value}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="categoryId"
            render={({ field }) => (
              <CategorySelect
                categories={categories}
                value={field.value || undefined}
                onChange={(value) => field.onChange(value || null)}
              />
            )}
          />

          <FormField
            control={form.control}
            name="date"
            render={({ field }) => (
              <FormItem className="flex flex-col">
                <FormLabel>Date</FormLabel>
                <Popover>
                  <PopoverTrigger asChild>
                    <FormControl>
                      <Button
                        variant={"outline"}
                        className={cn(
                          "w-full pl-3 text-left font-normal",
                          !field.value && "text-muted-foreground"
                        )}
                      >
                        {field.value ? (
                          format(field.value, "PPP")
                        ) : (
                          <span>Pick a date</span>
                        )}
                        <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                      </Button>
                    </FormControl>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                      mode="single"
                      selected={field.value}
                      onSelect={field.onChange}
                      disabled={(date) =>
                        date > new Date() || date < new Date("1900-01-01")
                      }
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
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
                    placeholder="Transaction description"
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
              "Update Transaction"
            ) : (
              "Create Transaction"
            )}
          </Button>
        </form>
      </Form>
    </motion.div>
  );
}
