#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

from ... import core as c
from ... import ctrlstru as cs
from ... import varfunc as vf
from ..calcf import f_mul, f_div
from ..memiof import f_dwread_epd


@vf.EUDFunc
def f_lengthdir(length, angle):
    # sin, cos table
    clist = []
    slist = []

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    for i in range(91):
        cosv = math.floor(math.cos(math.pi / 180 * i) * 65536 + 0.5)
        sinv = math.floor(math.sin(math.pi / 180 * i) * 65536 + 0.5)
        clist.append(c.i2b4(cosv))
        slist.append(c.i2b4(sinv))

    cdb = c.Db(b''.join(clist))
    sdb = c.Db(b''.join(slist))

    ## MAIN LOGIC

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    if cs.EUDIf(angle >= 360):
        angle << f_div(angle, 360)[1]
    cs.EUDEndIf()

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    ldir_x, ldir_y = vf.EUDVariable(), vf.EUDVariable()  # cos, sin * 65536
    csign, ssign = vf.EUDLightVariable(), vf.EUDLightVariable()  # sign of cos, sin
    tableangle = vf.EUDVariable()

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    # get cos, sin from table
    if cs.EUDIf(angle <= 89):
        tableangle << angle
        csign << 1
        ssign << 1

    if cs.EUDElseIf(angle <= 179):
        tableangle << 180 - angle
        csign << -1
        ssign << 1

    if cs.EUDElseIf(angle <= 269):
        tableangle << angle - 180
        csign << -1
        ssign << -1

    if cs.EUDElse():
        tableangle << 360 - angle
        csign << 1
        ssign << -1

    cs.EUDEndIf()

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    tablecos = f_dwread_epd(c.EPD(cdb) + tableangle)
    tablesin = f_dwread_epd(c.EPD(sdb) + tableangle)

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    # calculate lengthdir
    ldir_x << f_div(f_mul(tablecos, length), 65536)[0]
    ldir_y << f_div(f_mul(tablesin, length), 65536)[0]

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    # restore sign of cos, sin
    if cs.EUDIf(csign == -1):
        ldir_x << 0xFFFFFFFF - ldir_x + 1
    cs.EUDEndIf()

    if cs.EUDIf(ssign == -1):
        ldir_y << 0xFFFFFFFF - ldir_y + 1
    cs.EUDEndIf()

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    return ldir_x, ldir_y

