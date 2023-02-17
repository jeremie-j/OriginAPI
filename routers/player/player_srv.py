from datetime import datetime
from typing import Union, Optional
from dateutil import tz

from origin_connector import origin_api

from models.player import player
from schemas.profile import PlayerStats, CreatePlayerStats, Account, Rank, LegendSchema, Legends, Session
from schemas.base_legend import Legend

import sqlalchemy as sa
from sqlalchemy.engine import Connection
from utils.rank import get_rank

NULL_VALUE = 2147483648


def get_player_stats(uid: int, platform: str):
    data = origin_api.apex_data(uid, platform)
    if data is None or data['name'] == "":
        return None
    legend = Legend(data.get('cdata2'))

    rank_name, rank_div = get_rank(data['rankScore'])

    rank = Rank(
        rank_score=data['rankScore'],
        rank_name=rank_name,
        rank_division=rank_div)

    account = Account(username=data['name'], platform=platform, uid=uid,
                      rank=rank, level=data['cdata23']+1, level_progression=100 - data['cdata24'])

    selected_legend = LegendSchema(
        id=legend.id,
        trackers=[{'id': tracker, 'value': value} for tracker, value in
                  [
            (data.get('cdata12'), data.get('cdata13')),
            (data.get('cdata14'), data.get('cdata15')),
            (data.get('cdata16'), data.get('cdata17'))
        ] if tracker != NULL_VALUE],
        badges=[
            {'id': badge, 'value': value} for badge, value in
            [
                (data.get('cdata6'), data.get('cdata7')),
                (data.get('cdata8'), data.get('cdata9')),
                (data.get('cdata10'), data.get('cdata11'))
            ] if badge != NULL_VALUE
        ],
        skin={"id": data.get('cdata3')},
        frame={"id": data.get('cdata4')},
        intro={"id": data.get('cdata18')},
    )
    legends = Legends(selected=selected_legend, all={
                      selected_legend.id: selected_legend})
    session = Session(
        online=data['online'],
        in_match=data['partyInMatch'],
        party_joinable=data['joinable'],
        party_full=data['partyFull']
    )
    return CreatePlayerStats(
        account=account,
        legends=legends,
        session=session
    )


def parse_player_stats():
    pass


def get_player_by_id(conn: Connection, platform: str, origin_id: Optional[str] = None, uid: Optional[int] = None) -> Union[PlayerStats, None]:
    stmt = sa.select([player]).where(player.c.platform == platform)

    if origin_id is not None:
        stmt = stmt.where(player.c.origin_id == origin_id.lower())
    elif uid is not None:
        stmt = stmt.where(player.c.uid == uid)
    data = conn.execute(stmt).first()

    if data is not None:
        data = dict(data)
        return PlayerStats(**data['data'], **data)


def create_player(conn: Connection, uid: int, origin_id: Optional[str], platform: str):
    player_stats = get_player_stats(uid, platform)
    if player_stats is None:
        raise ValueError('Player not found')

    stmt = sa.insert(player, values={
        'uid': uid,
        'origin_id': origin_id.lower() if origin_id is not None else None,
        'platform': platform,
        'data': player_stats.dict(exclude_none=True),
    }).returning(player)
    data = conn.execute(stmt).first()
    if data is not None:
        data = dict(data)
        print(data)
        return PlayerStats(**data['data'], **data)


def update_player(conn: Connection, origin_id: Optional[str], player_stats: PlayerStats):
    uid = player_stats.account.uid
    platform = player_stats.account.platform
    new_stats = get_player_stats(uid, platform)
    if new_stats is None:
        raise ValueError('Player does not exist anymore')
    selected_legend = new_stats.legends.selected
    new_stats.legends.all = {**player_stats.legends.all,
                             selected_legend.name: selected_legend}
    stmt = (
        sa.update(player)
        .where(player.c.uid == player_stats.account.uid)
        .values(
            data=new_stats.dict(),
            edited_at=datetime.now(tz=tz.UTC),
            times_edited=player_stats.times_edited + 1
        )).returning(player)

    if origin_id:
        stmt = stmt.values(origin_id=origin_id.lower())

    data = conn.execute(stmt).first()
    if data is not None:
        data = dict(data)
        return PlayerStats(**data['data'], **data)
