## NOTE: THIS FILE IS GENERATED BY EPSCRIPT! DO NOT MODITY
from eudplib import *
from eudplib.epscript.helper import _RELIMP, _IGVA, _CGFW, _ARR, _VARR, _SRET, _SV, _ATTW, _ARRW, _ATTC, _ARRC, _L2V, _LVAR, _LSH
# (Line 1) import eudplib.eudlib.utilf.datadumper;
from eudplib.eudlib.utilf import datadumper
# (Line 2) const inputData = py_bytes(1000);
inputData = _CGFW(lambda: [bytes(1000)], 1)[0]
# (Line 3) const outOffsets = list(0x6D5A30);
outOffsets = _CGFW(lambda: [FlattenList([0x6D5A30])], 1)[0]
# (Line 4) const flags = py_set();
flags = _CGFW(lambda: [set()], 1)[0]
# (Line 5) flags.add(py_str("copy"));
flags.add(str("copy"))
# (Line 6) datadumper._add_datadumper(inputData, outOffsets, flags);
datadumper._add_datadumper(inputData, outOffsets, flags)
# (Line 8) const expected_result = py_str("abcdeArmo\xE2\x80\x89\0");
expected_result = _CGFW(lambda: [str("abcdeArmo\xE2\x80\x89\0")], 1)[0]
# (Line 9) function test_stattext() {
@EUDFunc
def f_test_stattext():
    # (Line 10) const armo = Db("Armo");
    armo = Db("Armo")
    # (Line 11) const stattext = GetTBLAddr(1);
    stattext = GetTBLAddr(1)
    # (Line 12) settblf(1, 0, "abcde{:s}", armo, encoding="UTF-8");
    f_settblf(1, 0, "abcde{:s}", armo, encoding="UTF-8")
    # (Line 13) const ret = py_list();
    ret = list()
    # (Line 14) const br = EUDByteReader();
    br = EUDByteReader()
    # (Line 15) br.seekoffset(stattext);
    br.seekoffset(stattext)
    # (Line 16) foreach(char : expected_result) {
    for char in expected_result:
        # (Line 17) ret.append(br.readbyte());
        ret.append(br.readbyte())
        # (Line 18) }
        # (Line 19) return List2Assignable(ret);

    EUDReturn(List2Assignable(ret))
    # (Line 20) }
