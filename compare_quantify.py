# This script takes a path of folder containing diff files generated by designite_diff script.
# It assumes that the file names are in <project>.<commit-hash1>.<commit-hash2> format.
import os
import sys

A_AMB_INT = 'Ambiguous Interfaces'
A_FEA_CON = 'Feature Concentration'
A_UNS_DEP = 'Unstable Dependency'
A_CYC_DEP = 'Cyclic Dependency'
A_DEN_STR = 'Dense Structure'
A_SCA_FUN = 'Scattered Functionality'
A_GOD_COM = 'God Component'

D_UNN_ABS = "Unnecessary Abstraction"
D_IMP_ABS = "Imperative Abstraction"
D_MUL_ABS = "Multifaceted Abstraction"
D_UNUT_ABS = "Unutilized Abstraction"
D_DUP_ABS = "Duplicate Abstraction"
D_FEA_ENV = "Feature Envy"
D_DEF_ENC = "Deficient Encapsulation"
D_UXP_ENC = "Unexploited Encapsulation"
D_BRO_MOD = "Broken Modularization"
D_INS_MOD = "Insufficient Modularization"
D_HUB_MOD = "Hub-like Modularization"
D_CYC_MOD = "Cyclically-dependent Modularization"
D_WID_HIE = "Wide Hierarchy"
D_DEE_HIE = "Deep Hierarchy"
D_MUL_HIE = "Multipath Hierarchy"
D_CYC_HIE = "Cyclic Hierarchy"
D_REB_HIE = "Rebellious Hierarchy"
D_UNF_HIE = "Unfactored Hierarchy"
D_MIS_HIE = "Missing Hierarchy"
D_BRO_HIE = "Broken Hierarchy"

I_LONG_MTD = "Long Method"
I_COMP_MTD = "Complex Method"
I_LONG_PARAM_LIST = "Long Parameter List"
I_LONG_ID = "Long Identifier"
I_LONG_STMT = "Long Statement"
I_COMP_COND = "Complex Conditional"
I_VIRTUAL_CALL = "Virtual Method Call from Constructor"
I_EMTY_CATCH = "Empty Catch Block"
I_MAGIC_NO = "Magic Number"
I_DUP_CODE = "Duplicate Code"
I_MIS_DEF = "Missing Default"


def _get_smell_type(line):
    if line.startswith('Different architecture smells:'):
        return SmellType.ARCH
    if line.startswith('Different design smells:'):
        return SmellType.DESIGN
    if line.startswith('Different implementation smells:'):
        return SmellType.IMPL
    return None


class SmellType:
    ARCH = 0
    DESIGN = 1
    IMPL = 2


class ArchSmellCount:
    def __init__(self):
        self.cyc_dep = 0
        self.amb_int = 0
        self.fea_con = 0
        self.uns_dep = 0
        self.den_str = 0
        self.sca_fun = 0
        self.god_com = 0

    def total(self):
        return self.cyc_dep + self.amb_int + self.fea_con + self.uns_dep + self.den_str + self.sca_fun + self.god_com

    def count(self, line):
        smell_name = line.split(',')[2].strip()
        if smell_name == A_AMB_INT:
            self.amb_int += 1
        elif smell_name == A_FEA_CON:
            self.fea_con += 1
        elif smell_name == A_UNS_DEP:
            self.uns_dep += 1
        elif smell_name == A_CYC_DEP:
            self.cyc_dep += 1
        elif smell_name == A_DEN_STR:
            self.den_str += 1
        elif smell_name == A_SCA_FUN:
            self.sca_fun += 1
        elif smell_name == A_GOD_COM:
            self.god_com += 1

    def __str__(self):
        return str(self.amb_int) + ',' + str(self.fea_con) + ',' + str(
            self.uns_dep) + ',' + str(self.cyc_dep) + ',' + str(self.den_str) + ',' + str(
            self.sca_fun) + ',' + str(self.god_com)

class DesignSmellCount:
    def __init__(self):
        self.unn_abs = 0
        self.imp_abs = 0
        self.mul_abs = 0
        self.unut_abs = 0
        self.dup_abs = 0
        self.fea_env = 0
        self.def_enc = 0
        self.uxp_enc = 0
        self.bro_mod = 0
        self.ins_mod = 0
        self.hub_mod = 0
        self.cyc_mod = 0
        self.wid_hie = 0
        self.dee_hie = 0
        self.mul_hie = 0
        self.cyc_hie = 0
        self.reb_hie = 0
        self.unf_hie = 0
        self.mis_hie = 0
        self.bro_hie = 0

    def total(self):
        return self.unn_abs + self.imp_abs + self.mul_abs + self.unut_abs + self.dup_abs + self.fea_env + self.def_enc + self.uxp_enc + self.bro_mod + self.ins_mod + self.hub_mod + self.cyc_mod + self.wid_hie + self.dee_hie + self.mul_hie + self.cyc_hie + self.reb_hie + self.unf_hie + self.mis_hie + self.bro_hie

    def count(self, line):
        smell_name = line.split(',')[3].strip()
        if smell_name == D_UNN_ABS:
            self.unn_abs += 1
        elif smell_name == D_IMP_ABS:
            self.imp_abs += 1
        elif smell_name == D_MUL_ABS:
            self.mul_abs += 1
        elif smell_name == D_UNUT_ABS:
            self.unut_abs += 1
        elif smell_name == D_DUP_ABS:
            self.dup_abs += 1
        elif smell_name == D_FEA_ENV:
            self.fea_env += 1
        elif smell_name == D_DEF_ENC:
            self.def_enc += 1
        elif smell_name == D_UXP_ENC:
            self.uxp_enc += 1
        elif smell_name == D_BRO_MOD:
            self.bro_mod += 1
        elif smell_name == D_INS_MOD:
            self.ins_mod += 1
        elif smell_name == D_HUB_MOD:
            self.hub_mod += 1
        elif smell_name == D_CYC_MOD:
            self.cyc_mod += 1
        elif smell_name == D_WID_HIE:
            self.wid_hie += 1
        elif smell_name == D_DEE_HIE:
            self.dee_hie += 1
        elif smell_name == D_MUL_HIE:
            self.mul_hie += 1
        elif smell_name == D_CYC_HIE:
            self.cyc_hie += 1
        elif smell_name == D_REB_HIE:
            self.reb_hie += 1
        elif smell_name == D_UNF_HIE:
            self.unf_hie += 1
        elif smell_name == D_MIS_HIE:
            self.mis_hie += 1
        elif smell_name == D_BRO_HIE:
            self.bro_hie += 1

    def __str__(self):
        return str(self.unn_abs) + ',' + str(
            self.imp_abs) + ',' + str(self.mul_abs) + ',' + str(
            self.unut_abs) + ',' + str(self.dup_abs) + ',' + str(
            self.fea_env) + ',' + str(self.def_enc) + ',' + str(
            self.uxp_enc) + ',' + str(self.bro_mod) + ',' + str(
            self.ins_mod) + ',' + str(self.hub_mod) + ',' + str(
            self.cyc_mod) + ',' + str(self.wid_hie) + ',' + str(
            self.dee_hie) + ',' + str(self.mul_hie) + ',' + str(
            self.cyc_hie) + ',' + str(self.reb_hie) + ',' + str(
            self.unf_hie) + ',' + str(self.mis_hie) + ',' + str(
            self.bro_hie)

class ImplSmellCount:
    def __init__(self):
        self.long_mth = 0
        self.comp_mth = 0
        self.long_param_list = 0
        self.long_id = 0
        self.long_stmt = 0
        self.comp_cond = 0
        self.virtual_call = 0
        self.emty_catch = 0
        self.magic_no = 0
        self.dup_code = 0
        self.mis_def = 0

    def total(self):
        return self.long_mth + self.comp_mth + self.long_param_list + self.long_id + self.long_stmt + self.comp_cond + self.virtual_call + self.emty_catch + self.magic_no + self.dup_code + self.mis_def

    def count(self, line):
        tokens = line.split(',')
        if len(tokens) < 5:
            return
        smell_name = tokens[4].strip()
        if smell_name == I_LONG_MTD:
            self.long_mth += 1
        elif smell_name == I_COMP_MTD:
            self.comp_mth += 1
        elif smell_name == I_LONG_PARAM_LIST:
            self.long_param_list += 1
        elif smell_name == I_LONG_ID:
            self.long_id += 1
        elif smell_name == I_LONG_STMT:
            self.long_stmt += 1
        elif smell_name == I_COMP_COND:
            self.comp_cond += 1
        elif smell_name == I_VIRTUAL_CALL:
            self.virtual_call += 1
        elif smell_name == I_EMTY_CATCH:
            self.emty_catch += 1
        elif smell_name == I_MAGIC_NO:
            self.magic_no += 1
        elif smell_name == I_DUP_CODE:
            self.dup_code += 1
        elif smell_name == I_MIS_DEF:
            self.mis_def += 1

    def __str__(self):
        return str(self.long_mth) + ',' + str(self.comp_mth) + ',' + str(
            self.long_param_list) + ',' + str(self.long_id) + ',' + str(
            self.long_stmt) + ',' + str(self.comp_cond) + ',' + str(
            self.virtual_call) + ',' + str(self.emty_catch) + ',' + str(
            self.magic_no) + ',' + str(self.dup_code) + ',' + str(self.mis_def)


def _get_active_hash(line, hash1, hash2):
    if line.strip().endswith(hash1):
        return hash1
    if line.strip().endswith(hash2):
        return hash2
    print('Error state: hash must be one of the commit hashes')
    return None


def _write_to_csv(out_file, hash1, hash2, missing_arch_smells1, missing_arch_smells2, missing_design_smells1,
                  missing_design_smells2,
                  missing_impl_smells1, missing_impl_smells2):
    total1 = missing_arch_smells1.total() + missing_design_smells1.total() + missing_impl_smells1.total()
    total2 = missing_arch_smells2.total() + missing_design_smells2.total() + missing_impl_smells2.total()
    line = hash1 + ',' + hash2 + ',' + str(missing_arch_smells1) + ',' + str(missing_design_smells1) + ',' + str(missing_impl_smells1) + ',' + str(missing_arch_smells2) + ',' + str(missing_design_smells2) + ',' + str(missing_impl_smells2) + ',' + str(
        total1) + ',' + str(total2) + '\n'
    out_file.write(line)


def compare_quantify(folder_path):
    with open('compare_quantify.csv', 'w') as out_file:
        out_file.write(
            'hash1,hash2,A_AMB_INT1,A_FEA_CON1,A_UNS_DEP1,A_CYC_DEP1,A_DEN_STR1,A_SCA_FUN1,A_GOD_COM1,D_UNN_ABS1,D_IMP_ABS1,D_MUL_ABS1,D_UNUT_ABS1,D_DUP_ABS1,D_FEA_ENV1,D_DEF_ENC1,D_UXP_ENC1,D_BRO_MOD1,D_INS_MOD1,D_HUB_MOD1,D_CYC_MOD1,D_WID_HIE1,D_DEE_HIE1,D_MUL_HIE1,D_CYC_HIE1,D_REB_HIE1,D_UNF_HIE1,D_MIS_HIE1,D_BRO_HIE1,I_LONG_MTD1,I_COMP_MTD1,I_LONG_PARAM_LIST1,I_LONG_ID1,I_LONG_STMT1,I_COMP_COND1,I_VIRTUAL_CALL1,I_EMTY_CATCH1,I_MAGIC_NO1,I_DUP_CODE1,I_MIS_DEF1,A_AMB_INT2,A_FEA_CON2,A_UNS_DEP2,A_CYC_DEP2,A_DEN_STR2,A_SCA_FUN2,A_GOD_COM2,D_UNN_ABS2,D_IMP_ABS2,D_MUL_ABS2,D_UNUT_ABS2,D_DUP_ABS2,D_FEA_ENV2,D_DEF_ENC2,D_UXP_ENC2,D_BRO_MOD2,D_INS_MOD2,D_HUB_MOD2,D_CYC_MOD2,D_WID_HIE2,D_DEE_HIE2,D_MUL_HIE2,D_CYC_HIE2,D_REB_HIE2,D_UNF_HIE2,D_MIS_HIE2,D_BRO_HIE2,I_LONG_MTD2,I_COMP_MTD2,I_LONG_PARAM_LIST2,I_LONG_ID2,I_LONG_STMT2,I_COMP_COND2,I_VIRTUAL_CALL2,I_EMTY_CATCH2,I_MAGIC_NO2,I_DUP_CODE2,I_MIS_DEF2,Total1,Total2\n')
        for file in os.listdir(folder_path):
            tokens = file.split('.')
            if len(tokens) == 4:
                hash1 = tokens[2]
                hash2 = tokens[3]
                with open(os.path.join(folder_path, file)) as file_obj:
                    smell_type = SmellType.ARCH
                    active_hash = hash1
                    missing_arch_smells1 = ArchSmellCount()
                    missing_arch_smells2 = ArchSmellCount()
                    missing_design_smells1 = DesignSmellCount()
                    missing_design_smells2 = DesignSmellCount()
                    missing_impl_smells1 = ImplSmellCount()
                    missing_impl_smells2 = ImplSmellCount()

                    for line in file_obj:
                        cur_smell_type = _get_smell_type(line)
                        if cur_smell_type is not None:
                            smell_type = cur_smell_type
                            active_hash = _get_active_hash(line, hash1, hash2)
                            continue

                        if smell_type == SmellType.ARCH:
                            if active_hash == hash1:
                                missing_arch_smells1.count(line)
                            else:
                                missing_arch_smells2.count(line)
                        elif smell_type == SmellType.DESIGN:
                            if active_hash == hash1:
                                missing_design_smells1.count(line)
                            else:
                                missing_design_smells2.count(line)
                        elif smell_type == SmellType.IMPL:
                            if active_hash == hash1:
                                missing_impl_smells1.count(line)
                            else:
                                missing_impl_smells2.count(line)
                    _write_to_csv(out_file, hash1, hash2, missing_arch_smells1, missing_arch_smells2,
                                  missing_design_smells1,
                                  missing_design_smells2, missing_impl_smells1, missing_impl_smells2)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        compare_quantify(sys.argv[1])
    else:
        print('Usage instruction: compare_quantify <path>')
