# BaseModel är en datamodell som fungerar som en dataklass som inte behöver init-metoder
from pydantic import BaseModel, validator
from typing import Optional, Union

# Nedan är pydantic datamodeller som kommer fr BaseModel
class Freediver(BaseModel):
    id: int = None
    first_name: str
    last_name:str
    age: int

class UpdateFreediver (BaseModel):
    id: int 
    first_name: str = None
    last_name:str = None
    age: int = None

class FreediveLog(BaseModel):
    id: int = None
    depth_m: float
    discipline: str
    dive_time_sec: int
    down_speed_m_per_sec: Optional[Union[float, None]] = None 
    up_speed_m_per_sec: Optional[Union[float, None]] = None 
    dive_site: str
    date: str
    diver_id: int

    # Kollar om data är en tom sträng, om ja, returnerar "None" -> konverterar all tomma strängar för down_speed o up_speed kolunmer
    # Detta säkerställer att värde i dessa kolunmer alltid är float eller None
    @validator('down_speed_m_per_sec', 'up_speed_m_per_sec', pre=True)
    def validate_optional_fields(cls, v):
        if v == "":
            return None
        return v

class UpdateFreediveLog(BaseModel):
    id: int 
    depth_m: float = None
    discipline: str = None
    dive_time_sec: int = None
    down_speed_m_per_sec: Optional[Union[float, None]] = None 
    up_speed_m_per_sec: Optional[Union[float, None]] = None 
    dive_site: str = None
    date: str = None
    diver_id: int = None