from fastapi import APIRouter, Depends
from dependencies.database import provide_session
import requests
from domains.users.services import UserService
from domains.users.repositories import UserRepository
from domains.users.dto import (
    KeyWordDataRequest, KeyWordDataResponse
)
from dependencies.kakaoapi import (search_places_nearby, get_coords_from_address)
router = APIRouter()

name = "users"

@router.post("/getinfo")
async def getInfo(
    payload:KeyWordDataRequest
):
    keywordInfor = {}
    address = []
    x = payload.data.x
    y = payload.data.y
    distance = payload.data.distan
    keyword = payload.data.keyword
    keywordInfor, address = search_places_nearby(x,y,distance,keyword)
    for i in range(len(address)):
        xy_list = get_coords_from_address(address)
        keywordInfor['x'].append(xy_list[0])
        keywordInfor['y'].append(xy_list[1])
        print(xy_list)
    print(keywordInfor)
    return KeyWordDataResponse(keywordinfo=keywordInfor)