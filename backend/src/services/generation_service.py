import cohere
from typing import List, Dict, Any
from ..core.config import settings
from ..models.query import QueryResponse


class GenerationService:
    def __init__(self):
        self.client = cohere.Client(settings.cohere_api_key)

    def generate_response(
        self, 
        query: str, 
        context_chunks: List[Dict[str, Any]], 
        selected_text: str = None
    ) -> QueryResponse:
        """
        Generate a response using Cohere based on the query and context chunks.
        """
        # Prepare the context for the LLM
        context = "\n\n".join([chunk["content"] for chunk in context_chunks])
        
        # If selected text is provided, prioritize it in the context
        if selected_text:
            # For selected-text queries, we focus only on the selected text
            context = selected_text
        
        # Construct the prompt for the LLM
        if selected_text:
            # For selected-text queries, we only use the selected text
            prompt = f"""
            Based only on the following selected text from the book, answer the question.
            Do not use any external knowledge or information beyond what is provided.
            
            Selected text: {selected_text}
            
            Question: {query}
            
            Answer: """
        else:
            # For full-book queries, we use the retrieved context
            prompt = f"""
            Based only on the following context from the book, answer the question.
            Do not use any external knowledge or information beyond what is provided.
            
            Context: {context}
            
            Question: {query}
            
            Answer: """
        
        try:
            # Generate the response using Cohere
            response = self.client.generate(
                model='command',
                prompt=prompt,
                max_tokens=300,
                temperature=0.3,
                stop_sequences=["\n\n"]
            )
            
            # Extract the generated text
            generated_text = response.generations[0].text.strip()
            
            # Check if the response indicates information is not available
            if "not available in the provided book content" in generated_text.lower() or \
               "not mentioned in the text" in generated_text.lower():
                # This means the information wasn't found in the context
                return QueryResponse(
                    response="This information is not available in the provided book content.",
                    sources=[],
                    session_id=""  # Will be set by the calling function
                )
            
            # Prepare sources for the response
            sources = [
                {
                    "chunkId": chunk.get("id", ""),
                    "content": chunk.get("content", "")[:100] + "...",  # Truncate for brevity
                    "relevanceScore": chunk.get("relevance_score", 0.0)
                }
                for chunk in context_chunks
            ]
            
            return QueryResponse(
                response=generated_text,
                sources=sources,
                session_id=""  # Will be set by the calling function
            )
            
        except Exception as e:
            # Handle any errors from the Cohere API
            return QueryResponse(
                response="An error occurred while generating the response. Please try again.",
                sources=[],
                session_id=""
            )

    def check_hallucination(self, response: str, context: List[Dict[str, Any]]) -> bool:
        """
        Basic check to see if the response contains information not in the context.
        This is a simplified check - a full implementation would use more sophisticated methods.
        """
        # For now, we'll just return False (no hallucination detected)
        # In a real implementation, we would compare the response to the context
        return False