import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface GoalTableFilterProps {
  handleSortChange: (value: string) => void;
  handleFilterChange: (value: string) => void;
}

const GoalTableFilter = ({
  handleSortChange,
  handleFilterChange,
}: GoalTableFilterProps) => {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-4 ">
        {/* <h1 className="text-3xl font-bold">Goals</h1> */}
        <Select onValueChange={handleSortChange}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="duration">Remaining Duration</SelectItem>
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
            <SelectItem value="IN_PROGRESS">In Progress</SelectItem>
            <SelectItem value="COMPLETED">Completed</SelectItem>
            <SelectItem value="FAILED">Failed</SelectItem>
            <SelectItem value="CANCELLED">Cancelled</SelectItem>

          </SelectContent>
        </Select>
      </div>

      
    </div>
  );
};

export default GoalTableFilter;
