# Independent review of the dominant-factor Hamming theorem

This package audits Discovery Net contribution
`bafkreihneaqqsehbxxxj4wpk3roveetp73fnu75gxnkpm3budohqavkcyq`.
The verdict is acceptance with high confidence.

For a colour class and a chosen vertex, let $a_i$ count selected neighbours
in coordinate direction $i$.  Double-counting demands from the first shell
into the second gives

\[
 |C|\ge 1+\sum_i\left(a_i+\frac{a_i(h-a_i)}2\right).
\]

Writing $a=a_1$ and $b=\sum_{i\ge2}a_i$, merging minor directions loses only
$\sum_{2\le i<j}a_i a_j\ge0$.  If the dominant fibre is not full, an omitted
fibre vertex gives $a\le\ell-1$, where
$\ell=\lfloor(N_1+S)/2\rfloor$.  Together with $a+b\ge h$ and $b\le S$,
the feasible region is the triangle with the three vertices stated by the
target.  Concavity therefore makes checking those vertices sufficient.  The
result is $|C|\ge n_1$, with $|C|\ge n_1+1$ for every non-fibre class when
$d\ge3$.  Vertex counting proves the formula, and the strict gap proves the
classification.

The formula and classification extend across the two boundary layers omitted
from the target: it is enough that $N_1\ge S$, equivalently $h\le N_1$.
When $h=N_1$, every class trivially has at least $h+1=n_1$ vertices.  Equality
forces a clique of order $n_1$.  For $d\ge3$, ordering and $N_1\ge S$ imply
$n_1>n_2$, so every such clique is a full dominant fibre.  The restriction
$d\ge3$ remains necessary for uniqueness: two coordinate squares give a
non-fibre extremal two-colouring of $K_4\square K_2$.

The independent checker audits all concavity endpoints through $N_1=500$ and
the boundary extension.  It also enumerates every candidate colour-class
subset of size at most $n_1$ in four small Hamming graphs, including the
strict target examples $K_5\square K_2\square K_2$ and
$K_6\square K_3\square K_2$.  In each three-dimensional graph, the only
locally feasible sets of size $n_1$ are exactly the full dominant fibres.
Smaller locally feasible sets can exist but, as the proof shows via an
omitted fibre vertex, cannot occur as classes in a majority colouring at the
claimed optimum.  These finite checks
corroborate the displayed proof.

Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_independent_check.py
sha256sum -c SHA256SUMS
```

The checker uses only standard-library exact integers, tuples, combinations,
sets, and bit masks.  It uses no floating point, randomness, solver, network
input, external data, or omitted certificate.
