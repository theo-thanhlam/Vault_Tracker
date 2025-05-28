import { gql } from "@apollo/client";

export const GET_TRANSACTIONS_QUERY = gql`
  query GetTransactions($input:GetAllTransactionsInput!) {
    transaction {
      getTransactions(input:$input) {
        message
        code
        totalCount
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