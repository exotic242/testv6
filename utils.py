
from flask import request
from user_agents import parse as parse_ua

def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0]
    return request.remote_addr

def get_device_info():
    ua = parse_ua(request.headers.get("User-Agent"))
    return {
        "browser": ua.browser.family,
        "os": ua.os.family,
        "device": ua.device.family
    }
