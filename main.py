from docplex.mp.model import Model

#   O objetivo deste modelo é implementar o problema de corte de estoque 1D, onde um tamanho padrão de barra é definido
# e a partir dele, são cortados pedaços de tamanhos diferentes, de forma a minimizar o desperdício de material. É também obtido um plano de corte.
#

# Instanciando o modelo
mdl = Model(name='1D-CuttingStock')

# Definindo os parâmetros

Limit = 10 # Limite de barras a serem cortadas, limitação do solver

L = 3000 # Tamanho padrão da barra

a = [100, 200, 300, 400, 500] # Tamanhos dos pedaços a serem cortados
b = [1, 2, 3, 4, 5] # Demanda de cada tamanho

n = len(a) # Número de tamanhos diferentes

# Definindo as restrições

# Definindo as variáveis de decisão 
# y_j indicates whether stock piece j is used
y = [mdl.binary_var(name=f"y_{j}") for j in range(Limit)]  # Assuming a maximum of 1000 stock pieces

# x_ij indicates if a piece of type i is cut from stock piece j
x = [[mdl.binary_var(name=f"x_{i}_{j}") for j in range(Limit)] for i in range(n)]

# Constraints
# Demand satisfaction: each piece type's demand must be met
for i in range(n):
    mdl.add_constraint(mdl.sum(x[i][j] for j in range(Limit)) == b[i], f"Demand_{i}")

# Stock limitation: the total length of pieces cut from a stock piece must not exceed its length
for j in range(Limit):
    mdl.add_constraint(mdl.sum(a[i] * x[i][j] for i in range(n)) <= L * y[j], f"Stock_{j}")

# Linking constraint: x_ij can be 1 only if y_j is 1
for i in range(n):
    for j in range(Limit):
        mdl.add_constraint(x[i][j] <= y[j], f"Link_{i}_{j}")

# Ordering constraint to use lower-indexed stock pieces first
for j in range(1, Limit):
    mdl.add_constraint(y[j-1] >= y[j], f"Order_{j}")

# Objective function: Minimize the total number of stock pieces used
mdl.minimize(mdl.sum(y[j] for j in range(Limit)))

# Solve the model
solution = mdl.solve(log_output=True)

# Print the solution
if solution:
    print("Solution found:\n")
    print(f"Number of stock pieces needed: {solution.get_value(mdl.sum(y[j] for j in range(Limit)))}")
    for i in range(n):
        for j in range(Limit):
            if x[i][j].solution_value > 0.5:
                print(f"Cut piece of length {a[i]} from stock piece {j}")
else:
    print("No solution found.")