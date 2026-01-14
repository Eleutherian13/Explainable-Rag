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
            
            if response.choices and response.choices[0].message and response.choices[0].message.content:
                answer = response.choices[0].message.content.strip()
                return answer
            else:
                return self._generate_fallback(query, context_chunks)
            
        except APIError as e:
            print(f"OpenAI API error: {e}")
            return self._generate_fallback(query, context_chunks)
    
    def _generate_fallback(self, query: str, context_chunks: List[str]) -> str:
        """
        Fallback answer generation without LLM.
        Improved to provide diverse, complete answers.
        
        Args:
            query: User query
            context_chunks: Retrieved context chunks
            
        Returns:
            Full answer with complete content
        """
        if not context_chunks:
            return "I cannot find relevant information in the provided documents."
        
        # Extract meaningful keywords (length > 2)
        query_words = set(w.lower() for w in query.split() if len(w) > 2)
        
        # Score each chunk based on keyword overlap
        best_chunk = None
        best_score = -1
        
        for chunk in context_chunks:
            chunk_words = set(w.lower() for w in chunk.split() if len(w) > 2)
            overlap = len(query_words & chunk_words)
            if overlap > best_score:
                best_score = overlap
                best_chunk = chunk
        
        # If no overlap found, use the most relevant chunk (first retrieved)
        if best_chunk is None:
            best_chunk = context_chunks[0]
        
        # Return FULL content, find good break point at sentence
        if len(best_chunk) <= 1000:
            return best_chunk.strip()
        
        # For longer chunks, find last complete sentence
        truncated = best_chunk[:1200]
        for end_marker in ['. ', '! ', '? ', '.\n', '!\n', '?\n']:
            last_idx = truncated.rfind(end_marker)
            if last_idx > 500:  # At least 500 chars
                return best_chunk[:last_idx + 1].strip()
        
        # Fallback: return up to 1000 chars
        return best_chunk[:1000].strip()
