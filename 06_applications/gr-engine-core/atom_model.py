from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class Identity(BaseModel):
    id: str
    name: str = "Unknown"
    aliases: Optional[List[str]] = []

class Classification(BaseModel):
    domain: Optional[str] = "unknown"
    type: Optional[str] = "unknown"
    abstraction_level: Optional[int] = None
    gr_coordinates: Optional[Dict[str, Any]] = None

class Relation(BaseModel):
    is_a: Optional[List[str]] = []
    requires: Optional[List[str]] = []
    causes: Optional[List[str]] = []
    enables: Optional[List[str]] = []
    prevents: Optional[List[str]] = []
    applies_to: Optional[List[str]] = []
    mitigates: Optional[List[str]] = []
    # Flexible for other relation types
    
class Definition(BaseModel):
    what: Optional[str] = ""
    why: Optional[str] = ""
    how: Optional[str] = ""

class Atom(BaseModel):
    identity: Identity
    classification: Optional[Classification] = Field(default_factory=Classification)
    definition: Optional[Definition] = Field(default_factory=Definition)
    relations: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        extra = "ignore" # Allow extra fields for forward compatibility
