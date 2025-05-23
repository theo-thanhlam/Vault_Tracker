import { gql } from "@apollo/client";

export const CREATE_CATEGORY_MUTATION = gql`
  mutation CreateCategory($input: CreateCategoryInput!) {
    category {
      create(input: $input) {
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

export const UPDATE_CATEGORY_MUTATION = gql`
  mutation UpdateCategory($input: UpdateCategoryInput!) {
    category {
      update(input: $input) {
        message
        code
        values {
          id
          name
          type
          description
          parentId
          updatedAt
        }
      }
    }
  }
`;

export const DELETE_CATEGORY_MUTATION = gql`
  mutation DeleteCategory($input: DeleteCategoryInput!) {
    category {
      delete(input: $input) {
        message
        code
      }
    }
  }
`;