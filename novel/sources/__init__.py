#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .bgif2 import Bgif2
from .biquge import Biquge
from .cool18 import Cool18
from .danmei123 import Danmei123
from .doubangroup import Doubangroup
from .dzxsw import Dzxsw
from .feizw import Feizw
from .haxtxt import Haxtxt
from .icnsp import Icnsp
from .klxsw import Klxsw
from .lwxs import Lwxs
from .lwxs520 import Lwxs520
from .lwxsw import Lwxsw
from .piaotian import Piaotian
from .piaotiancc import Piaotiancc
from .ranwen import Ranwen
from .sdragon import Sdragon
from .shu69 import Shu69
from .shushu8 import Shushu8
from .sis import Sis
from .sto import Sto
from .ttshuba import Ttshuba
from .ttzw import Ttzw
from .ttzw5 import Ttzw5
from .uks5 import Uks5
from .wdxs import Wdxs
from .xs365 import Xs365
from .yfzww import Yfzww
from .yq33 import Yq33
from .zhaishu8 import Zhaishu8

SERIAL_TYPE = (
    'bgif2',
    'biquge',
    'danmei123',
    'dzxsw',
    'feizw',
    'haxtxt',
    'icnsp',
    'klxsw',
    'lwxs',
    'lwxs520',
    'lwxsw',
    'piaotian',
    'piaotiancc',
    'ranwen',
    'shu69',
    'shushu8',
    'sto',
    'ttshuba',
    'ttzw',
    'ttzw5',
    'uks5',
    'wdxs',
    'xs365',
    'yfzww',
    'yq33',
    'zhaishu8',
)

ARTICLE_TYPE = (
    'cool18',
    'doubangroup',
    'sdragon',
    'sis',
)

# Configuration for free ip in CERNET
CERNET_USE_PROXIES = (
    'cool18',
    'danmei123',
    'dzxsw',
    'haxtxt',
    'klxsw',
    'lwxs520',
    'lwxs',
    'lwxsw',
    'piaotian',
    'piaotiancc',
    'ranwen',
    'sdragon',
    'shu69',
    'shushu8',
    'sis',
    'sto',
    'ttshuba',
    'ttzw',
    'uks5',
    'wdxs',
    'xs365',
    'yq33',
    'zhaishu8',
)

DEFAULT_NOT_OVERWRITE = (
    'cool18',
)

AUTO_MARK_FINISH = (
    'sto',
)
