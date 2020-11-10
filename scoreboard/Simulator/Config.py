class Config:
    '''
    Simulator Hardware configuration
    '''
    functional_units = {
        "integer_alu": {"quantity": 1, "clock_cycles": 1},
        "load_store": {"quantity": 1, "clock_cycles": 1},
        "float_add_sub": {"quantity": 1, "clock_cycles": 2},
        "float_mult": {"quantity": 2, "clock_cycles": 10},
        "float_div": {"quantity": 1, "clock_cycles": 40},
    }

    # todo: Change this definition to register lists.
    register_status_size = 30

    # define R_TYPE 1
    # define I_TYPE 2
    # define J_TYPE 3
    # define F_TYPE 4
    # define M_TYPE 5

    # define NOP 0
    # define LOAD  1
    # define STORE 2
    # define REG1I 3
    # define REG2I 4
    # define REG2S 5
    # define JUMP  6
    # define JREG  7
    # define HALT  8
    # define REG3F 9
    # define BRANCH 10
    # define REG3   11
    # define REGID  12
    # define FLOAD  13
    # define FSTORE 14
    # define JREGN  15
    # define REG2F  16

    # define I_SPECIAL       0x00
    # define I_COP1          0x11
    # define I_DOUBLE        0x11
    # define I_MTC1          0x04
    # define I_HALT          0x01

    # define I_J             0x02
    # define I_JAL           0x03
    # define I_BEQ           0x04
    # define I_BNE           0x05
    # define I_BEQZ          0x06
    # define I_BNEZ          0x07

    # define I_DADDI         0x18
    # define I_DADDIU        0x19
    # define I_SLTI          0x0A
    # define I_SLTIU         0x0B
    # define I_ANDI          0x0C
    # define I_ORI           0x0D
    # define I_XORI          0x0E
    # define I_LUI           0x0F

    # define I_LB            0x20
    # define I_LH            0x21
    # define I_LW            0x23
    # define I_LBU           0x24
    # define I_LHU           0x25
    # define I_LWU           0x27#define R_TYPE 1
    # define I_TYPE 2
    # define J_TYPE 3
    # define F_TYPE 4
    # define M_TYPE 5

    # define NOP 0
    # define LOAD  1
    # define STORE 2
    # define REG1I 3
    # define REG2I 4
    # define REG2S 5
    # define JUMP  6
    # define JREG  7
    # define HALT  8
    # define REG3F 9
    # define BRANCH 10
    # define REG3   11
    # define REGID  12
    # define FLOAD  13
    # define FSTORE 14
    # define JREGN  15
    # define REG2F  16

    # define I_SPECIAL       0x00
    # define I_COP1          0x11
    # define I_DOUBLE        0x11
    # define I_MTC1          0x04
    # define I_HALT          0x01

    # define I_J             0x02
    # define I_JAL           0x03
    # define I_BEQ           0x04
    # define I_BNE           0x05
    # define I_BEQZ          0x06
    # define I_BNEZ          0x07

    # define I_DADDI         0x18
    # define I_DADDIU        0x19
    # define I_SLTI          0x0A
    # define I_SLTIU         0x0B
    # define I_ANDI          0x0C
    # define I_ORI           0x0D
    # define I_XORI          0x0E
    # define I_LUI           0x0F

    # define I_LB            0x20
    # define I_LH            0x21
    # define I_LW            0x23
    # define I_LBU           0x24
    # define I_LHU           0x25
    # define I_LWU           0x27
    # define I_SB            0x28
    # define I_SH            0x29
    # define I_SW            0x2B
    # define I_L_D           0x35
    # define I_S_D           0x3D
    # define I_LD            0x37
    # define I_SD            0x3F

    # define R_NOP           0x00
    # define R_JR            0x08
    # define R_JALR          0x09
    # define R_MOVZ          0x0A
    # define R_MOVN          0x0B

    # define R_DSLLV         0x14
    # define R_DSRLV         0x16
    # define R_DSRAV         0x17
    # define R_DMUL          0x1C
    # define R_DMULU         0x1D
    # define R_DDIV          0x1E
    # define R_DDIVU         0x1F

    # define R_AND           0x24
    # define R_OR            0x25
    # define R_XOR           0x26
    # define R_SLT           0x2A
    # define R_SLTU          0x2B
    # define R_DADD          0x2C
    # define R_DADDU         0x2D
    # define R_DSUB          0x2E
    # define R_DSUBU         0x2F

    # define R_DSLL          0x38
    # define R_DSRL          0x3A
    # define R_DSRA          0x3B

    # define F_ADD_D         0x00
    # define F_SUB_D         0x01
    # define F_MUL_D         0x02
    # define F_DIV_D         0x03
    # define F_MOV_D         0x06
    # define F_CVT_W_D       0x24
    # define F_CVT_L_D       0x25
    # define I_SB            0x28
    # define I_SH            0x29
    # define I_SW            0x2B
    # define I_L_D           0x35
    # define I_S_D           0x3D
    # define I_LD            0x37
    # define I_SD            0x3F

    # define R_NOP           0x00
    # define R_JR            0x08
    # define R_JALR          0x09
    # define R_MOVZ          0x0A
    # define R_MOVN          0x0B

    # define R_DSLLV         0x14
    # define R_DSRLV         0x16
    # define R_DSRAV         0x17
    # define R_DMUL          0x1C
    # define R_DMULU         0x1D
    # define R_DDIV          0x1E
    # define R_DDIVU         0x1F

    # define R_AND           0x24
    # define R_OR            0x25
    # define R_XOR           0x26
    # define R_SLT           0x2A
    # define R_SLTU          0x2B
    # define R_DADD          0x2C
    # define R_DADDU         0x2D
    # define R_DSUB          0x2E
    # define R_DSUBU         0x2F

    # define R_DSLL          0x38
    # define R_DSRL          0x3A
    # define R_DSRA          0x3B

    # define F_ADD_D         0x00
    # define F_SUB_D         0x01
    # define F_MUL_D         0x02
    # define F_DIV_D         0x03
    # define F_MOV_D         0x06
    # define F_CVT_W_D       0x24
    # define F_CVT_L_D       0x25

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
