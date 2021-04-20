import requests
req=requests.get("https://discord.com/api/path/to/the/endpoint")
print(req.headers["Retry-After"])
