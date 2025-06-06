import { Category } from "./category";

export interface Budget {
    id: string;
    name: string;
    description: string;
    amount: number;
    type: string;
    frequency: string;
    startDate: string;
    endDate: string;
    user_id: string;
    categories?: Category[];
    currentAmount: number;
    createdAt: string;
    updatedAt: string;
}