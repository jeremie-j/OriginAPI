from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class Tracker(BaseModel):
    id: Optional[int]
    name: Optional[str]
    value: Optional[int]


class Badge(BaseModel):
    id: Optional[int]
    name: Optional[str]
    value: Optional[int]


class Skin(BaseModel):
    id: Optional[int]
    name: Optional[str]
    rarity: str = 'to_implement'


class Frame(BaseModel):
    id: Optional[int]
    name: Optional[str]
    rarity: str = 'to_implement'


class Intro(BaseModel):
    id: Optional[int]
    name: Optional[str]
    rarity: str = 'to_implement'


class Pose(BaseModel):
    id: Optional[int]
    name: Optional[str]
    rarity: str = 'to_implement'


class Rank(BaseModel):
    rank_score: int
    rank_name: str
    rank_division: int


class LegendSchema(BaseModel):
    id: Optional[int]
    name: Optional[str]
    trackers: List[Tracker]
    badges: List[Badge]
    skin: Skin
    frame: Frame
    intro: Intro
    pose: Optional[Pose]


class Legends(BaseModel):
    selected: LegendSchema
    all: Dict[str, LegendSchema]


class Account(BaseModel):
    username: str
    platform: str
    uid: int
    level: int
    level_progression: int
    #time_since_server_change: int
    rank: Rank


class Session(BaseModel):
    online: bool
    in_match: bool
    party_joinable: bool
    party_full: bool


class CreatePlayerStats(BaseModel):
    account: Account
    legends: Legends
    session: Session


class PlayerStats(CreatePlayerStats):
    created_at: datetime
    edited_at: datetime
    times_edited: int
