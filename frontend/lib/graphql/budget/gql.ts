import { gql } from "@apollo/client"



export const GET_ALL_BUDGETS = gql`
    query GetAllBudgets {
        budget {
            getAllBudgets {
                code
                message
                values {
                    id
                    name
                    description
                    amount
                    type
                    frequency
                    startDate
                    endDate
                    userId
                    createdAt
                    updatedAt
                    currentAmount
                    categories {
                        id
                        name
                    }
                }
            }
        }
    }
`

export const DELETE_BUDGET = gql`
    mutation DeleteBudget($input: DeleteInput!) {
        budget {
            deleteBudget(input: $input) {
                code
                message
            }
        }
    }
`

export const CREATE_BUDGET_MUTATION = gql`
  mutation CreateBudget($input: CreateBudgetInput!) {
    budget {
      create(input: $input) {
        message
        code
        values {
          id
          name
          description
          amount
          type
          frequency
          startDate
          endDate
          categories {
            id
            name
          }
        }
      }
    }
  }
`;

export const UPDATE_BUDGET_MUTATION = gql`
  mutation UpdateBudget($input: UpdateBudgetInput!) {
    budget {
      update(input: $input) {
        message
        code
        values {
          id
          name
          description
          amount
          type
          frequency
          startDate
          endDate
          categories {
            id
            name
          }
        }
      }
    }
  }
`;

export const DELETE_BUDGET_MUTATION = gql`
  mutation DeleteBudget($input: DeleteBudgetInput!) {
    budget {
      delete(input: $input) {
        message
        code
      }
    }
  }
`;

export const GET_BUDGETS_QUERY = gql`
  query GetBudgets {
    budget {
      getAllBudgets {
        message
        code
        values {
          id
          name
          description
          amount
          type
          frequency
          startDate
          endDate
          currentAmount
          categories {
            id
            name
          }
        }
      }
    }
  }
`;