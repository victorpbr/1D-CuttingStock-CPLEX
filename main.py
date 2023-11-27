import sys
import docplex.mp

from docplex.mp.model import Model

# Criando instância do modelo
mdl = Model("1D-CuttingStock")

#Definindo variáveis

n = 1  # Number of different lengths of pieces required
m = 1  # Number of available stock lengths
L = [100, 150]  # Length of each stock piece
l = [30, 45, 50]  # Length of each required piece
d = [4, 6, 3]  # Demand for pieces of each length


# Criando variáveis de decisão
x = [[mdl.integer_var(name=f"x_{i}_{j}", lb=0) for j in range(n)] for i in range(m)]

# Criando restrições
# Restrição de demanda
for j in range(n):
    mdl.add_constraint(mdl.sum(x[i][j] for i in range(m)) >= d[j], f"Demand_{j}")

# Restrição de estoque
for i in range(m):
    mdl.add_constraint(mdl.sum(l[j] * x[i][j] for j in range(n)) <= L[i], f"Stock_{i}")

# Função objetivo
mdl.minimize(mdl.sum(l[j] * x[i][j] for i in range(m) for j in range(n)))

# Solve the model
solution = mdl.solve(log_output=True)

# Print the solution
if solution:
    print("Solution found:\n")
    for i in range(m):
        for j in range(n):
            print(f"Number of pieces of length {l[j]} cut from stock {i}: {x[i][j].solution_value}")
else:
    print("No solution found.")