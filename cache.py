from pixie import users
from pixie import servers
import threading
import time
import operator


def init(threshold=100):
    return CacheControl(threshold)


class CacheControl:

    cached_users = dict()
    cached_servers = dict()

    def __init__(self, threshold=100):
        self.cached_users = dict()
        self.cached_servers = dict()
        self.cleaner = threading.Thread(target=self.keep_clean, args=(threshold,), daemon=True)
        self.cleaner.start()

    def keep_clean(self, threshold=100):
        while True:
            time.sleep(100)
            if len(self.cached_users) > threshold:
                self.clean(self.cached_users, threshold)
            if len(self.cached_servers) > threshold:
                self.clean(self.cached_servers, threshold)

    def clean(self, d, threshold):
        sorted_ids = sorted(d.values(), key=operator.attrgetter('last_call'), reverse=True)
        for i in sorted_ids[int(round(threshold/2)):]:
            del d[i.id]
        pass

    def add_user(self, user):
        if not isinstance(user, users.DiscordUser):
            return
        self.cached_users[user.id] = user

    def add_server(self, server):
        if not isinstance(server, servers.DiscordServer):
            return
        self.cached_servers[server.id] = server

    def get_user(self, user_id):
        return self.cached_users.get(user_id)

    def get_server(self, server_id):
        return self.cached_users.get(server_id)

