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
          categories
        }
      }
    }
  }
` 

export const GET_ALL_GOALS = gql`
  query MyQuery {
    goal {
      getAllGoals {
        code
        message
        values {
          id
          name
          status
          target
          updatedAt
          progress
          categories {
            id
            name
            type
            description
            parentId
            createdAt
            updatedAt
            deletedAt
          }
          createdAt
          description
          endDate
          startDate
          currentAmount
        }
      }
    }
  }
`

export const UPDATE_GOAL = gql`
  mutation UpdateGoal($input: UpdateGoalInput!) {
    goal {
      update(input: $input) {
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
          categories{
            id
            name
          }
        }
      }
    }
  }
`


export const DELETE_GOAL = gql`
  mutation DeleteGoal($input: DeleteGoalInput!) {
    goal {
      delete(input: $input) {
        message
        code
      }
    }
  }
`