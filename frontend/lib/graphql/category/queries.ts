import { gql } from '@apollo/client';
import { apolloClient } from '@/lib/apollo-client';
import { Category } from '@/types/category';

export const GET_CATEGORIES_QUERY = gql`
  query GetCategories {
    category {
      getCategory {
        message
        code
        values {
          id
          name
          type
          description
          parentId
          createdAt
          updatedAt
        }
      }
    }
  }
`;

export async function getCategories(): Promise<Category[]> {
  try {
    const { data } = await apolloClient.query({
      query: GET_CATEGORIES_QUERY,
    });

    if (data?.category?.getCategory?.code !== 200) {
      throw new Error(data?.category?.getCategory?.message || 'Failed to fetch categories');
    }

    return data.category.getCategory.values || [];
  } catch (error) {
    console.error('Error fetching categories:', error);
    throw error;
  }
}