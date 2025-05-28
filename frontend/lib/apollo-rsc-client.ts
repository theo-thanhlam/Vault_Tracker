'use server'
import { HttpLink } from "@apollo/client";
import {
  registerApolloClient,
  ApolloClient,
  InMemoryCache,
} from "@apollo/client-integration-nextjs";
import { cookies } from "next/headers";

const rscApolloClient = registerApolloClient(async () => {
  const auth_token = (await cookies()).get("auth_token")

  return new ApolloClient({
    cache: new InMemoryCache(),
    link: new HttpLink({
      // this needs to be an absolute url, as relative urls cannot be used in SSR
      uri: `${process.env.NEXT_PUBLIC_API_URL}/api`,
      headers: auth_token?.value ?{
        Cookie:`auth_token=${auth_token?.value}`
      }:{},
      fetchOptions: {
        // you can pass additional options that should be passed to `fetch` here,
        // e.g. Next.js-related `fetch` options regarding caching and revalidation
        // see https://nextjs.org/docs/app/api-reference/functions/fetch#fetchurl-options
      },
    }),
  });
});
export const { getClient, query, PreloadQuery} = rscApolloClient