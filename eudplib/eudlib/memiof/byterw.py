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

from . import dwepdio as dwm, modcurpl as cp
from ...utils import EPD


class EUDByteReader:
    """Read byte by byte."""
    ret = c.EUDVariable()

    def __init__(self):
        self._suboffset = c.EUDLightVariable()
        self._read = c.Forward()

    # -------

    def seekepd(self, epdoffset):
        """Seek EUDByteReader to specific epd player address"""
        if c.IsEUDVariable(epdoffset):
            return c.VProc(
                epdoffset,
                [
                    epdoffset.QueueAssignTo(EPD(self._read) + 5),
                    self._suboffset.SetNumber(0),
                ],
            )
        else:
            return c.RawTrigger(
                actions=[
                    c.SetMemory(self._read + 20, c.SetTo, epdoffset),
                    self._suboffset.SetNumber(0),
                ]
            )

    @c.EUDMethod
    def seekoffset(self, offset):
        """Seek EUDByteReader to specific address"""
        # convert offset to epd offset & suboffset
        q, r = c.f_div(offset, 4)
        c.VProc(
            [q, r],
            [
                q.AddNumber(-(0x58A364 // 4)),
                q.SetDest(EPD(self._read) + 5),
                r.SetDest(self._suboffset),
            ],
        )

    # -------

    @c.EUDMethod
    def readbyte(self):
        """Read byte from current address. ByteReader will advance by 1 bytes.

        :returns: Read byte
        """
        case = [c.Forward() for _ in range(5)]
        ret = EUDByteReader.ret

        cs.DoActions([self._read << c.SetMemory(0x6509B0, c.SetTo, 0), ret.SetNumber(0)])

        for i in range(4):
            case[i] << c.NextTrigger()
            if i < 3:
                cs.EUDJumpIfNot(self._suboffset.Exactly(i), case[i + 1])
            for j in range(8):
                c.RawTrigger(
                    conditions=c.DeathsX(
                        c.CurrentPlayer, c.AtLeast, 1, 0, 2 ** (j + 8 * i)
                    ),
                    actions=ret.AddNumber(2 ** j),
                )
            if i < 3:
                c.RawTrigger(nextptr=case[-1], actions=self._suboffset.AddNumber(1))
            else:  # suboffset == 3
                cs.DoActions(
                    [
                        c.SetMemory(self._read + 20, c.Add, 1),
                        self._suboffset.SetNumber(0),
                    ]
                )

        case[-1] << c.NextTrigger()
        cp.f_setcurpl2cpcache()
        return ret


class EUDByteWriter:
    """Write byte by byte."""

    def __init__(self):
        self._suboffset = c.EUDLightVariable()
        self._write = c.Forward()

    # -------

    def seekepd(self, epdoffset):
        """Seek EUDByteWriter to specific epd player address"""
        if c.IsEUDVariable(epdoffset):
            c.VProc(
                epdoffset,
                [
                    epdoffset.QueueAssignTo(EPD(self._write) + 4),
                    self._suboffset.SetNumber(0),
                ],
            )
        else:
            c.RawTrigger(
                actions=[
                    c.SetMemory(self._write + 16, c.SetTo, epdoffset),
                    self._suboffset.SetNumber(0),
                ]
            )

    @c.EUDMethod
    def seekoffset(self, offset):
        """Seek EUDByteWriter to specific address"""
        # convert offset to epd offset & suboffset
        q, r = c.f_div(offset, 4)
        c.VProc(
            [q, r],
            [
                q.AddNumber(-(0x58A364 // 4)),
                q.SetDest(EPD(self._write) + 4),
                r.SetDest(self._suboffset),
            ],
        )

    # -------

    @c.EUDMethod
    def writebyte(self, byte):
        """Write byte to current position.

        Write a byte to current position of EUDByteWriter.
        ByteWriter will advance by 1 byte.
        """
        cs.EUDSwitch(self._suboffset)
        if cs.EUDSwitchCase()(0):
            c.VProc(
                byte,
                [
                    byte.SetDest(EPD(self._write) + 5),
                    c.SetMemory(self._write, c.SetTo, 0xFF),
                ],
            )
            cs.EUDBreak()
        for i in range(1, 4):
            if cs.EUDSwitchCase()(i):
                cs.DoActions(c.SetMemory(self._write, c.SetTo, 0xFF << (8 * i)))
                for j in range(8):
                    c.RawTrigger(
                        conditions=byte.AtLeastX(1, 2 ** j),
                        actions=c.SetMemory(self._write + 20, c.Add, 2 ** (j + i * 8)),
                    )
                cs.EUDBreak()

        cs.EUDEndSwitch()

        cs.DoActions(
            [
                self._suboffset.AddNumber(1),
                self._write << c.SetDeathsX(0, c.SetTo, 0, 0, 0xFF00),
                c.SetMemory(self._write + 20, c.SetTo, 0),
            ]
        )
        c.RawTrigger(
            conditions=self._suboffset.AtLeast(4),
            actions=[
                self._suboffset.SetNumber(0),
                c.SetMemory(self._write + 16, c.Add, 1),
            ],
        )

    @classmethod
    def flushdword(cls):
        pass
