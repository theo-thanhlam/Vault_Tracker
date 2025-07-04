import { TableBody, TableCell, TableRow } from "../ui/table";
import GoalTableRow from "./goal-table-row";
import { Goal } from "@/types/goal";
import GoalSkeleton from "./goal-skeleton";
import { Dialog } from "../ui/dialog";
import GoalDetail from "./goal-detail";

interface GoalTableBodyProps {
  sortBy: string;
  filterBy: string;
  goals: Goal[];
  onViewDetails?: (goal: Goal) => void;
  onEdit?: (goal: Goal) => void;
  onDelete?: (goal: Goal) => void;
}

function modify_goals(goals: Goal[], sortBy: string, filterBy: string): Goal[] {
  // Create a new array for filtered goals
  let filteredGoals = filterBy === "all" 
    ? [...goals]
    : goals.filter((goal: Goal) => goal.status === filterBy);

    
  
  // Create a new array for sorted goals
  return [...filteredGoals].sort((a: Goal, b: Goal) => {
    switch (sortBy) {
      case 'amount':
        return b.target - a.target;
      case 'progress':
        return b.progress - a.progress;
      case 'duration': {
        const durationA = new Date(a.endDate).getTime() - new Date(a.startDate).getTime();
        const durationB = new Date(b.endDate).getTime() - new Date(b.startDate).getTime();
        return durationA - durationB;
      }
      default:
        return 0;
    }
  });
}

const GoalTableBody = ({ 
  sortBy, 
  filterBy, 
  goals, 
  onViewDetails,
  onEdit, 
  onDelete 
}: GoalTableBodyProps) => {

  let modified_goals = modify_goals(goals, sortBy, filterBy)



  return (
    <TableBody>
      {goals.length === 0 ? 
        (
          <TableRow>
            <TableCell colSpan={6} className="text-center">
              <p className="text-gray-500">Add a goal to get started</p>
            </TableCell>
          </TableRow>
        ):
        (
          modified_goals.map((goal: Goal) => (
            <GoalTableRow 
              key={goal.id} 
              goal={goal} 
              onViewDetails={onViewDetails}
              onEdit={onEdit} 
              onDelete={onDelete} 
            />
          ))  
        )  
     }
      
    </TableBody>
  );
};

export default GoalTableBody;
