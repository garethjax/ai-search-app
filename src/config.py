"""
Configuration module for Research Assistant CLI
Handles environment variables and application settings securely
"""

import os
from typing import List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class LLMConfig:
    """Configuration for Language Model settings"""
    ollama_base_url: str
    ollama_model: str
    oobabooga_base_url: str
    oobabooga_model: str
    
    @classmethod
    def from_env(cls) -> 'LLMConfig':
        return cls(
            ollama_base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
            ollama_model=os.getenv('OLLAMA_MODEL', 'llama3.1:8b'),
            oobabooga_base_url=os.getenv('OOBABOOGA_BASE_URL', 'http://localhost:7860'),
            oobabooga_model=os.getenv('OOBABOOGA_MODEL', 'your_model_name_here')
        )

@dataclass
class SearchConfig:
    """Configuration for search engine settings"""
    brave_api_key: Optional[str]
    searx_instances: List[str]
    default_engines: List[str]
    max_results: int
    request_timeout: int
    
    @classmethod
    def from_env(cls) -> 'SearchConfig':
        searx_instances_str = os.getenv('SEARX_INSTANCES', '')
        searx_instances = [instance.strip() for instance in searx_instances_str.split(',') if instance.strip()]
        
        default_engines_str = os.getenv('DEFAULT_ENGINES', 'searx,brave,yahoo,startpage')
        default_engines = [engine.strip() for engine in default_engines_str.split(',') if engine.strip()]
        
        return cls(
            brave_api_key=os.getenv('BRAVE_API_KEY'),
            searx_instances=searx_instances,
            default_engines=default_engines,
            max_results=int(os.getenv('MAX_RESULTS', '8')),
            request_timeout=int(os.getenv('REQUEST_TIMEOUT', '12'))
        )

@dataclass
class AppConfig:
    """Main application configuration"""
    log_level: str
    default_output_dir: str
    save_results: bool
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        return cls(
            log_level=os.getenv('LOG_LEVEL', 'INFO').upper(),
            default_output_dir=os.getenv('DEFAULT_OUTPUT_DIR', './results'),
            save_results=os.getenv('SAVE_RESULTS', 'false').lower() == 'true'
        )

class Config:
    """Main configuration class that combines all settings"""
    
    def __init__(self):
        self.llm = LLMConfig.from_env()
        self.search = SearchConfig.from_env()
        self.app = AppConfig.from_env()
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of warnings"""
        warnings = []
        
        # Check for required API keys
        if not self.search.brave_api_key:
            warnings.append("BRAVE_API_KEY not set - Brave Search will be disabled")
        
        # Check for valid log level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        if self.app.log_level not in valid_log_levels:
            warnings.append(f"Invalid LOG_LEVEL '{self.app.log_level}', using INFO")
            self.app.log_level = 'INFO'
        
        # Check for valid max_results
        if self.search.max_results < 1 or self.search.max_results > 20:
            warnings.append(f"MAX_RESULTS should be between 1-20, got {self.search.max_results}")
            self.search.max_results = min(max(self.search.max_results, 1), 20)
        
        # Check for valid timeout
        if self.search.request_timeout < 5 or self.search.request_timeout > 60:
            warnings.append(f"REQUEST_TIMEOUT should be between 5-60 seconds, got {self.search.request_timeout}")
            self.search.request_timeout = min(max(self.search.request_timeout, 5), 60)
        
        return warnings
    
    def get_brave_api_key(self) -> Optional[str]:
        """Safely get Brave API key with validation"""
        key = self.search.brave_api_key
        if key and key.strip() and key != 'your_brave_api_key_here':
            return key.strip()
        return None
    
    def get_searx_instances(self) -> List[str]:
        """Get validated SearX instances"""
        if not self.search.searx_instances:
            # Fallback to default instances
            return [
                'https://searx.be',
                'https://search.sapti.me',
                'https://searx.prvcy.eu',
                'https://searx.tiekoetter.com',
                'https://northboot.xyz',
                'https://searx.work'
            ]
        return self.search.searx_instances

# Global configuration instance
config = Config() 