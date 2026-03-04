"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection

class Storage:
    """In-memory storage class for managing prompts and collections.

    This class simulates a database using Python dictionaries to store
    prompts and collections. It provides methods to perform CRUD
    operations on these entities.
    """
    
    def __init__(self):
        """Initialize the Storage with empty dictionaries for prompts and collections."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Store a new prompt in the storage.

        Args:
            prompt (Prompt): The prompt object to store.

        Returns:
            Prompt: The stored prompt object.
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its unique ID.

        Args:
            prompt_id (str): The unique identifier of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The prompt object if found, otherwise None.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all prompts currently stored.

        Returns:
            List[Prompt]: A list of all prompts in storage.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt's data.

        Args:
            prompt_id (str): The unique identifier of the prompt to update.
            prompt (Prompt): The updated prompt object.

        Returns:
            Optional[Prompt]: The updated prompt object if exists, otherwise None.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its unique ID.

        Args:
            prompt_id (str): The unique identifier of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, otherwise False.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Store a new collection in the storage.

        Args:
            collection (Collection): The collection object to store.

        Returns:
            Collection: The stored collection object.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its unique ID.

        Args:
            collection_id (str): The unique identifier of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection object if found, otherwise None.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all collections currently stored.

        Returns:
            List[Collection]: A list of all collections in storage.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by its unique ID.

        Args:
            collection_id (str): The unique identifier of the collection to delete.

        Returns:
            bool: True if the collection was deleted, otherwise False.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts associated with a specific collection.

        Args:
            collection_id (str): The unique identifier of the collection whose prompts to retrieve.

        Returns:
            List[Prompt]: A list of prompts associated with the specified collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self) -> None:
        """Clear all stored prompts and collections."""
        self._prompts.clear()
        self._collections.clear()

# Global storage instance
storage = Storage()
