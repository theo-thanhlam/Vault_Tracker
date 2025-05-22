import { gql } from '@apollo/client';

export const GET_CURRENT_USER = gql`
  query GetCurrentUser {
    auth {
      getCurrentUser {
      values{
        id
        firstName
        lastName
        email       
        role
        createdAt
        updatedAt
      }
      }
    }
  }
`;
