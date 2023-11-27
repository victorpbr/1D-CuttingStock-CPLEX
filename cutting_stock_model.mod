# AMPL Model

set PIECES;  # Set of piece types
param Limit;  # Limit of bars to be cut, solver limitation
param L;  # Standard size of the bar
param a {PIECES};  # Sizes of the pieces to be cut
param b {PIECES};  # Demand for each size

var y {1..Limit} binary;  # y_j indicates whether bar j is used
var x {PIECES, 1..Limit} integer >= 0;  # x_ij indicates if piece i is cut from bar j

# Constraints
# Demand satisfaction
subject to DemandSatisfaction {i in PIECES}:
    sum {j in 1..Limit} x[i,j] = b[i];

# Stock size limitation
subject to StockLimitation {j in 1..Limit}:
    sum {i in PIECES} a[i] * x[i,j] <= L * y[j];

# Linking constraint
subject to LinkingConstraint {i in PIECES, j in 1..Limit}:
    x[i,j] <= (L div a[i]) * y[j];

# Cutting order
subject to CuttingOrder {j in 2..Limit}:
    y[j-1] >= y[j];

# Objective: Minimize the number of bars used
minimize TotalBarsUsed: sum {j in 1..Limit} y[j];
