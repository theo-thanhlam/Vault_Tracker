import NextAuth from "next-auth"

declare module "next-auth" {
  interface Session {
    id_token?: string
    user?: {
        id?:string | null
      name?: string | null
      email?: string | null
      image?: string | null
    }
  }
} 