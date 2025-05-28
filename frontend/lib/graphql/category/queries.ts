import { gql } from '@apollo/client';
import { Category } from '@/types/category';

export const GET_CATEGORIES_QUERY = gql`
  query GetCategories {
    category {
      getAllCategories {
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
