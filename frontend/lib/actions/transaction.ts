"use server";

import { apolloClient } from "@/lib/apollo-client";
import { GET_TRANSACTIONS_QUERY } from "@/lib/graphql/transaction/queries";
import { Transaction } from "@/types/transaction";

export async function getInitialTransactions(): Promise<Transaction[]> {
  try {
    
    const { data } = await apolloClient.query({
      query: GET_TRANSACTIONS_QUERY,
    });

    return data?.transaction?.getTransactions?.transactions || [];
  } catch (error) {
    console.error("Failed to fetch initial transactions:", error);
    return [];
  }
} 