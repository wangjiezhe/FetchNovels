#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import string
from getpass import getpass

from tqdm import tqdm

# from multiprocessing.dummy import Pool

ENCODING = 'GB18030'


def md5(s):
    m = hashlib.md5(s.encode(ENCODING))
    return m.hexdigest()


def jieqi_pd(p, salt):
    return md5(md5(p) + salt)


def crack_salt(p, jieqi):
    col = string.ascii_letters + string.digits
    gen = (i1 + i2 + i3 + i4 + i5 + i6
           for i1 in col
           for i2 in col
           for i3 in col
           for i4 in col
           for i5 in col
           for i6 in col)

    # def check_salt(salt):
    #     if jieqi_pd(p, salt) == jieqi:
    #         print(salt)

    # with Pool(10) as p:
    #     p.map(check_salt, gen, 10)

    for s in tqdm(gen):
        if jieqi_pd(p, s) == jieqi:
            return s


if __name__ == '__main__':
    jieqiUserPassword = input('jieqiUserPassword: ')
    password = getpass()

    crack_salt(password, jieqiUserPassword)
