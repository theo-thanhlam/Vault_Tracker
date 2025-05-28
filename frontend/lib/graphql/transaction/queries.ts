import { gql } from "@apollo/client";
import {getClient, query, PreloadQuery} from "@/lib/apollo-rsc-client"

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

export async function getTransactions(limit = 10){
  try{
    const {data} = await query({query:GET_TRANSACTIONS_QUERY, variables:{input:{limit:10}}})
    return data.transaction.getTransactions.transactions
  }
  catch{
    throw new Error("GET TRANSACTIONS ERROR")
  }

}