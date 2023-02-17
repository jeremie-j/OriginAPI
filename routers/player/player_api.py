from typing import Optional
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from origin_connector import origin_api
from schemas.profile import PlayerStats
from routers.player import player_srv
from db.session import engine

router = APIRouter(
    prefix="/player",
    tags=["Player"],
)


@router.get("", response_model=PlayerStats)
async def get_infos(
    origin_id: Optional[str] = None,
    uid: Optional[int] = None,
    platform: str = 'PC'
):
    if origin_id is None and uid is None:
        raise HTTPException(400, 'Expected value for username or uid')

    try:
        with engine.begin() as conn:
            player_stats = player_srv.get_player_by_id(
                conn, platform, origin_id=origin_id, uid=uid)
            if player_stats:
                print('Player found, updating')
                return player_srv.update_player(conn, origin_id, player_stats)
            elif uid is None:
                print('No uid, searching uid by origin_id')
                uid = origin_api.get_uid(origin_id)
                if uid is None:
                    raise HTTPException(
                        404, 'No Origin account found for this username'
                    )
                player_stats = player_srv.get_player_by_id(
                    conn, platform, uid=uid
                )
                if player_stats is not None:
                    print('Player found by uid')
                    return player_srv.update_player(conn, origin_id, player_stats)
            a = player_srv.create_player(conn, uid, origin_id, platform)
            if a is not None:
                return a.dict(exclude_none=True)

    except ValueError as e:
        raise HTTPException(400)
