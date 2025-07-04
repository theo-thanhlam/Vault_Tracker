import { useState } from "react";
import TableSectionHeader from "../form-components/table-section-header";
import { GoalForm } from "./goal-form";

const GoalTableSectionHeader = ({ refetch }: { refetch: () => void }) => {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const handleGoalSuccess = () => {
    setIsCreateDialogOpen(false);
    refetch();
  };
  return (
    <TableSectionHeader
      title="Recent Goals"
      action_title="Add Goal"
      formTitle="Create Goal"
      formDescription="Add a new goal to your account."
      open={isCreateDialogOpen}
      onOpenChange={setIsCreateDialogOpen}
      onSuccess={handleGoalSuccess}
      formComponent={<GoalForm onSuccess={handleGoalSuccess} />}
    />
  )
}

export default GoalTableSectionHeader