'use server';
import { apolloClient } from '@/lib/apollo-client';
import { CREATE_CATEGORY_MUTATION, UPDATE_CATEGORY_MUTATION, DELETE_CATEGORY_MUTATION } from './gql';



// Types for category mutations
export type CreateCategoryInput = {
  name: string;
  type: string;
  description: string;
  parentId?: string;
};

export type UpdateCategoryInput = CreateCategoryInput & {
  id: string;
};

export type DeleteCategoryInput = {
  id: string;
};

// Server actions for category mutations
export async function createCategoryAction(input: CreateCategoryInput) {
  
  
  try {
    const { data } = await apolloClient.mutate({
      mutation: CREATE_CATEGORY_MUTATION,
      variables: { input },
    });
    
    if (data?.category?.create?.code !== 'SUCCESS') {
      throw new Error(data?.category?.create?.message || 'Failed to create category');
    }
    
    return {
      success: true,
      data: data.category.create.values,
      message: data.category.create.message
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to create category'
    };
  }
}

export async function updateCategoryAction(input: UpdateCategoryInput) {
  
  
  try {
    const { data } = await apolloClient.mutate({
      mutation: UPDATE_CATEGORY_MUTATION,
      variables: { input },
    });
    
    if (data?.category?.update?.code !== 'SUCCESS') {
      throw new Error(data?.category?.update?.message || 'Failed to update category');
    }
    
    return {
      success: true,
      data: data.category.update.values,
      message: data.category.update.message
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to update category'
    };
  }
}

export async function deleteCategoryAction(input: DeleteCategoryInput) {
  
  try {
    const { data } = await apolloClient.mutate({
      mutation: DELETE_CATEGORY_MUTATION,
      variables: { input },
    });
    
    if (data?.category?.delete?.code !== 'SUCCESS') {
      throw new Error(data?.category?.delete?.message || 'Failed to delete category');
    }
    
    return {
      success: true,
      message: data.category.delete.message
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to delete category'
    };
  }
} 