class FunctionUnit:

    @staticmethod
    def newFunctionUnit(name, busy, op, des, fi, fj, fk, qj, qk, rj, rk):
        newFunctionUnit = FunctionUnit()
        newFunctionUnit.name = name
        newFunctionUnit.busy = busy
        newFunctionUnit.op = op
        newFunctionUnit.des = des
        newFunctionUnit.fi = fi
        newFunctionUnit.fj = fj
        newFunctionUnit.fk = fk
        newFunctionUnit.qj = qj
        newFunctionUnit.qk = qk
        newFunctionUnit.rj = rj
        newFunctionUnit.rk = rk
        return newFunctionUnit

    name: str
    busy: bool
    op: str
    des: str
    fi: str
    fj: str
    fk: str
    qj: str
    qk: str
    rj: str
    rk: str
