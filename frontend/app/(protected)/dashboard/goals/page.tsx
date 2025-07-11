import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

import GoalTable from "@/components/goal/goal-table";
import PageWrapper from "@/components/dashboard/page-wrapper";

export default async function GoalPage() {
  
  
  
  return (
    <PageWrapper>
      <GoalTable />
    </PageWrapper>
  );
} 