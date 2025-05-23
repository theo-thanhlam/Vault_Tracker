import { gql } from "@apollo/client";

export const GET_TRANSACTIONS_QUERY = gql`
  query GetTransactions {
    transaction {
      getTransactions {
        message
        code
        transactions {
          id
          amount
          description
          categoryName
          categoryType
          date
          createdAt
          updatedAt
          
        }
      }
    }
  }
`; 