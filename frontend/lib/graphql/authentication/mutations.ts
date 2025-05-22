import { gql } from '@apollo/client';

// Register a new user
export const REGISTER_MUTATION = gql`
  mutation Register($input: RegisterInput!) {
    auth {
      register(input: $input) {
        message
        code
        values
        token
      }
    }
  }
`;

// Login user
export const LOGIN_MUTATION = gql`
  mutation Login($input: LoginInput!) {
    auth {
      login(input: $input) {
        message
        code
        token
      }
    }
  }
`;

// Google login
export const GOOGLE_LOGIN_MUTATION = gql`
  mutation GoogleLogin($input: GoogleLoginInput!) {
    auth {
      googleLogin(input: $input) {
        message
        code
        token
      }
    }
  }
`;

// Logout user
export const LOGOUT_MUTATION = gql`
  mutation Logout {
    auth {
      logout
    }
  }
`;

// Verify email
export const VERIFY_EMAIL_MUTATION = gql`
  mutation VerifyEmail($input: VerifyEmailInput!) {
    auth {
      verifyEmail(input: $input)
    }
  }
`;