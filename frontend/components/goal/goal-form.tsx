"use client";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
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
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { format } from "date-fns";
import { CalendarIcon } from "lucide-react";
import { toast } from "sonner";
import { CREATE_GOAL,UPDATE_GOAL, DELETE_GOAL } from "@/lib/graphql/goal/gql";
import { useMutation, useQuery } from "@apollo/client";
import { useState } from "react";
import { CategorySelect } from "@/components/category/category-select";
import { GET_CATEGORIES_BY_TYPE_QUERY, GET_CATEGORIES_QUERY } from "@/lib/graphql/category/gql";
import { Goal } from "@/types/goal";

const formSchema = z.object({
  name: z.string().min(2, {
    message: "Name must be at least 2 characters.",
  }),
  description: z.string().min(10, {
    message: "Description must be at least 10 characters.",
  }),
  target: z.string().refine((val) => !isNaN(Number(val)) && Number(val) > 0, {
    message: "Target must be a positive number.",
  }),
  startDate: z.date({
    required_error: "Start date is required.",
  }),
  endDate: z.date({
    required_error: "End date is required.",
  }),
  status: z.enum(["NOT_STARTED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED"], {
    required_error: "Status is required.",
  }),
  categoryId: z.string().optional(),
});

interface GoalFormProps {
  initialData?: Goal;
  onSuccess?: () => void;
}

export function GoalForm({ initialData, onSuccess }: GoalFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false); // loading state


  const [createGoal] = useMutation(CREATE_GOAL, {
    onCompleted: (data) => {
      toast.success("Goal created successfully");
      onSuccess?.();
    },
    onError: (error) => {
      toast.error("Failed to create goal");
    },
  });
  const [updateGoal] = useMutation(UPDATE_GOAL, {
    onCompleted: (data) => {
      toast.success("Goal updated successfully");
      onSuccess?.();
    },
    onError: (error) => {
      toast.error("Failed to update goal");
    },
  });
  

  const { data: categoriesData } = useQuery(GET_CATEGORIES_BY_TYPE_QUERY, {
    variables: {
      input: {
        type: "INCOME",
      },
    },
  });
  const categories = categoriesData?.category?.getCategoriesByType?.treeViews || [];

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues:initialData?
    {
      name: initialData.name,
      description: initialData.description,
      target: initialData.target.toString(),
      status: initialData.status as "IN_PROGRESS" | "COMPLETED" | "CANCELLED" | "FAILED",
      categoryId: initialData.categoryId,
      startDate: new Date(initialData.startDate),
      endDate: new Date(initialData.endDate),
    }:
    {
      name: "",
      description: "",
      target: "",
      status: "IN_PROGRESS",
      categoryId: undefined,
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    try {
      setIsSubmitting(true);
      if (initialData) {
        await updateGoal({
          variables: {
            input: {
              id: initialData.id,
              ...values,
              target: parseFloat(values.target),
              startDate: values.startDate,
              endDate: values.endDate,
            },
          },
        });
      } else {
        await createGoal({
          variables: {
            input: {
              ...values,
              target: parseFloat(values.target),
              startDate: values.startDate,
              endDate: values.endDate,
            },
          },
        });
      }
    } catch (error) {
      toast.error(initialData ? "Failed to update goal" : "Failed to create goal");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="Enter goal name" {...field} />
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
                  placeholder="Enter goal description"
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
          name="target"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Target Amount</FormLabel>
              <FormControl>
                <Input type="number" placeholder="00.00" {...field} step="0.01" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="startDate"
            render={({ field }) => (
              <FormItem className="flex flex-col">
                <FormLabel>Start Date</FormLabel>
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
                        date < new Date() || date < new Date("1900-01-01")
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
                        date < new Date() || date < new Date("1900-01-01")
                      }
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="status"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Status</FormLabel>
                <Select
                  onValueChange={field.onChange}
                  defaultValue={field.value}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select a status" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="IN_PROGRESS">In Progress</SelectItem>
                    <SelectItem value="COMPLETED">Completed</SelectItem>
                    <SelectItem value="FAILED">Failed</SelectItem>
                    <SelectItem value="CANCELLED">Cancelled</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="categoryId"
            render={({ field }) => (
              <FormItem>
                <CategorySelect
                  categories={categories}
                  value={field.value}
                  onChange={field.onChange}
                />
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <Button type="submit" className="w-full" disabled={isSubmitting}>
            {isSubmitting ? (
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                {initialData ? "Updating..." : "Creating..."}
              </div>
            ) : initialData ? (
              "Update Goal"
            ) : (
              "Create Goal"
            )}
          </Button>
      </form>
    </Form>
  );
}
