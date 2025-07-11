
import Link from 'next/link';
import { CategoryList } from '@/components/category/category-list';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import { getCategoryTree } from '@/lib/graphql/category/queries';
import { CategoryTable } from '@/components/category/category-table';
import PageWrapper from '@/components/dashboard/page-wrapper';


export default async function CategoriesPage() {
  
  return (
    <PageWrapper>
      <CategoryTable />
    </PageWrapper>
  );
}

function CategoryListSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <div key={i} className="flex items-center space-x-4">
          <Skeleton className="h-12 w-12 rounded-full" />
          <div className="space-y-2">
            <Skeleton className="h-4 w-[250px]" />
            <Skeleton className="h-4 w-[200px]" />
          </div>
        </div>
      ))}
    </div>
  );
} 