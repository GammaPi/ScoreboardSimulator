class FunctionUnitStatus:

    @staticmethod
    def newFunctionUnitStatus(functionUnitList: list):
        newFunctionUnitStatus = FunctionUnitStatus()
        newFunctionUnitStatus.functionUnitList = functionUnitList
        return newFunctionUnitStatus

    functionUnitList: list  # FunctionUnit
