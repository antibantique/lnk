import logging
import uuid

import constants as const

from aiocache import Cache

from utils import parse_ttl, calc_seconds
from exceptions import InvalidParameters


async def redirect(uid: str, cache: Cache) -> str:
    url = await cache.get(f'cache:{uid}')

    return url


async def shortify(data: dict, cache: Cache) -> str:
    try:
        url = data['url']
    except KeyError as e:
        logging.warning('No URL parameter: %s', e)
        raise InvalidParemeters

    uid = data.get('uid', uuid.uuid1().hex)

    ttl_str = data.get('ttl')
    if ttl_str is None:
        ttl = const.DEFAULT_TTL
    else:
        try:
            number, unit = parse_ttl(ttl_str)
        except Exception as e:
            logging.warning('Invalid TTL praremeter: %s', e)
            raise InvalidParameters
        else:
            ttl = calc_seconds(number, unit)

    await cache.add(f'cache:{uid}', url, ttl=ttl)

    return uid
