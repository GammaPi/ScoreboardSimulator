class stall:

    @staticmethod
    def newStall(type: str, dependToRegister: str, dependFromRegister: str):
        newStall = stall()
        newStall.type = type
        newStall.dependToRegister = dependToRegister
        newStall.dependFromRegister = dependFromRegister
        return newStall

    type: str
    dependToRegister: str
    dependFromRegister: str
