import { useState } from 'react'
import { ChakraProvider, Text } from '@chakra-ui/react'
import Home from './pages/home'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <ChakraProvider>
        <Home/>
      </ChakraProvider>
  )
}

export default App
