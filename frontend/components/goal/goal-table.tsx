"use client";
import React, { useState } from "react";
import GoalTableFilter from "@/components/goal/goal-table-filter";
import GoalTableBody from "@/components/goal/goal-table-body";
import GoalTableSectionHeader from "./goal-table-section-header";
import { DELETE_GOAL, GET_ALL_GOALS } from "@/lib/graphql/goal/gql";
import { useMutation, useQuery } from "@apollo/client";
import GoalTableHeader from "./goal-table-header";
import { Table, TableBody, TableCell, TableRow } from "../ui/table";
import GoalSkeleton from "./goal-skeleton";
import { Goal } from "@/types/goal";
import GoalDetail from "./goal-detail";
import { Dialog, DialogContent } from "../ui/dialog";
import { GoalForm } from "./goal-form";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "../ui/alert-dialog";
import { EditDialog } from "../form-components/edit-dialog";
import { toast } from "sonner";
import { DeleteDialog } from "../form-components/delete-dialog";

const GoalTable = () => {
  const [sortBy, setSortBy] = useState("amount");
  const [filterBy, setFilterBy] = useState("all");
  const [selectedGoal, setSelectedGoal] = useState<Goal | null>(null);
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  const {data, loading, error, refetch} = useQuery(GET_ALL_GOALS,{
    fetchPolicy: "network-only",
  } )
  const goals = data?.goal.getAllGoals.values || [];

  const handleSortChange = (value: string) => {
    setSortBy(value);
  };

  const handleFilterChange = (value: string) => {
    setFilterBy(value);
  };

  const handleViewDetails = (goal: Goal) => {
    setSelectedGoal(goal);
    setIsDetailDialogOpen(true);
  };

  const handleEdit = (goal: Goal) => {
    setSelectedGoal(goal);
    setIsEditDialogOpen(true);
  };

  const handleDelete = (goal: Goal) => {
    setSelectedGoal(goal);
    setIsDeleteDialogOpen(true);
  };

  const [deleteGoal] = useMutation(DELETE_GOAL, {
    onCompleted: (data) => {
      toast.success("Goal deleted successfully");
      refetch();
    },
    onError: (error) => {
      toast.error("Failed to delete goal");
    },
  })
  const handleDeleteConfirm = async () => {
    if (!selectedGoal) return;
    
    await deleteGoal({
      variables: {
        input: {
          id: selectedGoal.id,
        },
      },
    });
    setIsDeleteDialogOpen(false);
    setSelectedGoal(null);
  };

  return (
    <div className="flex flex-col gap-4">
      <GoalTableSectionHeader refetch={refetch} />
      <GoalTableFilter
        handleSortChange={handleSortChange}
        handleFilterChange={handleFilterChange}
      />
      <div className="overflow-x-auto">
        <Table>
          <GoalTableHeader />
          {loading ? (
            <TableBody>
              <TableRow>
                <TableCell colSpan={6} className="text-center">
                  <GoalSkeleton />
                </TableCell>
              </TableRow>
            </TableBody>
          ) : error ? (
            <TableBody>
              <TableRow>
                <TableCell colSpan={6} className="text-center">
                  Something went wrong. Please try again.
                </TableCell>
              </TableRow>
            </TableBody>
          ) : (
            <GoalTableBody 
              sortBy={sortBy} 
              filterBy={filterBy} 
              goals={goals} 
              onViewDetails={handleViewDetails}
              onEdit={handleEdit} 
              onDelete={handleDelete}
            />
          )}
        </Table>
      </div>

      {/* Detail Dialog */}
      {/* <Dialog open={isDetailDialogOpen} onOpenChange={setIsDetailDialogOpen}>
        <GoalDetail goal={selectedGoal} />
      </Dialog> */}

      {/* Edit Dialog */}
      <EditDialog
        title="Edit Goal"
        description="Update goal details"
        open={isEditDialogOpen}
        onOpenChange={setIsEditDialogOpen}
        formComponent={selectedGoal && <GoalForm initialData={selectedGoal} onSuccess={() => {
          setIsEditDialogOpen(false);
          refetch();
        }} />} 
      />

      {/* Delete Confirmation Dialog */}
      <DeleteDialog
        // title="Delete Goal"
        // description="Delete goal"
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        onDelete={handleDeleteConfirm}
      />
   
    </div>
  );
};

export default GoalTable;
