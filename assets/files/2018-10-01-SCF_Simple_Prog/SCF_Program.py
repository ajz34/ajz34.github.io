import numpy as np


def print_mat(mat, symm=True):
    if mat is None:
        print("Current matrix does not exist!")
        print()
        return
    num_row = mat.shape[0]
    try:
        num_col = mat.shape[1]
    except IndexError:  # vector case
        mat.resize(1, mat.shape[0])
        num_row = 1
        num_col = mat.shape[1]
    if num_row != num_col:
        symm = False
    cur_col = 0
    while cur_col < num_col:
        print()
        cur_end = min(cur_col + 5, num_col)
        print(" col" + "".join(["{:14d}"] * (cur_end - cur_col)).format(*[i + 1 for i in range(cur_col, cur_end)]))
        print(" ---" + "".join(["  ------------"] * (cur_end - cur_col)))
        if symm:
            for i in range(cur_col, num_row):
                cur_col_num = min(i - cur_col + 1, 5)
                print("{:4d}".format(i+1) +
                      "".join(["{:14.5e}"] * cur_col_num).format(*[mat[i, cur_col + j] for j in range(cur_col_num)]))
        else:
            for i in range(num_row):
                cur_col_num = min(num_col - cur_col, 5)
                print("{:4d}".format(i+1) +
                      "".join(["{:14.5e}"] * cur_col_num).format(*[mat[i, cur_col + j] for j in range(cur_col_num)]))
        cur_col = cur_end
    print()
    return


class Molecule:

    def __init__(self):
        """
        num_occ: (int) number of occupied orbital
        num_virt: (int) number of virtual orbital
        num_ao: (int) number of atomic orbital (in this case, equal to number of molecular orbital)
        mat_overlap: (np.array) defined at (p 142, eq 3.161)
        mat_core_hamiltonian: (np.array) defined at (p 140, eq 3.149)
        tsr_twoe_int: (np.array) defined at (p 141, eq 3.155)
        mat_coef: (np.array) defined at (p 136, eq 3.133)
        vec_eig: (np.array) eigenvalues of this system, or Fock matrix diagonal values in MO basis
        val_neu_repulsion_energy: (float) nuclei repulsion, constant when atom coordinates defined
        val_SCF_energy: (float) electronic energy
        """
        self.num_occ = None
        self.num_virt = None
        self.num_ao = None
        self.mat_overlap = None
        self.mat_core_hamiltonian = None
        self.tsr_twoe_int = None
        self.mat_coef = None
        self.vec_eig = None
        self.val_neu_repulsion_energy = None
        self.val_SCF_energy = None

    def hard_type_orbital_rhf(self, file_path):
        with open(file_path, "r") as file:
            # ----- Write your code here
            pass
        return self

    def hard_type_int_rhf(self, file_path):
        with open(file_path, "r") as file:
            # ----- Write your code here
            pass
        return self

    def scf_rhf(self):
        dev_p = 1  # deviation of P matrix between iterations
        dev_e = 1  # deviation of energy between iterations
        energy = 0.0e+0
        P = None  # Density matrix in atomic orbital
        P_old = None  #
        energy_old = -100.0e+0
        F = None
        C = None
        e = None
        count_scf = 0
        # ----- Make definitions here
        pass
        while (dev_p > 1e-8) or (dev_e > 1e-8):
            # ----- Write your code here
            pass
            # threshold condition
            dev_p = np.sum((P-P_old)**2)
            dev_e = np.abs(energy - energy_old)
            # print
            if count_scf < 3:
                print("*** SCF Step: ", count_scf + 1, " ***")
                print("SCF Energy: ", self.val_neu_repulsion_energy + energy)
                print()
                print("Density guess in atomic basis")
                print_mat(P_old)
                print("Fock matrix in atomic basis")
                print_mat(F)
                print("MO <-> AO coefficient matrix")
                print_mat(C, symm=False)
                print("Eigenvalues of this step")
                print_mat(e)
            else:
                print("*** SCF Step: ", count_scf + 1, " ***")
                print("SCF Energy: ", self.val_neu_repulsion_energy + energy)
            count_scf += 1
        # ----- Finish your code here
        pass
        return self
