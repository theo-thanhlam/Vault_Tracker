import { Category } from "./category";

export interface Goal {
    id: string;
    name: string;
    description: string;
    target: number;
    startDate: string;
    endDate: string;
    status: string;
    categories: Category[];
    progress: number;
    currentAmount: number;
    createdAt: string;
    updatedAt: string;
}