#!/usr/bin/env python3
import sys

# Colour constants
DARK = 2
WHITE = 3

# Order of the squares
n = 10

# Transversal type data for the square types
# The ith entry of each list represents that row i has form p_i (has i whites in the last 4 columns)
transversal_types = {
'R': 8*[1] + 2*[4],
'S': 7*[1] + 3*[3],
'T': 7*[1] + [2] + [3] + [4],
'U': 6*[1] + 2*[2] + 2*[3],
'V': 6*[1] + 3*[2] + [4],
'W': 5*[1] + 4*[2] + [3],
'X': 4*[1] + 6*[2]
}

use_z4 = "-z4" in sys.argv
if use_z4: sys.argv.remove("-z4")
use_z2xz2 = "-z2xz2" in sys.argv
if use_z2xz2: sys.argv.remove("-z2xz2")
if "-z4z2xz2" in sys.argv: use_z4 = True; use_z2xz2 = True; sys.argv.remove("-z4z2xz2")
use_triple = "-triple" in sys.argv
if use_triple: sys.argv.remove("-triple")
use_direct_extension = "-direct-extension" in sys.argv
if use_direct_extension: sys.argv.remove("-direct-extension")
if use_direct_extension and not use_triple:
	print("-direct-extension requires -triple")
	quit()
use_distinguished_subsquare = "-distinguished-subsquare" in sys.argv
if use_distinguished_subsquare: sys.argv.remove("-distinguished-subsquare")
if use_distinguished_subsquare and not (use_triple and use_direct_extension):
	print("-distinguished-subsquare requires -triple -direct-extension")
	quit()
use_pairwise_onehot = "-pairwise-onehot" in sys.argv
if use_pairwise_onehot: sys.argv.remove("-pairwise-onehot")
p0_case = None
for flag, value in [("-p0a", 3), ("-p0b", 2), ("-p0c", 1)]:
	if flag in sys.argv:
		if p0_case is not None:
			print("At most one of -p0a, -p0b, and -p0c may be used")
			quit()
		p0_case = value
		sys.argv.remove(flag)
l01_case = None
for value in range(n):
	flag = "-l01-{}".format(value)
	if flag in sys.argv:
		if l01_case is not None:
			print("At most one -l01-k flag may be used")
			quit()
		l01_case = value
		sys.argv.remove(flag)
if l01_case is not None and not use_triple:
	print("-l01-k requires -triple")
	quit()
lfirstpair_case = None
for a in range(4, n):
	for b in range(a+1, n):
		flag = "-lfirstpair-{}{}".format(a, b)
		if flag in sys.argv:
			if lfirstpair_case is not None:
				print("At most one -lfirstpair-ab flag may be used")
				quit()
			lfirstpair_case = (a, b)
			sys.argv.remove(flag)
if lfirstpair_case is not None and not use_distinguished_subsquare:
	print("-lfirstpair-ab requires -distinguished-subsquare")
	quit()
sigma_case = None
for flag, value in [("-sigma-12", "12"), ("-sigma-8+4", "8+4"),
					("-sigma-6+6", "6+6"), ("-sigma-4+4+4", "4+4+4")]:
	if flag in sys.argv:
		if sigma_case is not None:
			print("At most one -sigma-* flag may be used")
			quit()
		sigma_case = value
		sys.argv.remove(flag)
if sigma_case is not None and not use_distinguished_subsquare:
	print("-sigma-* requires -distinguished-subsquare")
	quit()
darkcol0_case = None
for value in range(6):
	flag = "-darkcol0-{}".format(value)
	if flag in sys.argv:
		if darkcol0_case is not None:
			print("At most one -darkcol0-k flag may be used")
			quit()
		darkcol0_case = value
		sys.argv.remove(flag)
whitegraph_case = None
for value in range(9):
	flag = "-whitegraph-{}".format(value)
	if flag in sys.argv:
		if whitegraph_case is not None:
			print("At most one -whitegraph-k flag may be used")
			quit()
		whitegraph_case = value
		sys.argv.remove(flag)
if darkcol0_case is not None and whitegraph_case is not None:
	print("-darkcol0-k and -whitegraph-k are alternative orbit splits")
	quit()
fixedstar_case = None
for value in range(6):
	flag = "-fixedstar-{}".format(value)
	if flag in sys.argv:
		if fixedstar_case is not None:
			print("At most one -fixedstar-k flag may be used")
			quit()
		fixedstar_case = value
		sys.argv.remove(flag)
if fixedstar_case is not None and whitegraph_case is None:
	print("-fixedstar-k requires -whitegraph-k")
	quit()
if fixedstar_case is not None and p0_case is None:
	print("-fixedstar-k requires one of -p0a, -p0b, or -p0c")
	quit()

# Verify that square names are provided
if len(sys.argv) <= 1 or len(sys.argv[1]) <= 1:
	print("Need to provide the names of the squares as first command-line argument: e.g., VX")
	print("Optionally pass -z4 or -z2xz2 to encode subsquare consistency constraints for Z_4 or Z_2 x Z_2")
	quit()

# Verify the square types are valid
P_type = sys.argv[1][0]
Q_type = sys.argv[1][1]

if not P_type in ['R','S','T','U','V','W','X']:
	print("Incorrect first square type. Type must be one of {R,S,T,U,V,W,X}.")
	quit()

if not Q_type in ['R','S','T','U','V','W','X']:
	print("Incorrect second square type. Type must be one of {R,S,T,U,V,W,X}.")
	quit()
if darkcol0_case is not None and not (use_distinguished_subsquare and P_type == 'U' and Q_type == 'U'):
	print("-darkcol0-k requires distinguished type UU")
	quit()
if whitegraph_case is not None and not (use_distinguished_subsquare and P_type == 'U' and Q_type == 'U'):
	print("-whitegraph-k requires distinguished type UU")
	quit()

# Multi-dimensional arrays to hold the variables used in the encoding
Pc = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Colours of square P
Qc = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Colours of square Q
P = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Symbols of square P
Q = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Symbols of square Q
Z = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Witness square ensuring (P,Q) is a transversal representation pair
if use_triple:
	L = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Third mutual transversal representation
	if use_direct_extension:
		PE = [[[0 for j in range(n)] for ip in range(n)] for i in range(n)] # P/L row-agreement indicators
		QE = [[[0 for j in range(n)] for ip in range(n)] for i in range(n)] # Q/L row-agreement indicators
	else:
		PL = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Witness for (P,L)
		QL = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Witness for (Q,L)

# Counter for # of variables used in SAT instance
total_vars = 0
# List to hold clauses of SAT instance
clauses = []

# Generate a clause containing the literals in the set X
def generate_clause(X):
	clause = ""
	for x in X:
		clause += str(x) + " "
	clauses.append(clause + "0")

# Generate a clause specifying (x1 & ... & xn) -> (y1 | ... | yk) where X = {x1, ..., xn} and Y = {y1, ..., yk}
def generate_implication_clause(X, Y):
	if 'F' in X or 'T' in Y:
		return
	while 'T' in X: X.remove('T')
	while 'F' in Y: Y.remove('F')
	clause = ""
	for x in X:
		clause += str(-x) + " "
	for y in Y:
		clause += str(y) + " "
	clauses.append(clause + "0")

# Generate clauses encoding exactly one variable in X is assigned true
def generate_exactly_one_clauses(X):
	if use_pairwise_onehot:
		generate_clause(X)
		for i in range(len(X)):
			for j in range(i+1, len(X)):
				generate_clause({-X[i], -X[j]})
	else:
		generate_adder_clauses(X, 1, 1)

# Return the number of leaves under node k in the complete binary tree with N nodes
def num_leaves_under(N, k):
	if k >= N: return 0
	if 2*k+1 >= N: return 1
	return num_leaves_under(N, 2*k+1) + num_leaves_under(N, 2*k+2)

# Generate clauses encoding that <= s variables and >= l variables in X are assigned true using the totalizer encoding
def generate_adder_clauses(X, l, s):
	global total_vars

	n = len(X)
	# Totalizer auxiliary variables
	R = [['F' for j in range(n+2)] for i in range(2*n-1)]
	for i in range(2*n-1):
		R[i][0] = 'T'

	for i in range(n-1):
		t = num_leaves_under(2*n-1, i)
		for j in range(t):
			total_vars += 1
			R[i][j+1] = total_vars
	for i in range(n-1, 2*n-1):
		R[i][1] = X[i-n+1]

	for i in range(n-1):
		m = num_leaves_under(2*n-1, i)
		for sigma in range(m+1):
			# Solve alpha + beta = sigma
			for alpha in range(sigma+1):
				beta = sigma - alpha
				generate_implication_clause({R[2*i+1][alpha], R[2*i+2][beta]}, {R[i][sigma]})
				generate_implication_clause({R[i][sigma+1]}, {R[2*i+1][alpha+1], R[2*i+2][beta+1]})

	for i in range(1,l+1):
		generate_clause({R[0][i]})
	for i in range(s+1,n+1):
		generate_clause({-R[0][i]})

# Define colour variables for P
for i in range(n):
	for j in range(n):
		for k in range(n):
			total_vars += 1
			Pc[i][j][k] = total_vars

# Define colour variables for Q
for i in range(n):
	for j in range(n):
		for k in range(n):
			total_vars += 1
			Qc[i][j][k] = total_vars

# Define symbol variables for P
for i in range(n):
	for j in range(n):
		for k in range(n):
			total_vars += 1
			P[i][j][k] = total_vars

# Define symbol variables for Q
for i in range(n):
	for j in range(n):
		for k in range(n):
			total_vars += 1
			Q[i][j][k] = total_vars

# Define symbol variables for Z
for i in range(n):
	for j in range(n):
		for k in range(n):
			total_vars += 1
			Z[i][j][k] = total_vars

if use_triple:
	# Define symbol variables for the third square.
	for A in [L]:
		for i in range(n):
			for j in range(n):
				for k in range(n):
					total_vars += 1
					A[i][j][k] = total_vars
	if use_direct_extension:
		for E in [PE, QE]:
			for i in range(n):
				for ip in range(n):
					for j in range(n):
						total_vars += 1
						E[i][ip][j] = total_vars
	else:
		# Define symbol variables for the two new composition witnesses.
		for A in [PL, QL]:
			for i in range(n):
				for j in range(n):
					for k in range(n):
						total_vars += 1
						A[i][j][k] = total_vars

# Constraints ensuring that Q = PZ
for i in range(n):
	for j in range(n):
		for k in range(n):
			for ip in range(n):
				generate_implication_clause({P[i][j][k], Q[ip][j][k]}, {Z[ip][j][i]})
				generate_implication_clause({P[i][j][k], Z[ip][j][i]}, {Q[ip][j][k]})
				generate_implication_clause({Z[ip][j][i], Q[ip][j][k]}, {P[i][j][k]})

# Z must be a Latin square
for i in range(n):
	for j in range(n):
		generate_exactly_one_clauses([Z[i][k][j] for k in range(n)])
		generate_exactly_one_clauses([Z[i][j][k] for k in range(n)])
		generate_exactly_one_clauses([Z[k][i][j] for k in range(n)])

if use_triple:
	if use_direct_extension:
		# E[i][ip][j] is true exactly when row i of A and row ip of L
		# agree in column j.  A and L are a TRP exactly when every row
		# pair has at most one true agreement indicator.
		for A, E in [(P, PE), (Q, QE)]:
			for i in range(n):
				for ip in range(n):
					for j in range(n):
						for k in range(n):
							generate_implication_clause({A[i][j][k], L[ip][j][k]}, {E[i][ip][j]})
							generate_implication_clause({E[i][ip][j], A[i][j][k]}, {L[ip][j][k]})
							generate_implication_clause({E[i][ip][j], L[ip][j][k]}, {A[i][j][k]})
					for j in range(n):
						for jp in range(j+1, n):
							generate_clause({-E[i][ip][j], -E[i][ip][jp]})
					generate_clause([E[i][ip][j] for j in range(n)])
			# Latin-square propagation for the agreement coordinates.  These
			# constraints follow from A and L being Latin and E encoding their
			# agreements, but expose the implied exact-one structure directly.
			for i in range(n):
				for j in range(n):
					generate_clause([E[i][ip][j] for ip in range(n)])
					for ip in range(n):
						for ipp in range(ip+1, n):
							generate_clause({-E[i][ip][j], -E[i][ipp][j]})
			for ip in range(n):
				for j in range(n):
					generate_clause([E[i][ip][j] for i in range(n)])
					for i in range(n):
						for iprime in range(i+1, n):
							generate_clause({-E[i][ip][j], -E[iprime][ip][j]})
		# Composition coherence.  Writing Q=PZ, L=P*PL, and L=Q*QL
		# gives PL=Z*QL after cancelling P column by column.  PE and QE
		# are one-hot encodings of PL and QL, respectively.  The clauses
		# below are redundant consequences of the three pair relations,
		# but expose their shared named-coordinate correlation directly.
		for ell in range(n):
			for j in range(n):
				for qrow in range(n):
					for prow in range(n):
						generate_implication_clause({QE[qrow][ell][j], Z[qrow][j][prow]}, {PE[prow][ell][j]})
						generate_implication_clause({QE[qrow][ell][j], PE[prow][ell][j]}, {Z[qrow][j][prow]})
						generate_implication_clause({Z[qrow][j][prow], PE[prow][ell][j]}, {QE[qrow][ell][j]})
		latin_squares = [L]
	else:
		# Enforce that (P,L) and (Q,L) are TRPs.  This is the same
		# composition-square encoding used above for (P,Q).
		for A, W in [(P, PL), (Q, QL)]:
			for i in range(n):
				for j in range(n):
					for k in range(n):
						for ip in range(n):
							generate_implication_clause({A[i][j][k], L[ip][j][k]}, {W[ip][j][i]})
							generate_implication_clause({A[i][j][k], W[ip][j][i]}, {L[ip][j][k]})
							generate_implication_clause({W[ip][j][i], L[ip][j][k]}, {A[i][j][k]})
		latin_squares = [L, PL, QL]

	# L, and composition witnesses when present, must be Latin squares.
	for A in latin_squares:
		for i in range(n):
			for j in range(n):
				generate_exactly_one_clauses([A[i][k][j] for k in range(n)])
				generate_exactly_one_clauses([A[i][j][k] for k in range(n)])
				generate_exactly_one_clauses([A[k][i][j] for k in range(n)])

	# For a generic extension, row permutations of L preserve all three TRP
	# conditions, so normalize the first column.  When L is the distinguished
	# square, its row coordinates instead carry the fixed subsquare below.
	if not use_distinguished_subsquare:
		for i in range(n):
			generate_clause({L[i][0][i]})
	else:
		# Permuting the six rows outside the subsquare does not affect L's
		# fixed bottom-right block or any TRP relation.  Sort those rows by
		# their first-column symbols to remove this residual factor of 6!.
		if sigma_case is None:
			for i in range(5):
				for k in range(n):
					for l in range(k):
						generate_implication_clause({L[i][0][k]}, {-L[i+1][0][l]})
			# The bottom subsquare rows already contain symbols 0,...,3, so
			# their first-column entries lie in 4,...,9.  Latinness and sorting
			# therefore force the first four top entries to be 0,1,2,3.
			for i in range(4):
				generate_clause({L[i][0][i]})
			if lfirstpair_case is not None:
				generate_clause({L[4][0][lfirstpair_case[0]]})
				generate_clause({L[5][0][lfirstpair_case[1]]})
	if l01_case is not None:
		generate_clause({L[0][1][l01_case]})

# Generate constraints encoding that every row of the square A has colours matching the list of transversal types in M
def colour_constraints(M, A):
	for i in range(n):
		# Row i is of form p_i, so ensure there are M[i] white entries in the last four columns of row i
		generate_adder_clauses([A[i][j][WHITE] for j in range(6,n)], M[i], M[i])
		# Row i is of form p_i, so ensure there are 2*M[i]-2 dark entries in the first six columns of row i
		generate_adder_clauses([A[i][j][DARK] for j in range(6)], 2*M[i]-2, 2*M[i]-2)

colour_constraints(transversal_types[P_type], Pc)
colour_constraints(transversal_types[Q_type], Qc)

# In type (U,U), the dark cells induce a simple bipartite graph between
# P-rows and Q-rows.  Its nonzero degrees on each side are (2,2,4,4),
# so the graph is forced: every degree-4 vertex meets all four vertices,
# and each degree-2 vertex meets the two degree-4 vertices.  Z names the
# unique intersection cell of each P/Q row pair, allowing this global
# consequence to be exposed directly to the solver.
if use_distinguished_subsquare and P_type == 'U' and Q_type == 'U':
	dark_edges = {(prow, qrow) for prow in range(6, n) for qrow in range(6, n)
				  if prow >= 8 or qrow >= 8}
	for prow in range(n):
		for qrow in range(n):
			forced_dark = (prow, qrow) in dark_edges
			if forced_dark:
				generate_clause([Z[qrow][j][prow] for j in range(6)])
				for j in range(6):
					generate_implication_clause({Z[qrow][j][prow]}, {Pc[prow][j][DARK]})
			else:
				for j in range(6):
					generate_clause({-Z[qrow][j][prow], -Pc[prow][j][DARK]})
	if darkcol0_case is not None or whitegraph_case is not None:
		darkcol0_representatives = [
			{(6, 8), (7, 9)}, # low-high + low-high
			{(6, 8), (8, 6)}, # low-high + high-low
			{(6, 8), (8, 9)}, # low-high + high-high
			{(8, 6), (9, 7)}, # high-low + high-low
			{(8, 6), (9, 8)}, # high-low + high-high
			{(8, 8), (9, 9)}, # high-high + high-high
		]
		if whitegraph_case is None:
			chosen = darkcol0_representatives[darkcol0_case]
		else:
			# Joint representatives for the column-0 dark matching and the
			# white-neighbour bit of P-row 0.  These nine cases are the exact
			# orbits under the four low/high row swaps.
			joint_representatives = [
				({(6, 8), (7, 9)}, 0),
				({(6, 8), (8, 6)}, 0),
				({(6, 8), (8, 6)}, 1),
				({(6, 8), (8, 9)}, 0),
				({(6, 8), (8, 9)}, 1),
				({(8, 6), (9, 7)}, 0),
				({(8, 6), (9, 8)}, 0),
				({(8, 6), (9, 8)}, 1),
				({(8, 8), (9, 9)}, 0),
			]
			chosen, whitegraph_bit = joint_representatives[whitegraph_case]
		for prow, qrow in dark_edges:
			generate_clause({Z[qrow][0][prow] if (prow, qrow) in chosen else -Z[qrow][0][prow]})

# Two darks per column in P
for j in range(6):
	generate_adder_clauses([Pc[i][j][DARK] for i in range(n)], 2, 2)

# Two darks per column in Q
for j in range(6):
	generate_adder_clauses([Qc[i][j][DARK] for i in range(n)], 2, 2)

# Set all extraneous variables to false
for i in range(n):
	for j in range(n):
		for k in range(n):
			if not k in {WHITE, DARK}:
				generate_clause({-Pc[i][j][k]})
				generate_clause({-Qc[i][j][k]})
	for j in range(6, n):
		generate_clause({-Pc[i][j][DARK]})
		generate_clause({-Qc[i][j][DARK]})
	for j in range(6):
		generate_clause({-Pc[i][j][WHITE]})
		generate_clause({-Qc[i][j][WHITE]})

# Symbol to colour correspondence:

for i in range(n):
	for j in range(6, n):
		for k in range(4):
			generate_implication_clause({P[i][j][k]}, {Pc[i][j][WHITE]})

for i in range(n):
	for j in range(6, n):
		for k in range(4):
			generate_implication_clause({Q[i][j][k]}, {Qc[i][j][WHITE]})

# Colour to symbol correspondence:

for i in range(n):
	for j in range(6, n):
		generate_implication_clause({Pc[i][j][WHITE]}, {P[i][j][0], P[i][j][1], P[i][j][2], P[i][j][3]})
	for j in range(6):
		generate_implication_clause({Pc[i][j][DARK]}, {P[i][j][4], P[i][j][5], P[i][j][6], P[i][j][7], P[i][j][8], P[i][j][9]})

for i in range(n):
	for j in range(6, n):
		generate_implication_clause({Qc[i][j][WHITE]}, {Q[i][j][0], Q[i][j][1], Q[i][j][2], Q[i][j][3]})
	for j in range(6):
		generate_implication_clause({Qc[i][j][DARK]}, {Q[i][j][4], Q[i][j][5], Q[i][j][6], Q[i][j][7], Q[i][j][8], Q[i][j][9]})

# Directly expose colour coherence at the unique P/Q row intersection.
# This follows from Q=PZ and the symbol-to-colour constraints, but avoiding
# the ten-way symbol detour materially strengthens propagation.
for prow in range(n):
	for qrow in range(n):
		for j in range(6):
			generate_implication_clause({Z[qrow][j][prow], Pc[prow][j][DARK]}, {Qc[qrow][j][DARK]})
			generate_implication_clause({Z[qrow][j][prow], Qc[qrow][j][DARK]}, {Pc[prow][j][DARK]})
		for j in range(6, n):
			generate_implication_clause({Z[qrow][j][prow], Pc[prow][j][WHITE]}, {Qc[qrow][j][WHITE]})
			generate_implication_clause({Z[qrow][j][prow], Qc[qrow][j][WHITE]}, {Pc[prow][j][WHITE]})

# In distinguished type (U,U), the white-intersection graph is forced up to
# two complementary 3+3 partitions.  It is edge-disjoint from the forced
# dark graph.  The two high P rows must use all six degree-one Q rows, and
# the two high Q rows must use all six degree-one P rows; the remaining four
# white edges are exactly K_2,2 on the two degree-two rows on each side.
# A -whitegraph-k representative also spends the corresponding top-row
# permutations to fix both 3+3 partitions.
if whitegraph_case is not None:
	white_edges = {(8, qrow) for qrow in range(3)}
	white_edges |= {(9, qrow) for qrow in range(3, 6)}
	white_edges |= {(prow, qrow) for prow in [6, 7] for qrow in [6, 7]}
	if whitegraph_bit == 0:
		white_edges |= {(prow, 8) for prow in [0, 1, 2]}
		white_edges |= {(prow, 9) for prow in [3, 4, 5]}
	else:
		white_edges |= {(prow, 8) for prow in [1, 2, 3]}
		white_edges |= {(prow, 9) for prow in [0, 4, 5]}
	for prow in range(n):
		for qrow in range(n):
			if (prow, qrow) in white_edges:
				generate_clause([Z[qrow][j][prow] for j in range(6, n)])
				for j in range(6, n):
					generate_implication_clause({Z[qrow][j][prow]}, {Pc[prow][j][WHITE]})
			else:
				for j in range(6, n):
					generate_clause({-Z[qrow][j][prow], -Pc[prow][j][WHITE]})

# Fixing symbols in the first row of P (symmetry breaking).  This normal
# form uses arbitrary permutations of the first six columns, so it is not
# imposed when those permutations instead canonicalize Sigma's support.
# First row is one of
# * [0, 1, 2, 4, 5, 6, 3, 7, 8, 9]
# * [0, 1, 3, 4, 5, 6, 2, 7, 8, 9]
# * [0, 2, 3, 4, 5, 6, 1, 7, 8, 9]
if sigma_case is None:
	for cl in [P[0][0][0], P[0][3][4], P[0][4][5], P[0][5][6], P[0][7][7], P[0][8][8], P[0][9][9]]:
		generate_clause([cl])
	generate_implication_clause({P[0][6][3]}, {P[0][1][1]})
	generate_implication_clause({P[0][6][3]}, {P[0][2][2]})
	generate_implication_clause({P[0][6][2]}, {P[0][1][1]})
	generate_implication_clause({P[0][6][2]}, {P[0][2][3]})
	generate_implication_clause({P[0][6][1]}, {P[0][1][2]})
	generate_implication_clause({P[0][6][1]}, {P[0][2][3]})
	generate_implication_clause({P[0][1][2]}, {P[0][2][3]})
	generate_implication_clause({P[0][1][2]}, {P[0][6][1]})
	generate_implication_clause({P[0][2][2]}, {P[0][1][1]})
	generate_implication_clause({P[0][2][2]}, {P[0][6][3]})
	if p0_case is not None:
		generate_clause({P[0][6][p0_case]})
else:
	# Canonicalizing Sigma does not consume permutations of symbols 4,...,9.
	# Use that full S_6 action by ordering their positions in the first row
	# of P.  This is independent of the row/column support labels.
	for k in range(4, n-1):
		for j in range(n):
			for jp in range(j+1):
				generate_clause({-P[0][j][k], -P[0][jp][k+1]})
	# In the (U,U) case, exchanging P and Q preserves every constraint.
	# Retain the half with the first entry of P no larger than that of Q.
	if P_type == Q_type:
		for k in range(n):
			for l in range(k):
				generate_clause({-P[0][0][k], -Q[0][0][l]})

# Ensure consistency of the dark entries in P and Q
for i in range(n):
	for j in range(6):
		for l in range(n):
			for k in range(n):
				generate_implication_clause({Qc[i][j][DARK], Q[i][j][k], P[l][j][k]}, {Pc[l][j][DARK]})
				generate_implication_clause({Pc[l][j][DARK], Q[i][j][k], P[l][j][k]}, {Qc[i][j][DARK]})

# Latin square constraints for P and Q
for i in range(n):
	for j in range(n):
		generate_exactly_one_clauses([P[i][j][k] for k in range(n)])
		generate_exactly_one_clauses([Q[i][j][k] for k in range(n)])
		generate_exactly_one_clauses([P[i][k][j] for k in range(n)])
		generate_exactly_one_clauses([Q[i][k][j] for k in range(n)])
		generate_exactly_one_clauses([P[k][j][i] for k in range(n)])
		generate_exactly_one_clauses([Q[k][j][i] for k in range(n)])

# Order rows of P and Q of the same type lexicographically

# Generate symbol ordering constraints within a block of the same colour
# K is the list of transversal types for the square H
def lex_order(K, H, square_name):
	for i in range(n-1):
		if K[i] == K[i+1]:
			# The active type-U row swaps canonicalize the column-0 dark
			# matching when that orbit split is selected.
			if (darkcol0_case is not None or whitegraph_case is not None) and i in [6, 8]:
				continue
			# A joint white-graph representative uses these top-row actions to
			# fix two 3+3 partitions.  Keep lex order inside each part, using
			# the stabilizer of the fixed partition.
			if whitegraph_case is not None:
				if square_name == 'Q' and i == 2:
					continue
				if square_name == 'P':
					if whitegraph_bit == 0 and i == 2:
						continue
					if whitegraph_bit == 1 and i == 3:
						continue
					if fixedstar_case is not None:
						if whitegraph_bit == 0 and i == 1:
							continue
						if whitegraph_bit == 1 and i == 4:
							continue
			for k in range(n):
				for l in range(k):
					generate_implication_clause({H[i][0][k]}, {-H[i+1][0][l]})

lex_order(transversal_types[P_type], P, 'P')
lex_order(transversal_types[Q_type], Q, 'Q')

# Constraints that the squares in the TRP are consistent with one of the following 4x4 Latin subsquares in the bottom-right of the third square L:
# Omega_1 (The Cayley table of Z_4)
# [ 0 1 2 3 ]
# [ 1 2 3 0 ]
# [ 2 3 0 1 ]
# [ 3 0 1 2 ]
# Omega_2 (The Cayley table of Z_2 x Z_2)
# [ 0 1 2 3 ]
# [ 1 0 3 2 ]
# [ 2 3 0 1 ]
# [ 3 2 1 0 ]
Ls = [[[0,1,2,3],[1,2,3,0],[2,3,0,1],[3,0,1,2]],
      [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]]
# Two new variables omega[0] and omega[1] to encode which order 4 subsquare appears in L
omega = [total_vars+1, total_vars+2]
total_vars += 2
for subsqtype in range(2):
	Omega = Ls[subsqtype]
	for i in range(n):
		for j in range(6,n):
			for jp in range(j+1,n):
				for l in range(4):
					k = Omega[l][j-6]
					kp = Omega[l][jp-6]
					# The omega variable can be removed from the antecedent if the (l,j-6) and (l,jp-6) entries in both order 4 subsquares are the same
					if Ls[0][l][j-6] == Ls[1][l][j-6] and Ls[0][l][jp-6] == Ls[1][l][jp-6]:
						generate_implication_clause({P[i][j][k]}, {-P[i][jp][kp]})
						generate_implication_clause({Q[i][j][k]}, {-Q[i][jp][kp]})
					else:
						generate_implication_clause({omega[subsqtype], P[i][j][k]}, {-P[i][jp][kp]})
						generate_implication_clause({omega[subsqtype], Q[i][j][k]}, {-Q[i][jp][kp]})
# (P,Q) must be compatible with the 4x4 subsquare Omega_1 or Omega_2
generate_clause({omega[0], omega[1]})
# If -z4 option enabled, (P,Q) must be compatible with Omega_1
if use_z4:
	generate_clause({omega[0]})
# If -z2xz2 option enabled, (P,Q) must be compatible with Omega_2
if use_z2xz2:
	generate_clause({omega[1]})

if use_distinguished_subsquare:
	# Make L the actual distinguished Latin square, rather than an arbitrary
	# mutual-TRP extension.  Its bottom-right block is Omega, and the colour
	# of a P/Q entry records whether the corresponding cell of L lies in a
	# bottom (subsquare) row.  PE and QE name that row exactly.
	for subsqtype in range(2):
		for i in range(4):
			for j in range(4):
				generate_implication_clause({omega[subsqtype]}, {L[i+6][j+6][Ls[subsqtype][i][j]]})
	if fixedstar_case is not None:
		# P-row 0 has its unique white cell at column 6.  Its source-row
		# coordinate is the small symbol selected by the p0 case.  In the
		# fixed white graph this edge belongs to a degree-three star centred
		# at Q-row 8 or 9.  The other two cells form one of six partial
		# transversals through the anchored cell of the selected Omega.
		fixedstar_pairs = []
		for subsqtype in range(2):
			def attributes(cell):
				column, lrow = cell
				return column, lrow, Ls[subsqtype][lrow][column]
			def compatible(first, second):
				return all(a != b for a, b in zip(attributes(first), attributes(second)))
			anchor = (0, p0_case)
			candidates = [
				(column, lrow) for column in range(4) for lrow in range(4)
				if (column, lrow) != anchor and compatible(anchor, (column, lrow))
			]
			pairs = []
			for first_index in range(len(candidates)):
				for second_index in range(first_index + 1, len(candidates)):
					first = candidates[first_index]
					second = candidates[second_index]
					if compatible(first, second):
						pairs.append((first, second))
			assert len(pairs) == 6
			fixedstar_pairs.append(pairs)
		qrow = 8 if whitegraph_bit == 0 else 9
		prows = [1, 2] if whitegraph_bit == 0 else [4, 5]
		for subsqtype in range(2):
			for prow, (column, lrow) in zip(prows, fixedstar_pairs[subsqtype][fixedstar_case]):
				j = column + 6
				ell = lrow + 6
				generate_implication_clause({omega[subsqtype]}, {Z[qrow][j][prow]})
				generate_implication_clause({omega[subsqtype]}, {PE[prow][ell][j]})
				generate_implication_clause({omega[subsqtype]}, {QE[qrow][ell][j]})
	if sigma_case is not None:
		if sigma_case == "12":
			edges = {(i, i) for i in range(6)} | {(i, (i+1) % 6) for i in range(6)}
		elif sigma_case == "8+4":
			edges = {(i, j) for i in range(2) for j in range(2)}
			edges |= {(i, i) for i in range(2, 6)} | {(i, 2+(i-1) % 4) for i in range(2, 6)}
		elif sigma_case == "6+6":
			edges = set()
			for base in [0, 3]:
				edges |= {(base+i, base+i) for i in range(3)}
				edges |= {(base+i, base+(i+1) % 3) for i in range(3)}
		else:
			edges = set()
			for base in [0, 2, 4]:
				edges |= {(i, j) for i in range(base, base+2) for j in range(base, base+2)}
		for i in range(6):
			for j in range(6):
				symbols = range(4, n) if (i, j) in edges else range(4)
				generate_clause({L[i][j][k] for k in symbols})
	for A, E, Ac in [(P, PE, Pc), (Q, QE, Qc)]:
		for i in range(n):
			for j in range(6):
				# Dark cells are precisely symbols 4,...,9 occurring in the
				# top-left 6-by-6 block Sigma of the distinguished square.
				generate_implication_clause({Ac[i][j][DARK]}, {E[i][ell][j] for ell in range(6)})
				for ell in range(6):
					for k in range(4, n):
						generate_implication_clause({E[i][ell][j], A[i][j][k]}, {Ac[i][j][DARK]})
				for ell in range(6, n):
					generate_implication_clause({E[i][ell][j]}, {-Ac[i][j][DARK]})
					generate_implication_clause({E[i][ell][j]}, {A[i][j][k] for k in range(4, n)})
			for j in range(6, n):
				# The white cells in the last four columns are exactly the
				# fixed subsquare cells, i.e. those on its bottom four rows.
				generate_implication_clause({Ac[i][j][WHITE]}, {E[i][ell][j] for ell in range(6, n)})
				for ell in range(6, n):
					generate_implication_clause({E[i][ell][j]}, {Ac[i][j][WHITE]})
				for ell in range(6):
					generate_implication_clause({E[i][ell][j]}, {-Ac[i][j][WHITE]})
					generate_implication_clause({E[i][ell][j]}, {A[i][j][k] for k in range(4, n)})

# Output SAT instance in DIMACS format
print("p cnf {} {}".format(total_vars, len(clauses)))
for clause in clauses:
	print(clause)
