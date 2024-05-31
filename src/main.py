from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from src.auth.base_config import auth_backend, fastapi_users
# from src.auth.schemas import UserRead, UserCreate
from src.user_profile.router import router as router_user_profile

from src.events.router import router as router_events
from src.reward.router import router as router_reward
from src.club.router import router as router_club
from src.mentorship.router import router as router_mentorship
from src.statistics.router import router as router_statistics
# from src.quetionnaire.router import router as router_quetionnaire
# from src.randomcofee.router import router as router_randomcofee
from src.user_club.router import router as router_user_club
from src.pages.router import router as router_pages
from src.market.router import router as router_market


app = FastAPI(
    title="Club Bot"
)

app.mount("/images", StaticFiles(directory="src/static/images"), name="images")
app.mount("/css_js", StaticFiles(directory="src/static/css_js"), name="css_js")

# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth",
#     tags=["Auth"],
# )
#
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["Auth"],
# )

app.include_router(router_user_profile)
app.include_router(router_events)
app.include_router(router_statistics)
# app.include_router(router_randomcofee)
# app.include_router(router_quetionnaire)
app.include_router(router_mentorship)
app.include_router(router_reward)
app.include_router(router_market)
app.include_router(router_club)
app.include_router(router_user_club)
app.include_router(router_pages)
