import { gql } from '@apollo/client'

export const CREATE_GOAL = gql`
  mutation CreateGoal($input: CreateGoalInput!) {
    goal {
      create(input: $input) {
        message
        code
        values {
          id
          name
          description
          target
          startDate
          endDate
          status
          userId
        }
      }
    }
  }
` 