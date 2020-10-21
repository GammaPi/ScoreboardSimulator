''' Hardware configuration
    Copy from https://github.com/FelSiq/scoreboarding-for-dynamic-instruction-scheduling/blob/master/configme.py
'''
class Config:
    functional_units = {
        "integer_alu": {"quantity": 1, "clock_cycles": 1},
        "load_store": {"quantity": 2, "clock_cycles": 2},
        "float_add_sub": {"quantity": 1, "clock_cycles": 2},
        "float_mult": {"quantity": 2, "clock_cycles": 10},
        "float_div": {"quantity": 1, "clock_cycles": 40},
    }

    instruction_list = {
        "L.D": {
            "functional_unit": "load_store",
            "instruction_type": "I",
        },

        "S.D": {
            "functional_unit": "load_store",
            "instruction_type": "I",
        },

        "MUL.D": {
            "functional_unit": "float_mult",
            "instruction_type": "R",
        },

        "DIV.D": {
            "functional_unit": "float_div",
            "instruction_type": "R",
        },

        "ADD.D": {
            "functional_unit": "float_add_sub",
            "instruction_type": "R",
        },

        "SUB.D": {
            "functional_unit": "float_add_sub",
            "instruction_type": "R",
        },

        "LW": {
            "functional_unit": "integer_alu",
            "instruction_type": "I",
        },

        "SW": {
            "functional_unit": "integer_alu",
            "instruction_type": "I",
        },

        "ADDI": {
            "functional_unit": "integer_alu",
            "instruction_type": "I",
        },

        "ADD": {
            "functional_unit": "integer_alu",
            "instruction_type": "R",
        },

        "SUB": {
            "functional_unit": "integer_alu",
            "instruction_type": "R",
        },

        "BEQ": {
            "functional_unit": "integer_alu",
            "instruction_type": "I",
        },
    }

    stage_delay = {
        "issue": 1,
        "read_operands": 1,
        "write_result": 1,
        "update_flags": 1,
    }

    custom_inst_additional_delay = {
        "": 0,
    }