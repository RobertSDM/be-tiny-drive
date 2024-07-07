# import json
# from service.logging_config import logger
# from fastapi import Request, Response
# from database.init_database import get_session
# from main import get_app
# from service.user_auth_serv import validate_token_serv
# from sqlalchemy.orm import Session

# app = get_app()

# @app.middleware("http")
# async def verify_auth_header(request: Request, call_next):
#     all_access_routes = ["/auth/register", "/auth/login"]
#     path = request.url.path

#     logger.info(request.method)
#     logger.info(request.url.path)

#     if path not in all_access_routes and request.method != "OPTIONS":
#         jwt_token = request.headers.get("Authentication")

#         if not jwt_token:
#             return Response(
#                 status_code=422,
#                 content=json.dumps(
#                     {"msg": "Authorization header not informed", "data": None}
#                 ),
#             )

#         db: Session = next(get_session())

#         try:
#             res = validate_token_serv(db, jwt_token)
#         finally:
#             db.close()

#         if not isinstance(res, bool):
#             return Response(
#                 status_code=res["status"], content=json.dumps(res["content"])
#             )

#     return await call_next(request)
