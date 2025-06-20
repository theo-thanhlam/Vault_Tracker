import { headers } from "next/headers";
import NextAuth, { DefaultSession, Account, JWT, Session, AuthOptions } from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';


const GET_CURRENT_USER_QUERY = `
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
  }`


export async function getCurrentUser(authToken: string) {
  if(!authToken){
    return null;
  }
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/gql`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Cookie': `auth_token=${authToken}`,
        },
        body: JSON.stringify({
          query: GET_CURRENT_USER_QUERY,
        }),
      });

      const result = await response.json();
      const user = result?.data?.auth?.getCurrentUser?.values;
      return user;
  }

export async function getAuthStatus(){

  const authHeader = (await headers()).get('x-auth-status')
  return authHeader
}

declare module "next-auth" {
  interface Session extends DefaultSession {
    id_token?: string;
  }

  interface JWT {
    id_token?: string;
  }
}

export const authOptions: AuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
      authorization: {
        params: {
          prompt: "login",

          response_type: "code",
        }
      }
    }),
  ],
  callbacks: {
    async jwt({ token, account, user }) {
      // Persist the OAuth access_token and or the user id to the token right after signin
      if (account?.id_token) {
        token.id_token = account.id_token as string;
      }
      return token;
    },
    async session({ session, token, user }) {
      // Send properties to the client, like an access_token and user id from a provider.
      if (token.id_token) {
        session.id_token = token.id_token as string;
        
      }
      return session;
       
    },
  },
  secret: process.env.NEXTAUTH_SECRET,
  
  
};
