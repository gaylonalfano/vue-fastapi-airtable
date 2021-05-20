import config
import pathlib
from fastapi import FastAPI, Request, Response, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# NOTE fastapi-airtable/backend/src/app.py
BASE_DIR = pathlib.Path(__file__).parent  # src

# print(config.AIRTABLE_API_KEY)

# ===== Schemas
class TextArea(BaseModel):
    content: str

class User(BaseModel):
    id: int
    name: str


# ===== Data
users = [
    {
        "id": 1,
        "name": "Gaylon"
    },
    {
        "id": 2,
        "name": "Ashley"
    },
    {
        "id": 3,
        "name": "Adrian"
    },
    {
        "id": 4,
        "name": "Aaron"
    },
]

app = FastAPI()

# Allow CORS for FE/BE communication
# https://fastapi.tiangolo.com/tutorial/cors/?h=cors
origins = [
    "http://localhost",
    "http://localhost:3000"  # Vue
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
async def read_root():
    return { "message": "Hello, World"}

# @app.get("/file")
# def read_index():
#     return FileResponse("../../frontend/index.html")

@app.get("/vite")
def read_vite(response: Response):
    # return {"request": request, "message": "This is the return from /vite GET"}
    # return {"request": request }  # Error
    # return {"message": "This is the return from /vite GET"}  # Works
    response.body = "Response body content"
    return { "response": response, "fruit": "apple", "status_code": response.status_code }  # Works


@app.get("/users")
async def read_users():
    """Return list of users"""
    return users  # Works without any Model, Response, etc.

# WORKS because it's returning the data in JSON
@app.post('/add')
async def post_textarea(data: TextArea):
    # print("content: ", content)
    # return {"content": content}
    print(data.dict())  # Works
    return {**data.dict()}  # Works

@app.post("/user", response_model=User)
async def create_user(user: User):
    # Q: Need async? Don't think so for this simple task...
    # Let's take the User object sent in the request and append to users
    # users.append(user)  # Error! Need to convert to dict first!
    # NOTE Read more https://fastapi.tiangolo.com/tutorial/body/
    # print("type(user): ", type(user))  # <class main.User>
    user_dict = user.dict()
    users.append(user_dict)
    return user


# # Null/Empty
# @app.post('/add')
# async def post_textarea(response: Response):
#     return { "response": response }  # body: ""
#     # return response.body  # ""

# ONLY seems to work with Response!
# @app.get("/")
# async def main(response: Response):
#     """
#     Returns a Response with a simple message.
#     """
#     message = "Hello, World"
#     response.body = { "message": message }
#     # return {"message": "Hello, World"}
#     # return {"response": response}  # Works {"response": {"status_code": ...,}}
#     # return response  # Error - Empty Response
#     # return response.body  # Works!
#     return {response}  # Works [{"status_code": ...,}]
#     # return "Hello world"  # Works "Hello World"


# Using python-multipart Form
# NOTE Tutorial uses Templates and method="POST" for <form>
# Therefore, they added param: email:str = Form(...)
# @app.post("/")
# async def submit_signup(response: Response):
#     """
#     Creates a new entry in Airtable with a signup email address.
#     """
#     # TODO Add CSRF for security
#     # return {"submitted_email": email}
#     # return {"request": request}  # CORS error
#     # return request  # CORS error
#     return {response}

# Let's try to parse the request.body which is set inside App.vue submitForm()
# ASYNC - WORKS!
@app.post("/")
async def submit_signup(request: Request):
    # print(request)  # <starlette.requests.Request object at 0x110eafac0>
    # return { request.body }  # Empty...
    # return request  # CORS error
    # return {"request": request}  # CORS
    # TODO Read the Deno router.post("/launches")
    # FIXME I MUST AWAIT SINCE I'M USING ASYNC!
    result = await request.body()
    # print("request.body: ", request.body)  # <bound method Request.body of <starlette...>
    print("request.body(): ", request.body())  # request.body():  <coroutine object Request.body at 0x10e7ef540>
    print("result: ", result)
    return result

# SYNC - BROKEN!
# @app.post("/")
# def submit_signup(request: Request):
#     # print(request)  # <starlette.requests.Request object at 0x110eafac0>
#     # return { request.body }  # Empty...
#     # return request  # CORS error
#     # return {"request": request}  # CORS
#     # TODO Read the Deno router.post("/launches")
#     print(request.body())
#     # return request  # CORS
#     return request.body()  # CORS
