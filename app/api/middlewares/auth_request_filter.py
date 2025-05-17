# from app.service.database_serv import get_session

# @app.middleware("http")
# async def verify_auth_header(request: Request, call_next):
#     all_access_routes = ("/auth/register", "/auth/login")
#     path = request.url.path

#     if not path.startswith(all_access_routes) and request.method != "OPTIONS":
#         jwt_token = request.headers.get("Authorization")

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
