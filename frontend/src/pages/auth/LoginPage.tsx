import React from 'react';
import { Center, Container } from '@chakra-ui/react';
import LoginForm from '../../components/auth/LoginForm';

const LoginPage: React.FC = () => {
  return (
    <Center minH="100vh">
      <Container maxW="md">
        <LoginForm />
      </Container>
    </Center>
  );
};

export default LoginPage;
