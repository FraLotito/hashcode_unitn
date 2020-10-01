import math
from collections import deque
from random import randint, choice
from time import sleep, asctime

print("Starting at", asctime().split(' ')[3])
in_file = open("in.txt")
data_file = open("data.csv", 'w')
data_file.write("Iteration, Score\n")
R, C, L, H = map(int, in_file.readline().strip().split(' '))

pizza = []

for r in range(R):
    row = list(in_file.readline().strip())
    pizza.append(row)


def dim(f):
    """ Dimensione in celle di una fetta """
    return (f[2]-f[0]+1) * (f[3]-f[1]+1)


def valid(f):
    """ Se una fetta contiene almeno L T e L M """
    m, t = 0, 0
    for r in range(f[2]-f[0]+1):
        for c in range(f[3]-f[1]+1):
            if pizza[f[0] + r][f[1] + c] == 'M': m += 1
            else: t += 1

            if m >= L and t >= L: return True

    return False


def cut(f):
    """ Taglia in una posizione casuale una fetta """

    if (f[2] - f[0]) > 1 and (randint(0, 1) or f[3] - f[1] <= 1): # Dividi Y
        cut = choice(range(f[0], f[2])) # Prima riga inclusiva, seconda no
        # print("  Cutting through Y at", cut)
        fetta_A = (f[0], f[1], cut, f[3])
        fetta_B = (cut+1, f[1], f[2], f[3])
    else:
        cut = choice(range(f[1], f[3])) # Prima colonna inclusiva, seconda no
        # print("  Cutting through X at", cut)
        fetta_A = (f[0], f[1], f[2], cut)
        fetta_B = (f[0], cut+1, f[2], f[3])

    return (fetta_A, fetta_B)


class Tree:
    def __init__(self, val, f=(0,0), father=None):
        self.val = val
        self.left = None
        self.right = None
        self.father = father
        self.fitness = f
        self.score = 0

    def __str__(self):
        """ Stampa l'albero in modo ordinato """
        s = str(self.val)
        if self.fitness != (0,0):
            s += ", F: {}/{}, S: {}".format(self.fitness[0], self.fitness[1], self.score)
        if self.left != None:
            s += '\n'
            s += '├ L: ' + '\n│    '.join(str(self.left).split('\n'))
        if self.right != None:
            s += '\n'
            s += '└ R: ' + '\n     '.join(str(self.right).split('\n'))
        return s


def visit_solution(t, trace=False):
    """ Visita l'albero della soluzione, calcola il fitness di ogni sottoalbero,
        stampa la soluzione (se trace=True) e ritorna il punteggio """

    if t.left is None or t.right is None: # Mi trovo in una foglia
        if valid(t.val):
            t.score = dim(t.val)
            t.fitness = (1, 1) # Valida 1 foglia su 1
            if trace:
                print("  {}  >>> Valid ({:02d}) <<<".format(t.val, t.score))
            return t.score
        else:
            t.score = 0
            t.fitness = (0, 1) # Valide 0 foglie su 1
            if trace:
                print("  {}  >>>      -     <<<".format(t.val))
            return t.score
    else: # Mi trovo in un sottoalbero, continuo la discesa
        t.score = visit_solution(t.left, trace) + visit_solution(t.right, trace)
        t.fitness = (t.left.fitness[0] + t.right.fitness[0],
                     t.left.fitness[1] + t.right.fitness[1])
        return t.score


def new_solution(trace=False):
    """ Nuova soluzione trovata, la stampo (con l'albero se trace=True) """

    time_string = asctime().split(' ')[3]
    print("Score: {:7d}      Fitness: {:02.1f}%       Iteration: {:6d}       At: {}\r"
        .format(T.score, T.fitness[0]/T.fitness[1]*100, iter_count, time_string), end='')
    data_file.write("{}, {}\n".format(iter_count, T.score))

    if trace:
        print('\n' + '-'*80)
        print(T, '\n')


def write_solution_to_file():
    """ Crea un file e scrivici la soluzione trovata, visitando l'albero """

    time_string = asctime().split(' ')[3]
    out = open("Solutions/solution_{}_{}.txt".format(T.score, time_string), 'w')
    out.write(str(T.fitness[0]) + '\n') # Numero di fette valide

    def write_leafs(t):
        if t.left is None or t.right is None:
            if valid(t.val):
                out.write("{} {} {} {}\n".format(t.val[0], t.val[1], t.val[2], t.val[3]))
        else:
            write_leafs(t.left)
            write_leafs(t.right)

    write_leafs(T)
    out.close()
    data_file.close()


T = Tree((0, 0, R-1, C-1))
q = deque([T])
last_score = 0
iter_count = 0

try:
    while True:
        iter_count += 1
        working_tree = q[0]

        # Finché ci sono fette da tagliare procedi con tagli casuali
        while len(q) > 0:
            curr_tree = q.popleft()
            fetta_A, fetta_B = cut(curr_tree.val)

            curr_tree.left  = Tree(fetta_A, father=curr_tree)
            curr_tree.right = Tree(fetta_B, father=curr_tree)

            if dim(fetta_A) > H:
                q.append(curr_tree.left)

            if dim(fetta_B) > H:
                q.append(curr_tree.right)


        # Visita l'albero della soluzione e calcola score e fitness dei nodi
        visit_solution(working_tree)

        # Se working_tree migliora la soluzione precedente sostituiscilo
        if working_tree.father is None: # Prima iterazione o ricostruito tutto dalla radice
            if working_tree.score > last_score:
                T = working_tree
                last_score = working_tree.score
                new_solution(trace=True)
        else: # Ristruttravo un sottoalbero
            if working_tree.score > random_subtree.score:
                # Inserisco working_tree nell'albero vero
                if last_direction == 'l':
                    working_tree.father.left = working_tree
                else:
                    working_tree.father.right = working_tree

                # Ricalcola score e fitness dei padri
                curr_node = working_tree.father
                while curr_node is not None:
                    curr_node.score = curr_node.left.score + curr_node.right.score
                    curr_node.fitness = (curr_node.left.fitness[0] + curr_node.right.fitness[0],
                                         curr_node.left.fitness[1] + curr_node.right.fitness[1])
                    curr_node = curr_node.father

                last_score = T.score
                new_solution(trace=True)

        # Scegli un sottoalbero a caso da provare a ricostruire
        random_subtree, last_direction = T, None
        # Scendo dalla radice i volte, a caso tra 0 e l'altezza massima dell'albero
        for i in range(math.ceil(math.log2(T.fitness[1]))):
            # Vado a caso a sx o dx, controllando di non scegliere un nodo "penultimo" (non avrebbe senso)
            if randint(0, 1) == 0 and random_subtree.left.left is not None:
                random_subtree = random_subtree.left
                last_direction = 'l'
            elif random_subtree.right.right is not None:
                random_subtree = random_subtree.right
                last_direction = 'r'
            else:
                break

        # Lo metto nella coda e l'iterazione riparte da questo
        q.append(Tree(random_subtree.val, father=random_subtree.father))

except KeyboardInterrupt:
    # Ctrl-C, esci e scrivi la soluzione
    print("\nWriting solution to file...")
    write_solution_to_file()
