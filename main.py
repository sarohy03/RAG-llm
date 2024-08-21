from fastapi import FastAPI
import  APIS.User_side,APIS.Client_Side
app = FastAPI()


app.include_router(APIS.User_side.router)
app.include_router(APIS.Client_Side.router)

