"""
Firebase client for real-time state management and persistence.
Implements robust error handling and reconnection logic.
"""
import json
import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import asdict, is_dataclass

import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.exceptions import GoogleCloudError

from config.settings import settings

class FirebaseManager:
    """Manages Firebase connections and provides data persistence operations."""
    
    _instance = None
    _db: Optional[FirestoreClient] = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern to prevent multiple Firebase initializations."""
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Firebase connection if not already done."""
        if not self._initialized:
            self._initialize_firebase()
            self._initialized = True
            
    def _initialize_firebase(self) -> None:
        """Initialize Firebase Admin SDK with robust error handling."""
        try:
            if not firebase_admin._apps:
                cred_path = settings.firebase.credentials_path