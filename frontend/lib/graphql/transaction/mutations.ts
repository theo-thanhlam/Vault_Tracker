import { gql } from "@apollo/client";

export const CREATE_TRANSACTION_MUTATION = gql`
  mutation CreateTransaction($input: CreateTransactionInput!) {
    transaction {
      create(input: $input) {
        message
        code
        values {
          id
          amount
          description
          categoryId
          date
          createdAt
          updatedAt
          userId
        }
      }
    }
  }
`;

export const UPDATE_TRANSACTION_MUTATION = gql`
  mutation UpdateTransaction($input: UpdateTransactionInput!) {
    transaction {
      update(input: $input) {
        message
        code
        values {
          id
          amount
          description
          categoryId
          date
          createdAt
          updatedAt
          userId
        }
      }
    }
  }
`;

export const DELETE_TRANSACTION_MUTATION = gql`
  mutation DeleteTransaction($input: DeleteTransactionInput!) {
    transaction {
      delete(input: $input) {
        message
        code
        values {
          id
        }
      }
    }
  }
`; 