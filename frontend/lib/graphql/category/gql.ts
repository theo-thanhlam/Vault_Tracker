import { gql } from "@apollo/client";

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

const Category_fragment = gql`
  fragment Category on CategoryType {
    id
    name
    type
    updatedAt
    description

    createdAt
  
    description
  }
`
const Category_recursive_fragment = gql`

  fragment CategoryRecursive on CategoryType {
    # Level 1
    id
    name
    type
    createdAt
    description
    updatedAt
    children {
      #Level 2
      ...Category
      children {
        # Level 3
        ...Category
        children{
          # Level 4
          ...Category
        }
      }
    }
  }
`

export const GET_CATEGORY_TREE = gql`
${Category_fragment}
${Category_recursive_fragment}
query CategoryTree {
  category {
    getAllCategories {
      message
      code
      
      treeViews {
        ...CategoryRecursive
      }
    }
  }
}
`