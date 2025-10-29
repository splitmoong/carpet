import os
from chromadb import PersistentClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DbManager:
    """static class for managing ChromaDB operations."""
    
    _client = None
    _collection = None
    
    @staticmethod
    def _get_client():
        """Initialize and return ChromaDB client (singleton pattern)."""
        if DbManager._client is None:
            home = os.path.expanduser("~")
            chroma_path = os.getenv("CHROMA_PATH", "chroma_store")
            
            # If relative path, make it relative to home directory
            if not chroma_path.startswith("/"):
                chroma_path = os.path.join(home, chroma_path)
            
            DbManager._client = PersistentClient(path=chroma_path)
        
        return DbManager._client
    
    @staticmethod
    def _get_collection():
        """Get or create the user_files collection."""
        if DbManager._collection is None:
            client = DbManager._get_client()
            DbManager._collection = client.get_or_create_collection("user_files")
        
        return DbManager._collection
    
    @staticmethod
    def checkKey(filepath: str) -> bool:
        """
        Check if a key (document ID) exists in ChromaDB.
        
        Args:
            filepath: The file path to check for existence
            
        Returns:
            bool: True if any chunks from this file exist, False otherwise
        """
        try:
            collection = DbManager._get_collection()
            #get all documents
            results = collection.get()
            
            if not results['ids']:
                return False
            
            #check if any document ID contains the filepath
            for doc_id in results['ids']:
                if filepath in doc_id:
                    return True
            
            #also check metadata for exact source match
            if results['metadatas']:
                for metadata in results['metadatas']:
                    if metadata and metadata.get('source') == filepath:
                        return True
            
            return False
            
        except Exception as e:
            print(f"Error checking key in ChromaDB: {e}")
            return False
    
    @staticmethod
    def get_chunks_by_file(filepath: str):
        """
        Get all chunks for a specific file.
        
        Args:
            filepath: The file path to retrieve chunks for
            
        Returns:
            dict: Dictionary with ids, documents, metadatas, and embeddings
        """
        try:
            collection = DbManager._get_collection()
            results = collection.get()
            
            if not results['ids']:
                return {'ids': [], 'documents': [], 'metadatas': [], 'embeddings': []}
            
            # Filter results for this file
            filtered = {'ids': [], 'documents': [], 'metadatas': [], 'embeddings': []}
            
            for i, metadata in enumerate(results['metadatas']):
                if metadata and metadata.get('source') == filepath:
                    filtered['ids'].append(results['ids'][i])
                    if results['documents']:
                        filtered['documents'].append(results['documents'][i])
                    if results['metadatas']:
                        filtered['metadatas'].append(results['metadatas'][i])
                    if results.get('embeddings'):
                        filtered['embeddings'].append(results['embeddings'][i])
            
            return filtered
            
        except Exception as e:
            print(f"Error retrieving chunks: {e}")
            return {'ids': [], 'documents': [], 'metadatas': [], 'embeddings': []}
    
    @staticmethod
    def deleteByFile(filepath: str) -> bool:
        """
        Delete all chunks associated with a file.
        
        Args:
            filepath: The file path to delete chunks for
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            collection = DbManager._get_collection()
            chunks = DbManager.get_chunks_by_file(filepath)
            
            if chunks['ids']:
                collection.delete(ids=chunks['ids'])
                print(f"Deleted {len(chunks['ids'])} chunks for {filepath}")
                return True
            else:
                print(f"No chunks found for {filepath}")
                return False
                
        except Exception as e:
            print(f"Error deleting chunks: {e}")
            return False