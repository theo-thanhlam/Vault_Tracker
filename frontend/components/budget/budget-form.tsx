import { Budget } from '@/types/budget';
import React, { useState } from 'react'
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";
import { useMutation } from "@apollo/client";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormDescription,
} from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { CalendarIcon, Trash2 } from "lucide-react";
import { format } from "date-fns";
import { cn } from "@/lib/utils";
import { CategoryMultiSelect } from "@/components/category/category-multi-select";
import { useQuery } from "@apollo/client";
import { GET_CATEGORY_TREE } from "@/lib/graphql/category/gql";
import { CREATE_BUDGET_MUTATION, UPDATE_BUDGET_MUTATION, DELETE_BUDGET_MUTATION } from "@/lib/graphql/budget/gql";

enum BudgetType {
  FIXED = "FIXED",
  FLEXIBLE = "FLEXIBLE",
  ROLLING = "ROLLING",
  SAVINGS = "SAVINGS"
}

enum BudgetFrequency {
  DAILY = "DAILY",
  WEEKLY = "WEEKLY",
  BI_WEEKLY = "BI_WEEKLY",
  MONTHLY = "MONTHLY",
  YEARLY = "YEARLY",
  CUSTOM = "CUSTOM"
}

const formSchema = z.object({
  name: z.string().min(2, {
    message: "Name must be at least 2 characters.",
  }),
  description: z.string().min(2, {
    message: "Description must be at least 2 characters.",
  }),
  amount: z.string().refine((val) => !isNaN(Number(val)) && Number(val) > 0, {
    message: "Amount must be a positive number.",
  }),
  type: z.nativeEnum(BudgetType, {
    required_error: "Type is required.",
  }),
  frequency: z.nativeEnum(BudgetFrequency, {
    required_error: "Frequency is required.",
  }),
  startDate: z.date({
    required_error: "Start date is required.",
  }),
  endDate: z.date({
    required_error: "End date is required.",
  }),
  categories: z.array(z.string()).min(1, {
    message: "Please select at least one category.",
  }),
});

type FormValues = z.infer<typeof formSchema>;

interface BudgetFormProps {
  initialData?: Budget;
  onSuccess?: () => void;
}

const BudgetForm = ({ initialData, onSuccess }: BudgetFormProps) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [startDateOpen, setStartDateOpen] = useState(false);
  const [endDateOpen, setEndDateOpen] = useState(false);
  const { data: categoriesData } = useQuery(GET_CATEGORY_TREE);
  const categories = categoriesData?.category?.getAllCategories?.treeViews || [];

  const [createBudget] = useMutation(CREATE_BUDGET_MUTATION, {
    onCompleted: (data) => {
      toast.success("Budget created successfully");
      onSuccess?.();
    },
    onError: (error) => {
      toast.error(error.message || "Failed to create budget");
    },
  });

  const [updateBudget] = useMutation(UPDATE_BUDGET_MUTATION, {
    onCompleted: (data) => {
      toast.success("Budget updated successfully");
      onSuccess?.();
    },
    onError: (error) => {
      toast.error(error.message || "Failed to update budget");
    },
  });

  const [deleteBudget] = useMutation(DELETE_BUDGET_MUTATION, {
    onCompleted: (data) => {
      toast.success("Budget deleted successfully");
      onSuccess?.();
    },
    onError: (error) => {
      toast.error(error.message || "Failed to delete budget");
    },
  });

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: initialData
      ? {
          name: initialData.name,
          description: initialData.description,
          amount: initialData.amount.toString(),
          type: initialData.type as BudgetType,
          frequency: initialData.frequency as BudgetFrequency,
          startDate: initialData.startDate ? new Date(initialData.startDate) : new Date(),
          endDate: initialData.endDate ? new Date(initialData.endDate) : new Date(),
          categories: initialData.categories?.map(category => category.id) || [],
        }
      : {
          name: "",
          description: "",
          amount: "",
          type: BudgetType.FIXED,
          frequency: BudgetFrequency.MONTHLY,
          startDate: new Date(),
          endDate: new Date(),
          categories: [],
        },
  });

  // Watch frequency and start_date for automatic end date updates
  const frequency = form.watch("frequency");
  const startDate = form.watch("startDate");

  // Update end date when frequency or start date changes
  React.useEffect(() => {
    if (frequency && startDate && frequency !== BudgetFrequency.CUSTOM) {
      let endDate = new Date(startDate);
      
      switch (frequency) {
        case BudgetFrequency.DAILY:
          endDate.setDate(endDate.getDate() + 1);
          break;
        case BudgetFrequency.WEEKLY:
          endDate.setDate(endDate.getDate() + 7);
          break;
        case BudgetFrequency.BI_WEEKLY:
          endDate.setDate(endDate.getDate() + 14);
          break;
        case BudgetFrequency.MONTHLY:
          endDate.setMonth(endDate.getMonth() + 1);
          break;
        case BudgetFrequency.YEARLY:
          endDate.setFullYear(endDate.getFullYear() + 1);
          break;
      }
      
      form.setValue("endDate", endDate);
    }
  }, [frequency, startDate, form]);

  const onSubmit = async (values: FormValues) => {
    setIsSubmitting(true);
    try {
      const input = {
        name: values.name,
        description: values.description,
        amount: parseFloat(values.amount),
        type: values.type,
        frequency: values.frequency,
        startDate: values.startDate,
        endDate: values.endDate,
        categories: values.categories,
      };

      if (initialData) {
        await updateBudget({
          variables: {
            input: {
              id: initialData.id,
              ...input,
            },
          },
        });
      } else {
        await createBudget({
          variables: {
            input,
          },
        });
      }
    } catch (error) {
      // Error handling is done in the mutation hooks
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!initialData?.id) return;
    
    if (window.confirm("Are you sure you want to delete this budget?")) {
      setIsSubmitting(true);
      try {
        await deleteBudget({
          variables: {
            input: {
              id: initialData.id,
            },
          },
        });
      } catch (error) {
        // Error handling is done in the mutation hook
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="Enter budget name" {...field} />
              </FormControl>
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
                  placeholder="Enter budget description"
                  className="resize-none"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="amount"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Amount</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  placeholder="0.00"
                  step="0.01"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      <div className="grid grid-cols-2 gap-4">
        <FormField
          control={form.control}
          name="type"
          render={({ field }) => (
            <FormItem className="col-span-1">
              <FormLabel>Type</FormLabel>
              <Select
                onValueChange={field.onChange}
                value={field.value}
                defaultValue={field.value}
              >
                <FormControl className="w-full">
                  <SelectTrigger>
                    <SelectValue placeholder="Select a type" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                 {
                  Object.values(BudgetType).map((type) => (
                    <SelectItem key={type} value={type}>{type}</SelectItem>
                  ))
                 }
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="frequency"
          render={({ field }) => (
            <FormItem >
              <FormLabel>Frequency</FormLabel>
              <Select
                onValueChange={field.onChange}
                value={field.value}
                defaultValue={field.value}
              >
                <FormControl className="w-full">
                  <SelectTrigger>
                    <SelectValue placeholder="Select frequency" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {
                    Object.values(BudgetFrequency).map((frequency) => (
                      <SelectItem key={frequency} value={frequency}>{frequency}</SelectItem>
                    ))
                  }
                  
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="startDate"
            render={({ field }) => (
              <FormItem className="flex flex-col">
                <FormLabel>Start Date</FormLabel>
                <Popover open={startDateOpen} onOpenChange={setStartDateOpen}>
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
                      onSelect={(date) => {
                        field.onChange(date);
                        setStartDateOpen(false);
                      }}
                      disabled={(date) =>
                        date < new Date("1900-01-01") ||
                        date > new Date("2100-12-31")
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
            name="endDate"
            render={({ field }) => (
              <FormItem className="flex flex-col">
                <FormLabel>End Date</FormLabel>
                <Popover open={endDateOpen} onOpenChange={setEndDateOpen}>
                  <PopoverTrigger asChild>
                    <FormControl>
                      <Button
                        variant={"outline"}
                        className={cn(
                          "w-full pl-3 text-left font-normal",
                          !field.value && "text-muted-foreground",
                          frequency !== BudgetFrequency.CUSTOM && "opacity-50 cursor-not-allowed"
                        )}
                        disabled={frequency !== BudgetFrequency.CUSTOM}
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
                      onSelect={(date) => {
                        field.onChange(date);
                        setEndDateOpen(false);
                      }}
                      disabled={(date) =>
                        date < new Date("1900-01-01") ||
                        date > new Date("2100-12-31")
                      }
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
                {frequency !== BudgetFrequency.CUSTOM && (
                  <FormDescription>
                    End date is automatically set based on the frequency
                  </FormDescription>
                )}
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="categories"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Categories</FormLabel>
              <FormControl>
                <CategoryMultiSelect
                  categories={categories}
                  value={field.value}
                  onChange={field.onChange}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="flex gap-4">
          <Button type="submit" className="flex-1" disabled={isSubmitting}>
            {isSubmitting
              ? initialData
                ? "Updating..."
                : "Creating..."
              : initialData
              ? "Update Budget"
              : "Create Budget"}
          </Button>
          
         
        </div>
      </form>
    </Form>
  );
};

export default BudgetForm;