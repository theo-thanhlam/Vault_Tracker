
import Link from 'next/link';
import { CategoryList } from '@/components/category/category-list';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';

export default async function CategoriesPage() {
  
  return (
    <div className="container mx-auto py-6 space-y-6 w-auto">
      <div className="flex items-center gap-4 flex-col items-start">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/dashboard" className="flex items-start gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
        </Button>
        <h1 className="text-xl font-bold md:text-2xl lg:text-3xl">Categories</h1>
      </div>
      <CategoryList />
    </div>
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