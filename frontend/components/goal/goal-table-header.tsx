import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Plus } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { GoalForm } from "./goal-form";

interface GoalTableHeaderProps {
  handleSortChange: (value: string) => void;
  handleFilterChange: (value: string) => void;
}

const GoalTableHeader = ({
  handleSortChange,
  handleFilterChange,
}: GoalTableHeaderProps) => {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-4 ">
        {/* <h1 className="text-3xl font-bold">Goals</h1> */}
        <Select onValueChange={handleSortChange}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="start-date">Start Date</SelectItem>
            <SelectItem value="end-date">End Date</SelectItem>
            <SelectItem value="amount">Amount</SelectItem>
            <SelectItem value="progress">Progress</SelectItem>
          </SelectContent>
        </Select>
        <Select onValueChange={handleFilterChange}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Filter by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All</SelectItem>
            <SelectItem value="in-progress">In Progress</SelectItem>
            <SelectItem value="completed">Completed</SelectItem>
            <SelectItem value="not-started">Not Started</SelectItem>
            <SelectItem value="overdue">Overdue</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Dialog>
        <DialogTrigger asChild>
          <Button className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            <span className="hidden md:block">New Goal</span>
          </Button>
        </DialogTrigger>
        <DialogContent className="">
          <DialogHeader>
            <DialogTitle>Create New Goal</DialogTitle>
          </DialogHeader>
          <GoalForm />
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default GoalTableHeader;
