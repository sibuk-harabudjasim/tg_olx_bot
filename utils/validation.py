# -*- coding: utf-8 -*-
import re

from utils.db import Tasks

url_re = re.compile(r'(((http|ftp|https):\/{2})+(([0-9a-z_-]+\.)+(aero|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mn|mn|mo|mp|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|nom|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ra|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw|arpa)(:[0-9]+)?((\/([~0-9a-zA-Z\#\+\%@\.\/_-]+))?(\?[0-9a-zA-Z\+\%@\/&\[\];=_-]+)?)?))\b')


def validate_blacklist(words):
    res = []
    if len(words) > 10:
        res.append('Don`t write too much words, you can miss to many adverts, usually, 5 is enough.')
    if [w for w in words if len(w) > 10]:
        res.append('Aren`t your words too complicated? Maybe you`d better stick to simpler criterias?')
    return res


def validate_whitelist(words):
    res = []
    if [w for w in words if len(w) > 10]:
        res.append('Aren`t your words too complicated? Maybe you`d better stick to simpler criterias?')
    return res


def validate_url(url):
    return url if url_re.match(url) else None


def _clean_name(name):
    name = re.sub(r'[-\s_]{2,}', '_', name)
    return re.sub(r'[\'"\?!\*\.\$#@%\^&\(\)]', '', name)


def escape_re(value):
    value = value.replace('.', '\\.')
    return value


async def validate_name(name):
    names = await Tasks.get_all_task_names()
    name = _clean_name(name)
    if name in names:
        return
    return name


__author__ = 'manitou'
