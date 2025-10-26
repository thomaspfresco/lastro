'''
/ai/nlp/setup.py
-> NLP-powered video search engine for natural language queries
'''

from sentence_transformers import SentenceTransformer
import numpy as np
import re

class VideoSearchEngine:
    def __init__(self):
        """Initialize the NLP search engine"""
        # Load multilingual model with better quality (Portuguese + English)
        # Model downloads ~420MB on first run (better accuracy than MiniLM)
        print("Loading NLP model...")
        self.model = SentenceTransformer('intfloat/multilingual-e5-large')
        
        self.projects_cache = []
        self.project_embeddings = None
        print("NLP model loaded successfully")
    
    def load_projects(self, projects):
        """Load projects and compute embeddings for semantic search"""
        from database.models import Project
        
        if isinstance(projects, list) and len(projects) > 0 and isinstance(projects[0], Project):
            # Convert SQLAlchemy objects to dictionaries
            self.projects_cache = [project.serialize() for project in projects]
        else:
            self.projects_cache = projects
        
        if not self.projects_cache:
            print("Warning: No projects loaded")
            return
        
        # Create rich text representations for semantic matching
        project_texts = []
        for project in self.projects_cache:
            # Combine all textual information
            text_parts = [
                str(project.get('title', '')),
                str(project.get('author', '')),
                str(project.get('category', '')),
                str(project.get('keywords', '')),
                str(project.get('location', '')),
                str(project.get('instruments', '')),
                str(project.get('infoPool', ''))
            ]
            text = ' '.join([part for part in text_parts if part and part != 'None'])
            project_texts.append(text)
        
        # Pre-compute embeddings for all projects
        print(f"Computing embeddings for {len(self.projects_cache)} projects...")
        self.project_embeddings = self.model.encode(
            project_texts, 
            show_progress_bar=False,
            convert_to_numpy=True
        )
        print(f"Embeddings computed successfully")
    
    def extract_keywords(self, prompt):
        """Extract meaningful keywords from casual language"""
        prompt_lower = prompt.lower()
        
        # Remove common filler words in Portuguese and English
        stop_words = {
            # Portuguese
            'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'da', 'do', 'das', 'dos',
            'em', 'no', 'na', 'nos', 'nas', 'para', 'por', 'com', 'sem',
            'que', 'qual', 'quais', 'onde', 'quando', 'como', 'quero', 'gostaria',
            'mostre', 'mostra', 'encontre', 'procuro', 'busco', 'vídeo', 'vídeos',
            'ver', 'assistir', 'me', 'sobre', 'acerca', 'tem', 'tens', 'há',
            'existe', 'existem', 'algum', 'alguma', 'alguns', 'algumas',
            'projeto', 'projetos', 'conteúdo', 'conteúdos',
            # English  
            'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'with',
            'from', 'by', 'about', 'show', 'find', 'video', 'videos', 'want',
            'would', 'like', 'me', 'some', 'any', 'is', 'are', 'there', 'have',
            'project', 'projects', 'content'
        }
        
        # Tokenize and filter
        words = re.findall(r'\b\w+\b', prompt_lower)
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords
    
    def fuzzy_text_match(self, project, keywords):
        """Check if project matches any keywords (fuzzy matching)"""
        # Combine all project text fields
        project_text = ' '.join([
            str(project.get('title', '')),
            str(project.get('author', '')),
            str(project.get('category', '')),
            str(project.get('keywords', '')),
            str(project.get('location', '')),
            str(project.get('instruments', ''))
        ]).lower()
        
        # Count keyword matches
        matches = 0
        for keyword in keywords:
            if keyword in project_text:
                matches += 1
        
        return matches
    
    def expand_context_with_history(self, prompt, conversation_context):
        """Expand the current prompt with conversation history"""
        if not conversation_context:
            return prompt
        
        # Get last 3 prompts to build context
        recent_prompts = [msg.get('prompt', '') for msg in conversation_context[-3:]]
        
        # Check for continuation words
        continuation_words = [
            'também', 'ainda', 'mais', 'outro', 'outra', 'outros', 'outras',
            'agora', 'depois', 'então', 'e', 'mas', 'porém', 'só',
            'also', 'too', 'another', 'more', 'now', 'then', 'and', 'but', 'only'
        ]
        
        prompt_lower = prompt.lower()
        is_continuation = any(prompt_lower.startswith(word) for word in continuation_words)
        
        if is_continuation or len(prompt.split()) < 5:
            # Likely a continuation, combine with previous context
            combined = ' '.join(recent_prompts + [prompt])
            return combined
        
        return prompt
    
    def semantic_search(self, prompt, top_k=50):
        """Perform semantic search across all projects"""
        if self.project_embeddings is None or len(self.projects_cache) == 0:
            return []
        
        # Encode the prompt
        prompt_embedding = self.model.encode([prompt], convert_to_numpy=True)
        
        # Compute cosine similarities with all projects
        similarities = np.dot(self.project_embeddings, prompt_embedding.T).flatten()
        
        # Get top-k most similar
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if idx < len(self.projects_cache):
                project = self.projects_cache[idx].copy()
                project['semantic_score'] = float(similarities[idx])
                results.append(project)
        
        return results
    
    def hybrid_search(self, prompt, keywords):
        """Combine semantic search with keyword matching"""
        # Get semantic search results
        semantic_results = self.semantic_search(prompt, top_k=100)
        
        if not semantic_results:
            return []
        
        # Re-rank based on keyword matches and semantic similarity
        for project in semantic_results:
            keyword_matches = self.fuzzy_text_match(project, keywords)
            
            # Hybrid score: 80% semantic, 20% keyword matches
            # Increased semantic weight since we have a better model
            semantic_weight = 0.8
            keyword_weight = 0.2
            
            normalized_keywords = min(keyword_matches / max(len(keywords), 1), 1.0) if keywords else 0
            project['relevance_score'] = (
                semantic_weight * project['semantic_score'] +
                keyword_weight * normalized_keywords
            )
        
        # Sort by hybrid score
        semantic_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return semantic_results
    
    def search(self, prompt, conversation_context=None, max_results=10):
        """
        Main search function - works with natural, casual language
        
        Args:
            prompt (str): User's natural language query
            conversation_context (list): Previous conversation messages
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of matching projects with relevance scores
        """
        if not self.projects_cache:
            return []
        
        # Expand prompt with conversation context
        expanded_prompt = self.expand_context_with_history(prompt, conversation_context)
        
        # Extract keywords for hybrid matching
        keywords = self.extract_keywords(expanded_prompt)
        
        # Perform hybrid search
        results = self.hybrid_search(expanded_prompt, keywords)
        
        # Return top results
        return results[:max_results]


# Global search engine instance
search_engine = None

def initNLP():
    """Initialize the NLP search engine"""
    global search_engine
    
    if search_engine is None:
        search_engine = VideoSearchEngine()
        print("NLP search engine initialized")
    
    return search_engine

def get_search_engine():
    """Get the global search engine instance"""
    global search_engine
    
    if search_engine is None:
        return initNLP()
    
    return search_engine

def refresh_project_embeddings():
    """
    Refresh project embeddings from database
    Call this after database updates
    """
    from database.models import Project
    
    engine = get_search_engine()
    projects = Project.query.all()
    engine.load_projects(projects)
    print(f"Refreshed embeddings for {len(projects)} projects")