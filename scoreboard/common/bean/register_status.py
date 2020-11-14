class RegisterStatus:

    @staticmethod
    def newRegisterStatus(registerName: str, functionName: str):
        newRegisterStatus = RegisterStatus()
        newRegisterStatus.registerName = registerName
        newRegisterStatus.functionUnitName = functionName
        return newRegisterStatus

    registerName: str
    functionUnitName: str
