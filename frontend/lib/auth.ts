

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
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api`, {
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