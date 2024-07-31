import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.cors import CORSMiddleware

from RequestModel.ReqModel import TokenRequest
from Service.UserService import userLogin
from TokenAuth.auth import create_access_token, create_refresh_token, verify_token
from Utils.Exceptions import CustomHTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/refresh-token")

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])


async def get_current_user(authorization: str = Depends(oauth2_scheme)):
    refreshToken, param = get_authorization_scheme_param(authorization)
    user_info = verify_token(refreshToken)
    if user_info:
        return user_info
    else:
        raise CustomHTTPException(status_code=401, content={
            "success": False,
            "data": {}
        })


@app.post("/login", response_model=dict)
def login_for_access_token(form_data: TokenRequest):
    user = userLogin(form_data.username, form_data.password)
    if not user:
        return {
            'success': False,
            'data': {
            }
        }
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


@app.post("/refresh-token", response_model=dict)
def login_for_access_token(authorization: str = Depends(oauth2_scheme)):
    try:
        refreshToken, param = get_authorization_scheme_param(authorization)
        token_info = verify_token(refreshToken)
        if token_info:
            access_token, expire = create_access_token(data={'sub': token_info['sub']})
            return {
                'success': True,
                'data': {
                    'accessToken': access_token,
                    'refreshToken': refreshToken,
                    'expires': expire.strftime("%Y/%m/%d %H:%M:%S")
                }

            }
        else:
            return {
                'success': False,
                'data': {
                }
            }

    except Exception as e:
        print(f"函数login_for_access_token 出现异常，参数是{authorization},异常是:{e}")


@app.get("/hello")
def say_hello(current_user: dict = Depends(get_current_user)):
    return {"data": current_user}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
