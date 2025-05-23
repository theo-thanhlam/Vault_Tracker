export enum CategoryTypeEnum {
  EXPENSE = "EXPENSE",
  INCOME = "INCOME",
  EQUITY = "EQUITY",
  LIABILITY = "LIABILITY",
  ASSET = "ASSET",
  OTHER = "OTHER",
}

export interface Category {
  id: string;
  name: string;
  type: CategoryTypeEnum;
  description: string;
  parentId?: string;
  createdAt: string;
  updatedAt?: string;
  deletedAt?: string;
  userId: string;
}

export interface CategoryFormData {
  name: string;
  type: CategoryTypeEnum;
  description: string;
  parentId?: string;
} 