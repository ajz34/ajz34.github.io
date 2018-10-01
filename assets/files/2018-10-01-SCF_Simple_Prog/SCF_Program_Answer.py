import numpy as np


def ltouts_to_symm_matrix(lst, dim):

    # we import a list with split strings, and the dimension we desire
    mat = np.zeros((dim, dim))
    column_ind = []
    for line in lst:
        # judge whether this line contains matrix elements
        if (len(line) > 1) and (len(line[1]) > 5) and ((line[1][1] == '.') or (line[1][2] == '.')):
            row_ind = int(line[0])
            for ind_elem, elem in enumerate(line[1:]):
                mat_elem = float(elem.replace('D', 'E'))
                mat[row_ind-1, column_ind[ind_elem]-1] = mat_elem
                mat[column_ind[ind_elem]-1, row_ind-1] = mat_elem
        else:
            column_ind = np.array(line, dtype=int)
    return mat


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
            while True:
                line = file.readline()
                if line[7:22] == "basis functions":
                    break
            self.num_ao = int(line.split()[0])
            line = file.readline()
            self.num_occ = int(line.split()[0])
            line = file.readline()
            self.val_neu_repulsion_energy = float(line.split()[3])
        return self

    def hard_type_int_rhf(self, file_path):
        with open(file_path, "r") as file:
            # Find Overlap
            while True:
                line = file.readline()
                if line[:16] == " *** Overlap ***":
                    break
            parse_line = []
            while True:
                line = file.readline()
                if line[1] == ' ':
                    parse_line.append(line.split())
                else:
                    break
            self.mat_overlap = ltouts_to_symm_matrix(parse_line, self.num_ao)
            # Find Core Hamiltonian
            while True:
                line = file.readline()
                if line[:31] == " ****** Core Hamiltonian ******":
                    break
            parse_line = []
            while True:
                line = file.readline()
                if line[1] == ' ':
                    parse_line.append(line.split())
                else:
                    break
            self.mat_core_hamiltonian = ltouts_to_symm_matrix(parse_line, self.num_ao)
            # Find two-electron integral
            with open(file_path) as log_file:
                # Read Number of Basis Functions
                while True:
                    log_line = log_file.readline()
                    if log_line[:39] == " *** Dumping Two-Electron integrals ***":
                        break
                for ind in range(6):
                    log_line = log_file.readline()
                mat = np.zeros((self.num_ao, self.num_ao, self.num_ao, self.num_ao))
                while True:
                    log_line = log_file.readline()
                    try:
                        ind_i = int(log_line[3: 6]) - 1
                        ind_j = int(log_line[9:12]) - 1
                        ind_k = int(log_line[15:18]) - 1
                        ind_l = int(log_line[21:24]) - 1
                        twoe_val = float(log_line[30:49].replace("D", "E"))
                        mat[ind_i, ind_j, ind_k, ind_l] = \
                            mat[ind_i, ind_j, ind_l, ind_k] = \
                            mat[ind_j, ind_i, ind_k, ind_l] = \
                            mat[ind_j, ind_i, ind_l, ind_k] = \
                            mat[ind_k, ind_l, ind_i, ind_j] = \
                            mat[ind_k, ind_l, ind_j, ind_i] = \
                            mat[ind_l, ind_k, ind_i, ind_j] = \
                            mat[ind_l, ind_k, ind_j, ind_i] = \
                            twoe_val
                    except:  # anything reading failure, use bare except
                        break
            self.tsr_twoe_int = mat
        return self

    def scf_rhf(self):
        # Give X = S^{-1/2} matrix through svd
        S = self.mat_overlap  # (3.161)
        s, U = np.linalg.eigh(S)  # (3.166)
        X = U.dot(np.diag(s**(-1/2))).dot(U.T)  # (3.167)
        nbasis = self.num_ao
        nocc = self.num_occ
        P = np.zeros((nbasis, nbasis))  # p148
        H = self.mat_core_hamiltonian  # (3.153)
        R = self.tsr_twoe_int  # (uv|sl) storage
        dev_p = 1  # deviation of P matrix between iterations
        dev_e = 1  # deviation of energy between iterations
        energy = 0.0e+0
        C = None
        e = None
        count_scf = 0
        while (dev_p > 1e-8) or (dev_e > 1e-8):
            P_old = np.copy(P)
            energy_old = np.copy(energy)
            F = H +\
                np.einsum("ls,uvsl->uv", P, R) + \
                np.einsum("ls,ulsv->uv", P, R) * -1/2  # (3.154)
            F_prime = X.T.dot(F).dot(X)
            e, C_prime = np.linalg.eigh(F_prime)  # probably np.linalg.eigh has eigens sorted
            C = X.dot(C_prime)
            P = 2 * C[:,:nocc].dot(C[:,:nocc].T)
            energy = 0.5 * np.trace(P.dot(H+F))
            dev_p = np.sum((P-P_old)**2)
            dev_e = np.abs(energy - energy_old)
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
        self.mat_coef = C
        self.vec_eig = e
        self.val_SCF_energy = energy
        return self
