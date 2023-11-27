from amplpy import AMPL, Environment

ampl = AMPL()  # Initialize AMPL environment
# Load the model (assuming the model is written in a file named 'cutting_stock_model.mod')

ampl.read('cutting_stock_model.mod')

# Definindo os parâmetros
Limit = 550 # Limite de barras a serem cortadas, limitação do solver

L = 3000 # Tamanho padrão da barra

a = [400,600,700,800,900,1100,1200,1800] # Tamanhos dos pedaços a serem cortados
b = [190,285,95,95,380,190,95,95] # Demanda de cada tamanho
n = len(a) # Número de tamanhos diferentes

# Set data
ampl.set['PIECES'] = range(len(a))
ampl.param['Limit'] = Limit
ampl.param['L'] = L
ampl.param['a'] = {i: a[i] for i in range(len(a))}
ampl.param['b'] = {i: b[i] for i in range(len(b))}

# Choose a solver
ampl.setOption('solver', 'highs')  # or another solver like 'glpk'
ampl.setOption('display', 1)  # Display solver output
ampl.setOption('solver_msg', 1)  # Show messages from the solver
# Solve the problem
ampl.solve()

# Retrieve and print the solution
print("Number of stock pieces needed:", ampl.getValue("TotalBarsUsed"))
for j in range(1, Limit + 1):
    stock_piece_used = ampl.getValue(f'y[{j}]')
    if stock_piece_used > 0.5:
        print(f"\nStock piece {j} is used.")
        for i in range(len(a)):
            num_cuts = ampl.getValue(f'x[{i},{j}]')
            if num_cuts > 0:
                print(f"  Cut {num_cuts} piece(s) of length {a[i]} from stock piece {j}")