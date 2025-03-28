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
  useToast,
  FormErrorMessage,
  Text,
  Link
} from '@chakra-ui/react'

const RegisterForm = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const toast = useToast()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    // Validate passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      setIsLoading(false)
      return
    }

    try {
      await authService.register(email, password)
      toast({
        title: 'Registration Successful',
        description: 'Please login with your credentials',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
      navigate('/login')
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        'An error occurred during registration. Please try again.'
      )
      toast({
        title: 'Registration Failed',
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
        <Heading>Create Account</Heading>
        
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
            autoComplete="new-password"
          />
        </FormControl>

        <FormControl isInvalid={!!error}>
          <FormLabel>Confirm Password</FormLabel>
          <Input 
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm your password"
            required
            isDisabled={isLoading}
            autoComplete="new-password"
          />
          <FormErrorMessage>{error}</FormErrorMessage>
        </FormControl>

        <Button 
          type="submit" 
          colorScheme="blue" 
          width="full"
          isLoading={isLoading}
          loadingText="Creating Account..."
        >
          Register
        </Button>

        <Text fontSize="sm">
          Already have an account?{' '}
          <Link color="blue.500" href="/login">
            Login here
          </Link>
        </Text>
      </VStack>
    </Box>
  )
}

export default RegisterForm
