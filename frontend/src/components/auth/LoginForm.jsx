import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  useToast
} from '@chakra-ui/react'
import { useState } from 'react'

const LoginForm = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const toast = useToast()

  const handleSubmit = (e) => {
    e.preventDefault()
    // We'll add the login logic later
    console.log('Login attempt:', { email, password })
    toast({
      title: 'Login Attempt',
      description: 'Login functionality coming soon!',
      status: 'info',
      duration: 3000,
      isClosable: true,
    })
  }

  return (
    <Box maxW="md" mx="auto" mt={8}>
      <VStack spacing={4} as="form" onSubmit={handleSubmit}>
        <Heading>Login to NoteKo</Heading>
        
        <FormControl>
          <FormLabel>Email</FormLabel>
          <Input 
            type="email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </FormControl>

        <FormControl>
          <FormLabel>Password</FormLabel>
          <Input 
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </FormControl>

        <Button type="submit" colorScheme="blue" width="full">
          Login
        </Button>
      </VStack>
    </Box>
  )
}

export default LoginForm
