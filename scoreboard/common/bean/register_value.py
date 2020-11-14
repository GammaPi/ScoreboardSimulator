class RegisterValue:

    @staticmethod
    def newRegisterValue(name: str, value: str):
        newRegisterValue = RegisterValue()
        newRegisterValue.name = name
        newRegisterValue.value = value
        return newRegisterValue

    name: str
    value: str
