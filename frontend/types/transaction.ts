export interface Transaction {
  id: string;
  amount: number;
  description: string;
  categoryName: string;
  categoryType: string;
  date: string;
  createdAt: string;
  updatedAt: string | null;
  categoryId: string;
  // userId: string;
} 