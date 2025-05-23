import NextAuth, { DefaultSession, Account, JWT, Session, AuthOptions } from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';

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

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };