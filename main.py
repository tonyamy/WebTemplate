import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware

from RequestModel.ReqModel import TokenRequest
from Service.UserService import userLogin
from TokenAuth.auth import create_access_token, create_refresh_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])


@app.post("/login", response_model=dict)
def login_for_access_token(form_data: TokenRequest):
    user = userLogin(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token, expire = create_access_token(data={"sub": user['username']})

    refresh_token = create_refresh_token(data={"sub": user['username']})
    return {
        'success': True,
        'data': {
            'avatar': "https://avatars.githubusercontent.com/u/44761321",
            'username': user['username'],
            'nickname': user['nickname'],
            'roles': [user['roles']],
            'accessToken': access_token,
            'refreshToken': refresh_token,
            'expires': expire.strftime("%Y/%m/%d %H:%M:%S")
        }
    }

    # @app.get("/")
    # async def root():
    #     return {"message": "Hello World"}
    #
    #
    # @app.get("/hello/{name}")
    # async def say_hello(name: str):
    #     return {"message": f"Hello {name}"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
