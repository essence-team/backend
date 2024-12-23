from database.db_session_maker import close_db_connection, initialize_database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.channels import channel_router
from routers.digest import digest_router
from routers.subscription import subscription_router
from routers.user import user_router

tags_metadata = [
    {"name": "users", "description": "Operations with users. Create and update users."},
    {"name": "subscriptions", "description": "Manage user subscriptions."},
    {"name": "channels", "description": "Manage user channels."},
    {"name": "digest", "description": "Get digest for user."},
]

app = FastAPI(
    title="Essence Bot Backend",
    on_startup=[initialize_database],
    on_shutdown=[close_db_connection],
    tags_metadata=tags_metadata,
)
app.include_router(user_router)
app.include_router(subscription_router)
app.include_router(channel_router)
app.include_router(digest_router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization"],
)
