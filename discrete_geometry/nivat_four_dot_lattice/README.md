# A lattice criterion for binary four-dot periodicity

For independent integer directions \(u,v\), the binary subshift
\(\ker((1+X^u)(1+X^v))\) has the generalized Nivat property **if and only
if \(|\det(u,v)|=1\)**. Here generalized means that any finite nonempty
window \(D\) with \(P_c(D)\leq|D|\) forces a nonzero period.

For every larger determinant, an explicit pair of arithmetic lines in
different direction-lattice cosets gives a nonperiodic configuration.
For every window within that lattice, its exact complexity is
\(1+r+s-i\), where \(r,s\) count occupied rows and columns and \(i\)
counts points isolated in both. This yields sharp six-site low-complexity
and eight-site strictly low-complexity thresholds **within this
construction and window class**.

The same obstruction passes to any polynomial containing the bad
two-direction factor. In particular,
\((1+X)(1+XY^2)(1+Y)\) is square-free and its support spans the full
integer lattice, yet its subshift fails the generalized property.
The obstruction is inherited from a divisor.

The positive theorem and the separated-line mechanism come from
Kari–Moutot; this note gives their lattice-index formulation, exact witness
windows, and factor consequence. See [SOURCES.md](SOURCES.md) for
attribution and scope. This is **not a counterexample to the original
rectangular Nivat conjecture**, nor a classification of products of three
or more binomials. No exclusive historical priority is claimed.

## Files and reproduction

- [PROOF.md](PROOF.md): statements, proofs, and the finite-quotient bridge.
- [verify.py](verify.py): exact standard-library checks.
- [expected.json](expected.json): deterministic compact output.
- [SHA256SUMS](SHA256SUMS): hashes of the other five files.

Run from this directory with Python 3.11 or later, without dependencies:

    python3 verify.py > /tmp/nivat-four-dot-output.json
    diff -u expected.json /tmp/nivat-four-dot-output.json
    sha256sum -c SHA256SUMS

Verified using Python 3.11.2, including an identical run with assertions
disabled via the Python option -O. Runtime is under a second on the
development machine.

The checks cover eight direction-lattice fixtures, 96 fixture window
languages, all 511 nonempty windows in a \(3\times3\) coordinate grid,
and all 4095 nonempty incidence windows in a \(4\times3\) grid.
They find 18 six-site low windows and 39 eight-site strict windows in the
last grid, check 2304 explicit period separators and 2753 annihilator
equations, and reject three inputs violating the hypotheses.
The complete \(3\times3\) language digest is:

    0d5efd84b40899697f64f2ce9eba9d9d5358912b840b280513d0848b74c75565

Finite quotient configurations used by the checker are periodic.
Their role is to verify window languages. Infinite nonperiodicity and
the universal theorem use the written proof; the unimodular direction
also imports the published four-dot theorem. No solver, floating-point
calculation, external dataset, or omitted computational certificate is
required.
