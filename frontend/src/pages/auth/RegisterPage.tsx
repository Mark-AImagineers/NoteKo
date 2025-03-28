import React from 'react';
import { Center, Container } from '@chakra-ui/react';
import RegisterForm from '../../components/auth/RegisterForm';

const RegisterPage: React.FC = () => {
  return (
    <Center minH="100vh">
      <Container maxW="md">
        <RegisterForm />
      </Container>
    </Center>
  );
};

export default RegisterPage;