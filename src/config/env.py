from __future__ import annotations

import os
from dotenv import load_dotenv

class EnvConfig:
    """Class responsible for loading environment variables"""
    
    DEFAULT_PORT = 5050
    
    def __init__(self) -> None:
        self._load_env()
        
    def _load_env(self) -> None:
        """
        Loads environment variables
        """
        
        dotenv_path = os.getenv("DOTENV_FILE")
        load_dotenv(dotenv_path=dotenv_path)
        
        self._issuer_base_url = os.getenv('ISSUER_BASE_URL')
        assert self._issuer_base_url is not None, "Issuer base URL is not set"
        
        self._port = os.getenv('PORT')
        if self._port is None:
            self._port = EnvConfig.DEFAULT_PORT
            
        self._issuer_id = os.getenv('ISSUER_ID')
        self._eth_provider = os.getenv('ETHPROVIDER')
        self._private_key = os.getenv('PRIVATE_KEY')
        self._oracle_address = os.getenv('ORACLE_ADDRESS')
        self._contest_address = os.getenv('CONTEST_ADDRESS')
        
    @property
    def issuer_base_url(self) -> str:
        """
        Returns the issuer base URL
        """
        
        return self._issuer_base_url
    
    @property
    def issuer_id(self) -> str:
        """
        Returns the issuer ID
        """
        
        return self._issuer_id
    
    @property
    def api_port(self) -> int:
        """
        Returns the API port
        """
        
        return self._port

    @property
    def eth_provider(self) -> str:
        return self._eth_provider

    @property
    def private_key(self) -> str:
        return self._private_key

    @property
    def oracle_address(self) -> str:
        return self._oracle_address

    @property
    def contest_address(self) -> str:
        return self._contest_address
