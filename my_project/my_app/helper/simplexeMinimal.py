import numpy as np
from copy import deepcopy

# fonction retournant le numero de colonne de la variable entrante


def variable_entrante(A):
    ligne, colonne = np.shape(A)
    z = A[ligne-1, :]
    return np.argmin(z)

# fonction retournant le numero de ligne de la variable sortante


def variable_sortante(A, q):

    line, col = np.shape(A)
    col_p = A[:line-2, q]
    col_constante = A[:line-2, col-2]
    c = []
    for i in range(1, len(col_p)):
        if col_p[i] > 0:
            c.insert(i, col_constante[i]/col_p[i])
        else:
            c.insert(i, 10000000)
    c.insert(0, 10000000)
    return np.argmin(c)

# fonction du pivot, ecriture des variables de bases en fonctions des variables hors bases
# par combinaison linéaire des lignes par la lignes du pivot p, la colonne du pivot q


def pivot(A, p, q):
    N = deepcopy(A)
    ligne, colonne = np.shape(N)

    for i in range(1, ligne-2):
        if i == p:
            N[i, :-1] = A[i, :-1]/A[i, q]
        else:
            N[i, :-1] = A[i, :-1] - A[i, q]/A[p, q]*A[p, :-1]

    return N

# fonction calculant zi et ci-zi


def zi_cizi(A):
    l, m = np.shape(A)
    cb = A[1:l-2, m-1]
    for i in range(m-1):
        # calcul zi
        A[-2, i] = sum(A[1:l-2, i]*cb)
    for i in range(m-2):
        A[-1, i] = A[0, i] - A[-2, i]


def simplexe(A):
    # copie du tableau simplexe afin d'effectuer les opérations
    X = A.copy()
    l, m = np.shape(A)
    # calcul de zi
    zi_cizi(X)
    nb_pivotement = 1

    # tant qu'il y a des positifs sur la dernière ligne
    # tant que la variable entrante est positive
    while X[X.shape[0]-1, variable_entrante(X)] < 0:
        # récupération de la ligne et de la colonne pivot

        index_colonne_pivot = variable_entrante(X)
        index_ligne_pivot = variable_sortante(X, index_colonne_pivot)

        # modifier cb à chaque entrée dans la base d'une variable
        X[index_ligne_pivot, m-1] = X[0, index_colonne_pivot]

        # pivotement
        X = pivot(X, index_ligne_pivot, index_colonne_pivot)
        zi_cizi(X)
        nb_pivotement += 1

    z = X[l-2, -2]
    p = point(X)
   
    #retourner les solutions et la valeur minimisé
    return (z, p)


def index_du_un_de_colonne(A, colonne):
    l, m = np.shape(A)

    for i in range(1, l-2):
        if A[i][colonne] == 1:
            return i


def point(A):
    l, m = np.shape(A)

    B = []
    for i in np.arange(m):
        if i < m-2:
            if A[l-1, i] == 0:
                index_ligne_du_un = index_du_un_de_colonne(A, i)
                B.insert(i, A[index_ligne_du_un, m-2])
            else:
                B.insert(i, 0)

    return B

"""A = np.array([
  [4, 0, 1, 0, 0, 0, 300],
  [0, 1, 0, 1, 0, 0, 400],
  [1, 1, 0, 0, 1, 0, 500],
  [2, 1, 0, 0, 0, 1, 700],
  [7, 5, 0, 0, 0, 0, 0]
])

print(f'Simplexe de base = \n {A} \n')

X = simplexe(A)"""

    