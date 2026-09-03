# Majority C-chromatic number of three-dimensional Hamming graphs

## Result

Let $H(3,n)=K_n\square K_n\square K_n$, and let

\[
s=\left\lceil\frac{n+1}{2}\right\rceil.
\]

A majority C-coloring is a vertex coloring in which every vertex has at
least half of its neighbors in its own color class.  Its maximum possible
number of nonempty color classes is denoted by

\[
\overline\chi_{\geqslant}(G).
\]

For every integer $n\geq2$,

\[
\boxed{
\overline\chi_{\geqslant}(H(3,n))
=\left\lfloor\frac{n^2}{s}\right\rfloor.}
\]

Equivalently, the value is $2n-2$ for odd $n\geq3$, is $2n-4$ for
even $n\geq8$, and the three remaining values are $2,5,9$ for
$n=2,4,6$, respectively.

This resolves the three-dimensional balanced case of the open problem posed
in Bujtás--Dettlaff--Furmańczyk--Laskowska, [*Majority C-coloring in
Cartesian products*](https://arxiv.org/abs/2608.27669), arXiv:2608.27669
(2026).  The result is apparently new relative to that paper and targeted
searches performed on 2026-09-03; this is not a priority claim.

## Upper bound: every color class has at least $ns$ vertices

Put $N=n-1$,

\[
r=\left\lceil\frac N2\right\rceil,
\qquad h=N+r=\left\lceil\frac{3N}{2}\right\rceil,
\qquad s=r+1.
\]

Every vertex of $H(3,n)$ has degree $3N$, so every vertex has at least
$h$ same-color neighbors.

Fix a nonempty color class $C$ and a vertex $v\in C$.  For
$i\in\{1,2,3\}$, let $a_i$ be the number of same-color neighbors of
$v$ obtained by changing coordinate $i$, and put
$A=a_1+a_2+a_3$.  Then

\[
0\leq a_i\leq N,\qquad A\geq h.
\]

Let $B\subseteq C$ be the vertices at Hamming distance two from $v$.
A vertex counted by $a_i$ has exactly $a_i$ possible same-color
neighbors among $v$ and the distance-one shell: $v$ itself and the
other $a_i-1$ selected vertices on the same coordinate line.  It must
therefore have at least $h-a_i$ neighbors in $B$.  Every vertex of
$B$ has only two neighbors in the distance-one shell.  Double-counting
the edges between the two shells gives

\[
2|B|\geq\sum_{i=1}^3 a_i(h-a_i).
\]

Consequently,

\[
|C|\geq
1+A+\frac12\sum_{i=1}^3a_i(h-a_i). \tag{1}
\]

It remains to minimize the right side.  For fixed $A$, the sum
$\sum_i a_i^2$ is maximized by concentrating mass into coordinates up to
the cap $N$.

If $A=N+t$ with $r\leq t\leq N$, then

\[
\sum_i a_i^2\leq N^2+t^2,
\]

and the right side of (1), minus $(N+1)(r+1)$, is at least

\[
(t-r)\left(1+\frac{N-t}{2}\right)\geq0.
\]

If $A=2N+t$ with $0\leq t\leq N$, then

\[
\sum_i a_i^2\leq2N^2+t^2,
\]

and the same difference is at least

\[
N-r+t\left(1+\frac{N+r-t}{2}\right)\geq0.
\]

These cases exhaust $h\leq A\leq3N$.  Thus

\[
|C|\geq(N+1)(r+1)=ns.
\]

If a coloring has $q$ nonempty classes, their sizes sum to $n^3$, so

\[
q\leq\left\lfloor\frac{n^3}{ns}\right\rfloor
=\left\lfloor\frac{n^2}{s}\right\rfloor. \tag{2}
\]

## Construction attaining the bound

Work in the cyclic group $\mathbb Z_n$.  For every $i\in\mathbb Z_n$,
let

\[
R_i=\{i,i+1,\ldots,i+s-1\}\pmod n.
\]

We first partition the $n\times n$ grid $\mathbb Z_n^2$.  Choose a set
$I$ of active row indices.  For each $i\in I$, make the row class

\[
P_i=\{(i,j):j\in R_i\}.
\]

For each column $j$, put every grid point not already used into

\[
Q_j=\{(i,j):i\notin I\text{ or }j\notin R_i\}.
\]

The sets $P_i$ and $Q_j$ partition $\mathbb Z_n^2$.  Use the
following active rows.

* If $n=2m+1$ is odd, take
  $I=\mathbb Z_n\setminus\{0,m+1\}$.
* If $n=2$, take $I=\varnothing$.
* If $n=4$, take $I=\{0\}$.
* If $n=6$, take $I=\{0,2,4\}$.
* If $n=2m\geq8$, take
  $I=\mathbb Z_n\setminus\{0,1,m,m+1\}$.

Each $P_i$ has size $s$.  Each $Q_j$ also has size at least $s$:

* in the odd case, the two omitted cyclic intervals $R_0$ and
  $R_{m+1}$ cover every column, so at most $s-1=m=n-s$ active intervals
  contain any column;
* for even $n\geq8$, each column is covered by at least two of the four
  omitted intervals, because both pairs $(R_0,R_m)$ and
  $(R_1,R_{m+1})$ cover all columns; hence at most
  $s-2=m-1=n-s$ active intervals contain a column;
* the assertions for $n=2,4,6$ follow directly (for $n=6$, every column
  lies in exactly two of $R_0,R_2,R_4$).

Lift every grid class $D\in\{P_i:i\in I\}\cup\{Q_j:j\in\mathbb Z_n\}$
to the color class

\[
\mathbb Z_n\times D\subseteq\mathbb Z_n^3.
\]

Since $D$ lies in one row or one column, it is a clique in
$K_n\square K_n$.  A vertex in the lifted class has $n-1$ same-color
neighbors from its first coordinate and $|D|-1\geq s-1=r$ from $D$.
It therefore has at least $N+r=h$ same-color neighbors, as required.

The number of classes is $|I|+n$: it is $2n-2$ for odd $n$, $2n-4$
for even $n\geq8$, and $2,5,9$ for $n=2,4,6$.  Direct division shows
that these values equal the right side of (2), proving the formula.

## Reproduction and checks

The theorem above is a human proof; no computation is part of its trust
boundary.  The pure-Python checker independently constructs the classes,
checks the partition and the majority condition from the definition, checks
the class count against the closed formula, and exhaustively checks the
three-variable shell inequality for every $2\leq n\leq60$.

```bash
python3 verify.py --max-n 60
python3 -m unittest -v test_verify.py
```

Expected final output:

```text
VERIFIED n=2..60; constructions=59; shell_triples=1687949; max_vertices=216000
```

`exploratory_sat.py` preserves the exact SAT model used before the structural
proof was found.  It is not needed for the theorem.  With
`python-sat==1.8.dev24`, for example:

```bash
python3 exploratory_sat.py coloring --n 3 --colors 5
python3 exploratory_sat.py coloring --n 3 --colors 4
python3 exploratory_sat.py minimum-class --n 5 --size 14
python3 exploratory_sat.py minimum-class --n 5 --size 15
```

The expected statuses are `UNSAT`, `SAT`, `UNSAT`, and `SAT`.  Generated CNF
instances, solver traces, and logs are intentionally not committed.

For the coloring cross-check, the encoding has one Boolean variable
$x_{v,c}$ per vertex and named color, exactly-one constraints at each
vertex, and a nonemptiness clause for each color.  The first occurrence of
color $c-1$ is required to precede the first occurrence of $c$; this
removes only permutations of color names.  If $d=3(n-1)$ and
$h=\lceil d/2\rceil$, the implication that $x_{v,c}$ forces at least
$h$ same-color neighbors is encoded, for every
$(d-h+1)$-subset $T\subseteq N(v)$, by

\[
\neg x_{v,c}\ \vee\ \bigvee_{u\in T}x_{u,c}.
\]

These clauses are equivalent to saying that at most $d-h$ neighbors of a
selected vertex may have a different color.  The minimum-class mode uses one
Boolean per vertex, fixes the origin by vertex transitivity, uses the same
conditional clauses, and adds a sequential-counter at-most-size constraint.

### Trust boundary

The mathematical claim rests on the proof above.  The checker uses only
Python integer and set operations and is a definition-level corroboration,
not a formal proof.  The optional SAT cross-check additionally trusts the
PySAT encoding and its bundled solver; no SAT verdict is used in the theorem.
