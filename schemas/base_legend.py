from schemas.legends import ash, bangalore, bloodhound, caustic, crypto, fuse, gibraltar, horizon, lifeline, loba, mirage, octane, pathfinder, rampart, revenant, seer, valkyrie, wattson, wraith
from schemas.profile import Tracker, Badge, Skin, Frame, Intro
from typing import Optional, Dict
from pydantic import BaseModel


class BaseLegend(BaseModel):
    name: str
    trackers: Dict[int, dict]
    badges: Dict[int, dict]
    skins: Dict[int, dict]
    frames: Dict[int, dict]
    intros: Dict[int, dict]

    def get_tracker(self, id: int, value: Optional[int]):
        formated_value = str(value)[:-2]
        try:
            return Tracker(name=self.trackers[id]['name'], value=formated_value)
        except KeyError:
            return Tracker(name=f'unknown_{self.name}_tracker_{id}', value=formated_value)

    def get_badge(self, id: int, value: Optional[int]):
        try:
            return Badge(name=self.badges[id]['name'], value=value)
        except KeyError:
            return Badge(name=f'unknown_{self.name}_badge_{id}')

    def get_skin(self, id: int):
        try:
            return Skin(name=self.skins[id]['name'])
        except KeyError:
            return Skin(name=f'unknown_{self.name}_skin_{id}')

    def get_frame(self, id: int):
        try:
            return Frame(name=self.frames[id]['name'])
        except KeyError:
            return Frame(name=f'unknown_{self.name}_frame_{id}')

    def get_intro(self, id: int):
        try:
            return Intro(name=self.intros[id]['name'])
        except KeyError:
            return Intro(name=f'unknown_{self.name}_intro_{id}')


class Legend():
    items = {
        216194192: ash,
        725342087: bangalore,
        898565421: bloodhound,
        1111853120: caustic,
        80232848: crypto,
        405279270: fuse,
        182221730: gibraltar,
        88599337: horizon,
        1409694078: lifeline,
        1579967516: loba,
        2045656322: mirage,
        843405508: octane,
        1464849662: pathfinder,
        2105222312: rampart,
        64207844: revenant,
        1399802246: seer,
        435256162: valkyrie,
        187386164: wattson,
        827049897: wraith,
    }

    def __new__(cls, id: int):
        module = cls.items[id]
        return BaseLegend(
            name=module.legend_name,
            trackers=module.trackers,
            badges=module.badges,
            skins=module.skins,
            frames=module.frames,
            intros=module.intros
        )
