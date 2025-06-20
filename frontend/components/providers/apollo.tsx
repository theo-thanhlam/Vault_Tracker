"use client";


import { HttpLink } from "@apollo/client";
import {
  ApolloNextAppProvider,
  ApolloClient,
  InMemoryCache,
} from "@apollo/client-integration-nextjs";


// have a function to create a client for you
function makeSSRClient() {
  const httpLink = new HttpLink({
    // this needs to be an absolute url, as relative urls cannot be used in SSR
    uri: `${process.env.NEXT_PUBLIC_API_URL}/gqql`,
    credentials:"include",
    
    fetchOptions: {
     
    },
   
  });


  return new ApolloClient({
    cache: new InMemoryCache(),
    link: httpLink,
  });
}

// you need to create a component to wrap your app in
export function ApolloWrapper({ children }: React.PropsWithChildren) {
  return (
    <ApolloNextAppProvider makeClient={makeSSRClient}>
      {children}
    </ApolloNextAppProvider>
  );
}