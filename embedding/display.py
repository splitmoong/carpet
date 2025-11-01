import os
from chromadb import PersistentClient
from typing import Optional


class Display:
    
    def __init__(self):
        """Initialize ChromaDB client."""
        home = os.path.expanduser("~")
        # Use fixed chroma store path instead of reading from environment
        chroma_path = os.path.join(home, "chroma_store")
        if not chroma_path.startswith("/"):
            chroma_path = os.path.join(home, chroma_path.lstrip("./"))
        
        self.client = PersistentClient(path=chroma_path)
        self.collection = self.client.get_or_create_collection("user_files")
    
    def show_all(self):
        """Display all documents in ChromaDB with their metadata."""
        try:
            # Get all documents from the collection
            results = self.collection.get()
            
            if not results['ids']:
                print("📦 ChromaDB is empty. No documents found.")
                return
            
            total_docs = len(results['ids'])
            # Compute total unique source files (if metadata is present)
            total_files = 0
            if results.get('metadatas'):
                total_files = len({m.get('source', 'Unknown') for m in results['metadatas'] if m})

            print(f"📊 ChromaDB Contents ({total_files} files, {total_docs} chunks)")
            print("=" * 80)
            
            # Group by source file
            sources = {}
            for i, doc_id in enumerate(results['ids']):
                metadata = results['metadatas'][i] if results['metadatas'] else {}
                source = metadata.get('source', 'Unknown')
                
                if source not in sources:
                    sources[source] = []
                
                sources[source].append({
                    'id': doc_id,
                    'document': results['documents'][i] if results['documents'] else None,
                    'metadata': metadata
                })
            
            # Display grouped by source
            for source, chunks in sources.items():
                print(f"\n📄 Source: {source}")
                print(f"   Chunks: {len(chunks)}")
                print("-" * 80)
                
                for chunk in chunks:
                    chunk_idx = chunk['metadata'].get('chunk_index', 'N/A')
                    total_chunks = chunk['metadata'].get('total_chunks', 'N/A')
                    doc_preview = chunk['document'][:100] if chunk['document'] else "No content"
                    
                    print(f"\n   Chunk {chunk_idx + 1}/{total_chunks}")
                    print(f"   ID: {chunk['id']}")
                    print(f"   Preview: {doc_preview}...")
            
            print("\n" + "=" * 80)
            print(f"Total: {total_docs} chunks from {len(sources)} source(s)")
            
        except Exception as e:
            print(f"❌ Error displaying ChromaDB contents: {e}")
    
    def show_sources(self):
        """Display just the list of source files."""
        try:
            results = self.collection.get()
            
            if not results['ids']:
                print("\n📦 No documents found in ChromaDB.")
                return
            
            # Extract unique sources
            sources = set()
            chunk_counts = {}
            
            for i, metadata in enumerate(results['metadatas']):
                if metadata:
                    source = metadata.get('source', 'Unknown')
                    sources.add(source)
                    chunk_counts[source] = chunk_counts.get(source, 0) + 1
            
            print(f"\n📚 Source Files in ChromaDB ({len(sources)} files)")
            print("=" * 80)
            
            for source in sorted(sources):
                chunks = chunk_counts.get(source, 0)
                print(f"   • {source} ({chunks} chunks)")
            
            print("=" * 80)
            
        except Exception as e:
            print(f"❌ Error listing sources: {e}")
    
    def show_stats(self):
        """Display statistics about ChromaDB."""
        try:
            results = self.collection.get()
            
            if not results['ids']:
                print("\n📦 ChromaDB is empty.")
                return
            
            # Calculate statistics
            total_chunks = len(results['ids'])
            sources = set()
            total_chars = 0
            
            for i, metadata in enumerate(results['metadatas']):
                if metadata:
                    sources.add(metadata.get('source', 'Unknown'))
                if results['documents'] and results['documents'][i]:
                    total_chars += len(results['documents'][i])
            
            avg_chunk_size = total_chars / total_chunks if total_chunks > 0 else 0
            
            print(f"\n📈 ChromaDB Statistics")
            print("=" * 80)
            print(f"   Total Chunks: {total_chunks}")
            print(f"   Unique Files: {len(sources)}")
            print(f"   Total Characters: {total_chars:,}")
            print(f"   Avg Chunk Size: {avg_chunk_size:.0f} characters")
            print("=" * 80)
            
        except Exception as e:
            print(f"❌ Error calculating stats: {e}")
    
    def clear_all(self, confirm: bool = False):
        """Clear all documents from ChromaDB."""
        if not confirm:
            print("\n⚠️  Warning: This will delete all documents from ChromaDB!")
            response = input("Are you sure? (yes/no): ").strip().lower()
            if response != 'yes':
                print("❌ Cancelled.")
                return
        
        try:
            results = self.collection.get()
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                print(f"✅ Deleted {len(results['ids'])} chunks from ChromaDB.")
            else:
                print("📦 ChromaDB is already empty.")
                
        except Exception as e:
            print(f"❌ Error clearing ChromaDB: {e}")