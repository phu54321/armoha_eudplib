#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from ... import core as c
from ... import ctrlstru as cs
from ... import utils as ut

from . import modcurpl as cp
from . import byterw as bm
from . import cpmemio as cm


@c.EUDFunc
def f_repmovsd_epd(dstepdp, srcepdp, copydwn):
    cpmoda = c.Forward()

    c.VProc([dstepdp, srcepdp], [
        c.SetMemory(cpmoda, c.SetTo, -1),
        dstepdp.QueueAddTo(ut.EPD(cpmoda)),
        srcepdp.SetDest(ut.EPD(0x6509B0)),
    ])

    if cs.EUDWhileNot()(copydwn == 0):
        cpmod = cm.f_dwread_cp(0)
        cpmoda << cpmod.getDestAddr()

        c.VProc(cpmod, [
            cpmod.AddDest(1),
            c.SetMemory(0x6509B0, c.Add, 1),
            copydwn.SubtractNumber(1),
        ])

    cs.EUDEndWhile()

    cp.f_setcurpl2cpcache()


# -------


_br = bm.EUDByteReader()
_bw = bm.EUDByteWriter()


@c.EUDFunc
def f_memcpy(dst, src, copylen):
    b = c.EUDVariable()

    _br.seekoffset(src)
    _bw.seekoffset(dst)

    loopstart = c.NextTrigger()
    loopend = c.Forward()

    cs.EUDJumpIf(copylen.Exactly(0), loopend)

    c.SetVariables(b, _br.readbyte())
    _bw.writebyte(b)

    cs.DoActions(copylen.SubtractNumber(1))
    cs.EUDJump(loopstart)

    loopend << c.NextTrigger()


@c.EUDFunc
def f_memcmp(buf1, buf2, count):
    _br.seekoffset(buf1)
    _bw.seekoffset(buf2)

    if cs.EUDWhile()(count >= 1):
        count -= 1
        ch1 = _br.readbyte()
        ch2 = _bw.readbyte()
        cs.EUDContinueIf(ch1 == ch2)
        c.EUDReturn(ch1 - ch2)
    cs.EUDEndWhile()

    c.EUDReturn(0)
