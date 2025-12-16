"""Base importer class for CSV/data imports"""

import csv
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod


class BaseImporter(ABC):
    """Abstract base class for data importers"""
    
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate the input file format"""
        pass
    
    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        """Parse the file and return structured data"""
        pass
    
    def read_csv(self, **kwargs) -> pd.DataFrame:
        """Read CSV file with pandas"""
        return pd.read_csv(self.file_path, **kwargs)
    
    def detect_delimiter(self) -> str:
        """Detect CSV delimiter"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            sample = f.read(1024)
            sniffer = csv.Sniffer()
            return sniffer.sniff(sample).delimiter
    
    def map_columns(self, df: pd.DataFrame, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """Map column names to standard names"""
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        # Remove unmapped columns (optional - could keep them in metadata)
        keep_columns = list(column_mapping.values())
        existing_columns = [col for col in keep_columns if col in df.columns]
        return df[existing_columns]
    
    def infer_column_mapping(self, df: pd.DataFrame, expected_columns: List[str]) -> Dict[str, str]:
        """Attempt to infer column mapping from column names"""
        mapping = {}
        df_columns_lower = {col.lower(): col for col in df.columns}
        
        for expected in expected_columns:
            # Try exact match
            if expected in df.columns:
                mapping[expected] = expected
                continue
            
            # Try case-insensitive match
            if expected.lower() in df_columns_lower:
                mapping[df_columns_lower[expected.lower()]] = expected
                continue
            
            # Try partial matches
            for col in df.columns:
                if expected.lower() in col.lower() or col.lower() in expected.lower():
                    mapping[col] = expected
                    break
        
        return mapping

