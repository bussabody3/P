import time, redis, os, json, re, requests, asyncio 
from pyrogram import *
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MockRedis:
    """A mock Redis class that provides safe no-op methods when Redis is unavailable"""
    def __init__(self):
        self._data = {}
    
    def get(self, key):
        return self._data.get(key)
    
    def set(self, key, value, *args, **kwargs):
        self._data[key] = value
        return True
    
    def delete(self, *keys):
        for key in keys:
            self._data.pop(key, None)
        return len(keys)
    
    def exists(self, *keys):
        return sum(1 for key in keys if key in self._data)
    
    def keys(self, pattern="*"):
        if pattern == "*":
            return list(self._data.keys())
        import fnmatch
        return [k for k in self._data.keys() if fnmatch.fnmatch(k, pattern)]
    
    def hget(self, name, key):
        h = self._data.get(name, {})
        return h.get(key) if isinstance(h, dict) else None
    
    def hset(self, name, key=None, value=None, mapping=None):
        if name not in self._data:
            self._data[name] = {}
        if key is not None:
            self._data[name][key] = value
        if mapping:
            self._data[name].update(mapping)
        return 1
    
    def hgetall(self, name):
        return self._data.get(name, {})
    
    def hdel(self, name, *keys):
        h = self._data.get(name, {})
        count = 0
        for key in keys:
            if key in h:
                del h[key]
                count += 1
        return count
    
    def incr(self, key, amount=1):
        val = int(self._data.get(key, 0)) + amount
        self._data[key] = str(val)
        return val
    
    def decr(self, key, amount=1):
        return self.incr(key, -amount)
    
    def lpush(self, name, *values):
        if name not in self._data:
            self._data[name] = []
        for v in values:
            self._data[name].insert(0, v)
        return len(self._data[name])
    
    def rpush(self, name, *values):
        if name not in self._data:
            self._data[name] = []
        self._data[name].extend(values)
        return len(self._data[name])
    
    def lrange(self, name, start, end):
        lst = self._data.get(name, [])
        if end == -1:
            return lst[start:]
        return lst[start:end+1]
    
    def llen(self, name):
        return len(self._data.get(name, []))
    
    def sadd(self, name, *values):
        if name not in self._data:
            self._data[name] = set()
        before = len(self._data[name])
        self._data[name].update(values)
        return len(self._data[name]) - before
    
    def smembers(self, name):
        return self._data.get(name, set())
    
    def srem(self, name, *values):
        s = self._data.get(name, set())
        count = 0
        for v in values:
            if v in s:
                s.discard(v)
                count += 1
        return count
    
    def sismember(self, name, value):
        s = self._data.get(name, set())
        return value in s

    def ping(self):
        return True

# Try to connect to Redis, but don't fail if it's not available
try:
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    r.ping()
except Exception as e:
    print(f"Warning: Redis not available: {e}")
    print("Bot will work with in-memory storage (data won't persist across restarts)")
    r = MockRedis()

to_config = """
from main import r, MockRedis
"""

print('''
Loading…
█▒▒▒▒▒▒▒▒▒''')
print('\n\n')

# Get token from environment variables or from information.py
try:
    # First try to get from environment variables (for Render)
    token = os.getenv('BOT_TOKEN')
    owner_id = int(os.getenv('DEV_ID', 0))
    
    # If not in environment, try from information.py
    if not token:
        from information import token, owner_id
    
    if token:
        Dev_Zaid = token.split(':')[0]
        if r:
            r.set(f'{Dev_Zaid}botowner', owner_id)
except Exception as e:
    print(f"Error loading config: {e}")
    # If neither environment nor file exist, prompt for input
    token = input('[+] Enter the bot token : ')
    owner_id = int(input('[+] Enter SUDO ID : '))
    Dev_Zaid = token.split(':')[0]
    
    # Try to save to Redis if available
    if r:
        try:
            r.set(f'{Dev_Zaid}botowner', owner_id)
        except:
            pass
    
    # Save to information.py
    with open('information.py', 'w+') as www:
        text = 'token = "{}"\nowner_id = {}'
        www.write(text.format(token, owner_id))

# Get owner_id from Redis or use the one from environment/config
if r:
    if not r.get(f'{Dev_Zaid}botowner'):
        if owner_id:
            r.set(f'{Dev_Zaid}botowner', owner_id)
    else:
        owner_id = int(r.get(f'{Dev_Zaid}botowner'))
else:
    if not owner_id:
        owner_id = int(input('[+] Enter SUDO ID : '))

print('''
10% 
███▒▒▒▒▒▒▒ ''')

to_config += f"\ntoken = '{token}'"
to_config += f"\nDev_Zaid = token.split(':')[0]"
to_config += f"\nsudo_id = {owner_id}"

try:
    username = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()["result"]["username"]
    to_config += f"\nbotUsername = '{username}'"
except:
    username = os.getenv('BOT_USERNAME', 'A7718BOT')
    to_config += f"\nbotUsername = '{username}'"

to_config += "\nfrom kvsqlite.sync import Client as DB"
to_config += "\nytdb = DB('ytdb.sqlite')"
to_config += "\nsounddb = DB('sounddb.sqlite')"
to_config += "\nwsdb = DB('wsdb.sqlite')"

print('''
30% 
█████▒▒▒▒▒ ''')

with open('config.py','w+') as w:
    w.write(to_config)

from config import *

print('''
50% 
███████▒▒▒ ''')

app = Client(f'{Dev_Zaid}r3d', 38699092, '480f2b2d941c5c49ddc34e6d8c5db3fd',
    bot_token=token,
    plugins={"root": "Plugins"},
)

# إضافة app لملف config.py لكي تتمكن الإضافات من استخدامه
with open('config.py', 'a') as f:
    f.write("\nfrom main import app\n")

# Initialize Redis keys if Redis is available
if r:
    if not r.get(f'{Dev_Zaid}:botkey'):
        r.set(f'{Dev_Zaid}:botkey', '⇜')

    if not r.get(f'{Dev_Zaid}botname'):
        r.set(f'{Dev_Zaid}botname', 'شهد')

    if not r.get(f'{Dev_Zaid}botchannel'):
        r.set(f'{Dev_Zaid}botname', 'JolyTepbot')

def Find(text):
    m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»""'']))"
    url = re.findall(m,text)  
    return [x[0] for x in url]

print('''
[===========================]

█████╗░██████╗░██████╗░
██╔══██╗╚════██╗██╔══██╗
██████╔╝░█████╔╝██║░░██║
██╔══██╗░╚═══██╗██║░░██║
██║░░██║██████╔╝██████╔╝
╚═╝░░╚═╝╚═════╝░╚═════╝░

[===========================]

🔮 Your bot started successfully on R 3 D ☆ Source 🔮

•••••••• @Tepthon - @A7718BOT •••••••••

''')

print('''

100% 
██████████''')

async def main():
    await app.start()
    from Plugins.azan import start_azan_task
    start_azan_task(app)
    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())
