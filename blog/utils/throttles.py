# !/usr/bin/env python3
import time
from rest_framework.throttling import BaseThrottle, SimpleRateThrottle

# --------------------------- 自定义类实现 --------------------------------------

VISIT_RECORD = {}


class VisitThrottle(BaseThrottle):
    """
    根据 IP 限制, 10S 内只能访问3次
    """

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        ctime = time.time()

        remote_addr = request.META.get('REMOTE_ADDR')
        # remote_addr = request._request.META.get('REMOTE_ADDR')  # 实际执行

        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime]
            return True

        history = VISIT_RECORD.get(remote_addr)
        self.history = history
        while history and history[-1] < ctime - 10:
            history.pop()

        if len(history) < 3:
            history.insert(0, ctime)
            return True
        # return True    表示继续访问
        # return False   表示访问评率太高被限制

    def wait(self):
        """ 等待时间 """
        ctime = time.time()
        return 10 - (ctime - self.history[-1])


# ----------------------------- 继承类 -------------------------------------


class IPThrottle(SimpleRateThrottle):
    """ 根据 ip 限制 """
    scope = 'anonymity'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    """ 根据用户限制 """
    scope = 'User'

    def get_cache_key(self, request, view):
        return request.user.username
