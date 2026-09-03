# The distance-three slice for two fixed points in `Av(123)`

Let

\[
f^{(2)}_{n,d}(123)
=\#\{\pi\in S_n:\pi\text{ avoids }123,\ \operatorname{Fix}(\pi)=\{a,a+d\}
\text{ for some }a\}.
\]

A 123-avoider has at most two fixed points, so requiring the two displayed
fixed points already makes them the complete fixed-point set.

## Theorem

For every integer \(m\geq3\), with
\(C_j=\binom{2j}{j}/(j+1)\),

\[
\boxed{
f^{(2)}_{2m,3}(123)
=6(C_{m-1}-C_{m-2})^2
+2C_{m-2}(C_m-3C_{m-1}+C_{m-2})
}
\]

and

\[
\boxed{
f^{(2)}_{2m+1,3}(123)
=8C_{m-1}(C_m-2C_{m-1}).
}
\]

Equivalently,

\[
f^{(2)}_{2m,3}(123)
=\frac{4(m-2)(16m^2-21m-27)}{m^2(m+1)}C_{m-2}^2
\]

and

\[
f^{(2)}_{2m+1,3}(123)
=\frac{16(m-2)}{m+1}C_{m-1}^2.
\]

These are exactly the specializations at \(d=3\) of Conjecture A.2 in
Birmajer, Gil, Tirrell, and Weiner,
[*Pattern-avoiding stabilized-interval-free permutations*](https://arxiv.org/abs/2306.03155).
The source proves the two extreme-distance cases; this result proves the
next fixed-distance slice after the previously established \(d=2\) case.

## Catalan hooks

For nonnegative \(j,x,y\), let \(H_{j,x,y}\) count the permutations
\(\sigma\in\operatorname{Av}_{j+x+y}(123)\) satisfying both conditions:

1. the values \(1,\ldots,x\) occur among the first \(j+x\) positions and
   occur there in decreasing order;
2. the last \(y\) entries are greater than \(x\) and decreasing.

Only \(0\leq x,y\leq2\) are needed. Direct Catalan deletions give

\[
\begin{array}{c|ccc}
H_{j,x,y}&y=0&y=1&y=2\\ \hline
x=0&C_j&C_{j+1}&C_{j+2}-C_{j+1}\\
x=1&C_{j+1}&C_{j+2}-C_{j+1}&C_{j+3}-2C_{j+2}\\
x=2&C_{j+2}-C_{j+1}&C_{j+3}-2C_{j+2}&
C_{j+4}-3C_{j+3}+C_{j+2}.
\end{array}
\tag{1}
\]

Here are complete details of the nontrivial entries. Put \(N=j+x+y\).

- For \(H_{j,2,0}\), the excluded avoiders have 1 before 2. Then 2 must
  be final, or 1, 2, and the next entry would be a 123. Deleting the final
  2 gives an arbitrary member of \(\operatorname{Av}_{N-1}(123)\).
  The same terminal deletion, or its reflected version, gives
  \(H_{j,0,2}=H_{j,1,1}=C_N-C_{N-1}\).
- For \(H_{j,2,1}\), a final value greater than 2 forces 2 to precede 1.
  Ending in 1 and ending in 2 each describe a Catalan class of size
  \(C_{N-1}\). Hence \(H_{j,2,1}=C_N-2C_{N-1}\). The terminal-descent
  version gives the same formula for \(H_{j,1,2}\).
- For \(H_{j,2,2}\), it is enough to require a final descent whose entries
  are both greater than 2; these conditions force 2 to precede 1. There are
  \(C_N-C_{N-1}\) avoiders with a final descent. Among them, those whose
  last two entries contain 1 number \(C_{N-1}\). Those containing 2 but
  not 1 number \(C_{N-1}-C_{N-2}\): start with all avoiders ending in 2
  and remove those ending in the ascending pair 1,2. This proves the
  bottom-right entry of (1).

All deletion maps used here are reversible. Inserting a terminal 1 or 2,
or inserting 1 immediately before a terminal entry, cannot create a new
123 for the same extremal-value reason.

## Fixed-point grid decomposition

Fix two fixed points \(a<b=a+d\), using one-based positions and values.
Split both axes into the intervals before \(a\), strictly between \(a,b\),
and after \(b\).

Three grid cells are empty in every 123-avoider:

- no position before \(a\) has value below \(a\), because that entry
  followed by the two fixed points would be a 123;
- no position after \(b\) has value above \(b\), by the dual argument;
- no middle position has a middle value, because it would lie in a 123
  between the two fixed points.

Each of the four remaining off-diagonal middle strips is decreasing. Two
increasing entries in such a strip, together with the appropriate fixed
point, would form a 123.

Let \(x\) be the number of middle values placed before \(a\), and let \(y\)
be the number of middle positions carrying values above \(b\). Let \(j\)
and \(k\) be the numbers of points in the upper-left and lower-right corner
cells. Counting rows and columns gives

\[
j=\frac{n-d-1-x-y}{2},\qquad k=n-2d-j. \tag{2}
\]

There are \(\binom{d-1}{x}\) choices for the middle values in the left
strip and \(\binom{d-1}{y}\) choices for the middle positions in the upper
strip. After standardization, the union of the upper-left corner and its
two strips is counted by \(H_{j,x,y}\). Reverse-complement shows that the
lower-right union is counted by
\(H_{k,d-1-x,d-1-y}\).

Conversely, any two such hook fillings, together with the strip choices and
the fixed points, inflate to a unique 123-avoider. A 123 wholly in either
hook is excluded by definition. Across the two hooks, positions increase
while value bands weakly decrease; the only common middle band consists of
two decreasing strips and cannot supply the first and third entries of a
cross-hook 123. The fixed-point and empty-cell observations exclude every
remaining case. Thus the exact decomposition is

\[
f^{(2)}_{n,d}(123)=
\sum_{\substack{0\leq x,y<d\\j\in\mathbb Z_{\geq0},\ k\geq0}}
\binom{d-1}{x}\binom{d-1}{y}
H_{j,x,y}H_{k,d-1-x,d-1-y}, \tag{3}
\]

where \(j,k\) are given by (2). Notice that (3) is a decomposition identity;
the present theorem evaluates only its \(d=3\) specialization.

## Evaluation at distance three

Let \(d=3\). If \(n=2m\), equation (2) requires \(x+y\) even. The five
possibilities are

\[
(0,0),(0,2),(1,1),(2,0),(2,2).
\]

The two extreme cases together contribute

\[
2C_{m-2}(C_m-3C_{m-1}+C_{m-2}),
\]

while the other three, including their binomial strip-choice factors,
contribute

\[
(1+4+1)(C_{m-1}-C_{m-2})^2.
\]

This is the first even formula.

If \(n=2m+1\), equation (2) requires \(x+y\) odd. The four possibilities
\((0,1),(1,0),(1,2),(2,1)\) give

\[
8C_{m-1}(C_m-2C_{m-1}).
\]

Finally, the Catalan ratio

\[
\frac{C_m}{C_{m-1}}=\frac{4m-2}{m+1}
\]

gives the two rational forms in the theorem. Direct substitution of \(d=3\)
in Conjecture A.2 gives the same expressions: only its \(i=1\) summand can
survive.

## Reproduction

The checker needs only CPython 3.11 or later and the standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
```

It performs four checks:

1. It compares an optimized 123 detector with the literal three-index
   definition on every permutation through length 8.
2. It exhaustively selects the required permutations directly through
   length 10.
3. Independently, it constructs the complete sets through the hook-grid
   decomposition (3) and compares them entry by entry with the direct sets.
4. It enumerates the hook classes needed by (1), compares their sizes with
   the Catalan formulas, and checks exact agreement with the specialized
   Birmajer--Gil--Tirrell--Weiner expression for \(3\leq m\leq200\).

The universal theorem rests on the written bijections; the computation is a
finite corroboration. All arithmetic and enumeration are exact. There are
no external packages, imported data, random choices, floating-point
operations, or solvers.

## Novelty scope

Targeted searches found the general distance-refined conjecture, its two
extreme slices, and the committed proof of the \(d=2\) slice, but no proof or
separate statement of the \(d=3\) formulas. The result is therefore
apparently new to the searched sources, not a historical-priority claim.
