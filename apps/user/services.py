import random
import requests
import string
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone


class CacheTypes:
    registration_sms_verification = "registration_sms_verification"


def generate_cache_key(type_, *args):
    return f"{type_}{''.join(args)}"

def send_verification_code(phone, type_, session):
    code = "".join(random.choice(string.digits) for _ in range(6))
    # message_id = str(timezone.now())
    # requests.post(
    #     settings.SMS_URL,
    #     auth=(settings.SMS_LOGIN, settings.SMS_PASSWORD),
    #     json={
    #         "messages": [
    #             {
    #                 "recipient": phone,
    #                 "message-id": message_id,
    #                 "sms": {
    #                     "originator": "3700",
    #                     "content": {
    #                         "text": f"auto.uz <#> Sizning maxfiy kodingiz: {code}",
    #                     },
    #                 },
    #             }
    #         ]
    #     },
    # )
    cache_key = generate_cache_key(type_, phone, session)
    cache.set(cache_key, code, timeout=1020)
    return cache_key

