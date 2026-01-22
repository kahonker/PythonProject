from mcstatus import JavaServer, MCServer  # attempt direct import; if one is missing Python will raise
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from os import getenv

load_dotenv()

server_ip_env = getenv("SERVER_IP")
server_port_env = 25565

app = FastAPI()

def check_server_status() -> bool:
    '''Uses mcstatus to check if the server is running.

    Returns a boolean'''
    host, port = server_ip_env, server_port_env
    target = f"{host}:{port}"

    try:
        server_obj = JavaServer.lookup(target, 5)
        status = server_obj.status()
        return True
    except Exception as e:
        print("mcstatus error:", e)
        return False
