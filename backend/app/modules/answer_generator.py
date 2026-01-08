"""
Answer generation module with LLM integration.
"""
from typing import List, Optional
import os
from openai import OpenAI, APIError


class AnswerGenerator:
    """Generate answers using LLM with retrieved context."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize answer generator.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model name to use
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
    
    def generate(self, query: str, context_chunks: List[str], max_tokens: int = 500) -> str:
        """
        Generate answer from query and context.
        
        Args:
            query: User query
            context_chunks: Retrieved context chunks
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated answer
        """
        if not self.client:
            return self._generate_fallback(query, context_chunks)
        
        # Prepare context
        context = "\n\n".join(context_chunks)
        context = context[:4000]  # Limit context size
        
        # Create prompt
        system_prompt = """You are a helpful assistant that answers questions using only the provided context. 
        Do not use external knowledge. If the answer is not in the context, say "I cannot find this information in the provided documents."
        Be concise and accurate."""
        
        user_prompt = f"""Context:
{context}

Question: {query}

Answer:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )
            
            answer = response.choices[0].message.content.strip()
            return answer
            
        except APIError as e:
            print(f"OpenAI API error: {e}")
            return self._generate_fallback(query, context_chunks)
    
    def _generate_fallback(self, query: str, context_chunks: List[str]) -> str:
        """
        Fallback answer generation without LLM.
        
        Args:
            query: User query
            context_chunks: Retrieved context chunks
            
        Returns:
            Simple extraction-based answer
        """
        # Simple heuristic: return first chunk containing query keywords
        query_words = set(query.lower().split())
        
        for chunk in context_chunks:
            chunk_words = set(chunk.lower().split())
            overlap = len(query_words & chunk_words)
            if overlap > len(query_words) * 0.3:  # 30% word overlap
                return chunk[:300] + "..."
        
        # If no match, return first chunk
        if context_chunks:
            return context_chunks[0][:300] + "..."
        
        return "I cannot find relevant information in the provided documents."
