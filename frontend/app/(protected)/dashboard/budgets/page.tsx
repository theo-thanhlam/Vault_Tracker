import PageWrapper from "@/components/dashboard/page-wrapper";
import BudgetTable from "@/components/budget/budget-table";

export default async function BudgetPage() {
  return (
    <PageWrapper>
      <BudgetTable />
    </PageWrapper>
  );
}