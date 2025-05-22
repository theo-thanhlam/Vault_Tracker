import { NextRequest, NextResponse } from 'next/server';
import { getCurrentUser } from './lib/auth';


export async function middleware(request: NextRequest) {
  
  const authToken = request.cookies.get('auth_token')?.value;
  
  const user = await getCurrentUser(authToken as string);
  const response = NextResponse.next();
  response.headers.set('x-auth-status', user ? 'authenticated' : 'unauthenticated');


  if (request.nextUrl.pathname.startsWith('/auth')) {
    if (user) {
      return NextResponse.redirect(new URL('/dashboard', request.url),{
        headers: response.headers
      });
    }
  }

  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!user) {
      return NextResponse.redirect(new URL('/auth', request.url),{
        headers: response.headers
      });
    }
  }

  return response;
}
export const config = {
  matcher: ['/auth/:path*', '/dashboard/:path*'],
};
