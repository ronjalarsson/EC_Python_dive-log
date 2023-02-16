from pydantic import BaseModel, validator
from typing import Optional

# Nedan BaseModel är som en data class som vi slipper init metoder i klasser
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
    down_speed_m_per_sec: Optional[float] = None # Funkar inte. Får errors när jag skippa fylla i dessa None column
    up_speed_m_per_sec: Optional[float] = None # Funkar inte. Får errors när jag skippa fylla i dessa None column
    dive_site: str
    date: str
    diver_id: int

    #@validator('down_speed_m_per_sec', 'up_speed_m_per_sec', pre=True)
    #def validate_float(cls, v):
    #    if v is not None and not isinstance(v, float):
    #        raise ValueError('value is not a valid float')
    #    return v

class UpdateFreediveLog(BaseModel):
    id: int 
    depth_m: float = None
    discipline: str = None
    dive_time_sec: int = None
    down_speed_m_per_sec: Optional[float] = None # Funkar inte. Får errors när jag skippa fylla i dessa None column
    up_speed_m_per_sec: Optional[float] = None # Funkar inte. Får errors när jag skippa fylla i dessa None column
    dive_site: str = None
    date: str = None
    diver_id: int = None