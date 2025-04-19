import {
  Box,
  Button,
  Container,
  Flex,
  Heading,
  Textarea,
  VStack,
} from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"

import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/content-writer")({
  component: ContentWriter,
})

function ContentWriter() {
  const { user: currentUser } = useAuth()
  const [content, setContent] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
   
  }

  return (
    <Container maxW="full">
      <Heading size="lg" pt={12} mb={6}>
        Content Writer
      </Heading>
      
      <Box as="form" onSubmit={handleSubmit}>
        
      </Box>
    </Container>
  )
}