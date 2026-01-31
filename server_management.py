from mcstatus import JavaServer, MCServer  # attempt direct import; if one is missing Python will raise
from wakeonlan import send_magic_packet
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from os import getenv

from mcstatus.responses import JavaStatusResponse

load_dotenv()

MAC_ADDRESS = getenv("MAC_ADDRESS")
WAKE_ADDRESS = getenv("WAKE_ADDRESS")
server_ip_env = getenv("SERVER_IP")
server_port_env = 25565

app = FastAPI()

def check_server_status() -> JavaStatusResponse | None:
    '''Uses mcstatus to check if the server is running.

    Returns a boolean'''
    host, port = server_ip_env, server_port_env
    target = f"{host}:{port}"

    try:
        server_obj = JavaServer.lookup(target, 5)
        status = server_obj.status()
        return status
    except Exception as e:
        print("mcstatus error:", e)
        return None

def server_start():
    send_magic_packet(MAC_ADDRESS, ip_address=WAKE_ADDRESS, port=9)