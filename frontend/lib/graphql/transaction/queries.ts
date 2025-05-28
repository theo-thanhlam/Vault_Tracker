import {getClient, PreloadQuery} from "@/lib/apollo-rsc-client"
import { GET_TRANSACTIONS_QUERY } from "./gql"



export async function getTransactions(limit = 10){
  const client = await getClient()
  try{
    const {data} = await client.query({query:GET_TRANSACTIONS_QUERY, variables:{input:{limit:10}}})
    return data.transaction.getTransactions.transactions
  }
  catch{
    throw new Error("GET TRANSACTIONS ERROR")
  }

}