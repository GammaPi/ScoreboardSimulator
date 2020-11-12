from Simulator import Config



def test_instr_type():
    assert (Config.InstrType['LW'] != None)
    assert (Config.InstrType[0x01] != None)
    assert (Config.InstrType['L.D'] != None)
    assert (Config.InstrType['l.D'] != None)
    assert (Config.InstrType['l.d'] != None)
    assert (Config.InstrType['l.D'] == Config.InstrType['L.D'])



