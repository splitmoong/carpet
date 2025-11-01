from os import path
from typing import Callable, List
import os
import ollama as ollama_client
from chromadb import PersistentClient
from database.db_manager import DbManager


class Embedder:

    def __init__(self):
        self.handlers: dict[str, Callable[[str], None]] = {
            ".pdf": self._embed_pdf,
            ".txt": self._embed_txt
        }
        
        # initialize ChromaDB client
        home = os.path.expanduser("~")
        
        # Use fixed chroma store path (no environment lookup)
        chroma_path = os.path.join(home, "chroma_store")
        if not chroma_path.startswith("/"):
            chroma_path = os.path.join(home, chroma_path.lstrip("./"))
        
        self.client = PersistentClient(path=chroma_path)
        self.collection = self.client.get_or_create_collection("user_files")
        self.model = "qllama/bge-m3"

    def _embed_pdf(self, file_path: str):
        from extract.pdf.extract_preprocess_pdf import extract_and_preprocess
        txt = extract_and_preprocess(file_path)
        self._chunk_and_embed(txt, file_path)
    
    def _embed_txt(self, file_path: str):
        """Read text file and chunk + embed it."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            self._chunk_and_embed(text, file_path)
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    def _chunk_and_embed(self, text: str, source_file: str, chunk_size: int = 500, overlap: int = 50):
        """
        Chunk text with overlap and embed each chunk using ollama.
        
        Args:
            text: The text to chunk and embed
            source_file: The source file path for metadata
            chunk_size: Number of characters per chunk
            overlap: Number of characters to overlap between chunks
        """
        chunks = self._create_overlapping_chunks(text, chunk_size, overlap)
        print(f"Created {len(chunks)} chunks from {source_file}")
        
        #get embeddings for each chunk
        for i, chunk in enumerate(chunks):
            try:
                # Generate embedding using ollama
                embedding = self._get_embedding(chunk)
                
                # Store in ChromaDB with metadata
                self.collection.add(
                    ids=[f"{source_file}_chunk_{i}"],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{
                        "source": source_file,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }]
                )
                print(f"Embedded chunk {i+1}/{len(chunks)} from {source_file}")
                
            except Exception as e:
                print(f"Error embedding chunk {i} from {source_file}: {e}")
    
    def _create_overlapping_chunks(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: The text to chunk
            chunk_size: Number of characters per chunk
            overlap: Number of characters to overlap
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            if chunk.strip(): 
                chunks.append(chunk)
            
            start += (chunk_size - overlap)
        
        return chunks
    
    def _get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector for text using ollama model.
        
        Args:
            text: The text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        response = ollama_client.embeddings(
            model=self.model,
            prompt=text
        )
        return response['embedding']
    
    

    def embed(self, file_path: str):
        """
        Embed a file into ChromaDB. Checks if file already exists before embedding.
        
        Args:
            file_path: Path to the file to embed
        """
        # Check if file already exists in ChromaDB
        if DbManager.checkKey(file_path):
            print(f"⏭️  Skipping {file_path} - already embedded in database")
            return
        
        ext = path.splitext(file_path)[1].lower()

        if ext in self.handlers:
            print(f"📄 Embedding {file_path}...")
            self.handlers[ext](file_path)
        else:
            print(f"⚠️  Skipping unsupported file type: {file_path}")
    
    def search(self, query_text: str, n_results: int = 5):
        """
        Search for similar documents using vector similarity.
        
        Args:
            query_text: The text query to search for
            n_results: Number of top results to return (default: 5)
            
        Returns:
            dict: Dictionary containing:
                - sources: List of unique source file paths
                - results: Full ChromaDB query results with distances, documents, and metadatas
        """
        try:
            # Get embedding for the query text
            print(f"🔍 Searching for: {query_text}")
            query_embedding = self._get_embedding(query_text)
            
            # Query ChromaDB for similar vectors
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            if not results['ids'] or not results['ids'][0]:
                print("❌ No results found")
                return {'sources': [], 'results': results}
            
            # Extract unique source file paths
            sources = set()
            for metadata_list in results['metadatas']:
                for metadata in metadata_list:
                    if metadata and 'source' in metadata:
                        sources.add(metadata['source'])
            
            sources_list = list(sources)
            
            # Display results
            print(f"\n✅ Found {len(results['ids'][0])} matching chunks from {len(sources_list)} file(s)")
            print("=" * 80)
            
            for i, doc_id in enumerate(results['ids'][0]):
                distance = results['distances'][0][i] if results.get('distances') else None
                document = results['documents'][0][i] if results.get('documents') else None
                metadata = results['metadatas'][0][i] if results.get('metadatas') else {}
                
                source = metadata.get('source', 'Unknown')
                chunk_idx = metadata.get('chunk_index', 'N/A')
                
                print(f"\n🎯 Result #{i+1}")
                print(f"   Source: {source}")
                print(f"   Chunk: {chunk_idx}")
                if distance is not None:
                    print(f"   Distance: {distance:.4f}")
                if document:
                    preview = document[:200].replace('\n', ' ')
                    print(f"   Preview: {preview}...")
            
            print("\n" + "=" * 80)
            print(f"📁 Relevant files: {', '.join(sources_list)}")
            
            return {
                'sources': sources_list,
                'results': results
            }
            
        except Exception as e:
            print(f"❌ Error during search: {e}")
            return {'sources': [], 'results': None}
