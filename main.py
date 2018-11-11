from scipy.optimize import linprog
from fractions import Fraction
from decimal import Decimal
from plotly import tools
import plotly.graph_objs as go
import plotly.plotly as py

#FUNCTION
def nash_equilibrium(a):
        m = int(len(a))
        n = int(len(a[0]))
#Adding MIN if < 0 to A
        mina = 1
        for i in range(m):
                for j in range(n):
                        if(a[i][j] < mina) :
                                mina = a[i][j]
        if(mina < 0):
               for i in range(m):
                       for j in range(n):
                               a[i][j] -= mina
#PART 1 (Second player first, cause no transpon Matrix needed)
        for i in range(m):
                for j in range(n):
                        a[i][j] = -a[i][j]     #Sure, -A is hard
        B1 = []
        C1 = []
        Bounds1 = []
        for i in range(m):
                B1.append(1)
        for j in range(n):
                C1.append(1)
                Bounds1.append((None, 0))       #  z = -x <= 0
        res1 = linprog(C1, a, B1, bounds=Bounds1)   #Simplex is here
        q = res1.x
        V = 1/res1.fun                          #   V < 0 cause of z = -x. z*V still >0
        
#PART 2
        At = list(map(list, zip(*a)))             #Transposing A
        B2 = []
        C2 = []
        Bounds2 = []
        for j in range(n):
                B2.append(-1)
        for i in range(m):
                C2.append(1)
                Bounds2.append((0, None))       # y >= 0
        res2 = linprog(C2, At, B2, bounds=Bounds2)   #Simplex is here
        p = res2.x
        U = 1/res2.fun
#PRINTING
        print("| p |", end='| ')
        for i in range(m):
                p[i] *= U
                print(Fraction(Decimal(p[i])).limit_denominator(1000), end='| ') #Fractions
        
        print("\n| q |", end='| ')
        for j in range(n):
                q[j] *= V
                print(Fraction(Decimal(q[j])).limit_denominator(1000), end='| ') #Fractions
        if(mina < 0):
            U += mina
        print("\n| u |", end='| ')
        print(Fraction(Decimal(U)).limit_denominator(1000), '|')
#RETURN ALL WE BROKE
        for i in range(m):
                for j in range(n):
                        a[i][j] = -a[i][j]
                        if(mina < 0):
                            a[i][j] += mina
        return [U, p, q]

#MAIN
A = [[2.0, 3.0, -1.0], [1.0, 1.0, 0.0], [1.0, -2.0, -1.0]]

RES = nash_equilibrium(A)
print(RES)

#PLOTTING
m = int(len(A))
n = int(len(A[0]))
X1 = []
X2 = []
for i in range(m):
    X1.append(i+1)
for i in range(n):
    X2.append(i+1)
    
trace1 = go.Scatter( x = X1, 
          y =  RES[1], 
          mode = "markers")
trace2 = go.Scatter( x = X2, 
          y =  RES[2], 
          mode = "markers")

fig = tools.make_subplots(rows=2, cols=1, subplot_titles=('Player 1', 'Player 2'))

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 2, 1)

fig['layout'].update(height=1400, width=900, title='Player Strategies')

py.iplot(fig, filename='Results')
