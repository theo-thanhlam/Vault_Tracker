"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import GoalTableHeader from "@/components/goal/goal-table-header";
import GoalTableBody from "@/components/goal/goal-table-body";

const GoalTable = () => {
  const [sortBy, setSortBy] = useState("start-date");
  const [filterBy, setFilterBy] = useState("all");

  const handleSortChange = (value: string) => {
    setSortBy(value);
  };

  const handleFilterChange = (value: string) => {
    setFilterBy(value);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col gap-4"
    >
      <GoalTableHeader
        handleSortChange={handleSortChange}
        handleFilterChange={handleFilterChange}
      />
      <GoalTableBody sortBy={sortBy} filterBy={filterBy} />
    </motion.div>
  );
};

export default GoalTable;
