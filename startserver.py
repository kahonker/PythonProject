from wakeonlan import send_magic_packet
from dotenv import load_dotenv
from os import getenv

load_dotenv()

MAC_ADDRESS = getenv("MAC_ADDRESS")
WAKE_ADDRESS = getenv("WAKE_ADDRESS")

print(MAC_ADDRESS)

send_magic_packet(MAC_ADDRESS, ip_address=WAKE_ADDRESS, port=9)