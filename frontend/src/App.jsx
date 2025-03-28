import { Box } from '@chakra-ui/react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './pages/auth/LoginPage'

function App() {
  return (
    <BrowserRouter>
      <Box minH="100vh">
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </Box>
    </BrowserRouter>
  )
}

export default App