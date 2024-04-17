from fastapi import APIRouter

from app.services.dbsession import DBSessionDep
from app.schemas.user import UserRecord
from app.services.user import get_user

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


# all the db_session.commit should goes here not in services side.
@router.get(
    "/{user_id}",
    response_model=UserRecord
)
async def user_details(
    user_id: int,
    db_session: DBSessionDep,
):
    """
    Get any user details
    """
    user = await get_user(db_session, user_id)
    return user
