import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/authService';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  Text,
  useToast,
  FormErrorMessage,
  Link
} from '@chakra-ui/react';

const LoginForm = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const toast = useToast()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      await authService.login(email, password)
      toast({
        title: 'Login Successful',
        description: 'Welcome back!',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
      navigate('/dashboard')
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        'An error occurred during login. Please try again.'
      )
      toast({
        title: 'Login Failed',
        description: error,
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Box maxW="md" mx="auto" mt={8} p={6} borderRadius="lg" boxShadow="lg">
      <VStack spacing={6} as="form" onSubmit={handleSubmit}>
        <Heading>Login to NoteKo</Heading>
        
        {error && (
          <Text color="red.500" fontSize="sm">
            {error}
          </Text>
        )}

        <FormControl isInvalid={!!error}>
          <FormLabel>Email</FormLabel>
          <Input 
            type="email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
            isDisabled={isLoading}
            autoComplete="email"
          />
        </FormControl>

        <FormControl isInvalid={!!error}>
          <FormLabel>Password</FormLabel>
          <Input 
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
            isDisabled={isLoading}
            autoComplete="current-password"
          />
          <FormErrorMessage>{error}</FormErrorMessage>
        </FormControl>

        <Button 
          type="submit" 
          colorScheme="blue" 
          width="full"
          isLoading={isLoading}
          loadingText="Logging in..."
        >
          Login
        </Button>

        <Text fontSize="sm">
          Don't have an account?{' '}
          <Link color="blue.500" href="/register">
            Register here
          </Link>
        </Text>
      </VStack>
    </Box>
  )
}

export default LoginForm
