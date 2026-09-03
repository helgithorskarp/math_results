# The distance-two slice for two fixed points in `Av(123)`

Let

\[
f^{(2)}_{n,d}(123)
=\#\{\pi\in S_n:\pi\text{ avoids }123,\ \operatorname{Fix}(\pi)=\{a,a+d\}
\text{ for some }a\}.
\]

Since a 123-avoiding permutation has at most two fixed points, it is enough in
this definition to require that the displayed two points are fixed.

## Theorem

For every integer \(m\geq 2\),

\[
\boxed{f^{(2)}_{2m,2}(123)=2C_{m-1}^2}
\]

and

\[
\boxed{
f^{(2)}_{2m+1,2}(123)
=2C_{m-1}(C_m-C_{m-1})
=\frac{6(m-1)}{m+1}C_{m-1}^2,
}
\]

where \(C_j=\frac1{j+1}\binom{2j}{j}\) is the \(j\)-th Catalan number.

This proves the full \(d=2\) slice of Conjecture A.2 in Birmajer, Gil,
Tirrell, and Weiner, [*Pattern-avoiding stabilized-interval-free
permutations*](https://arxiv.org/abs/2306.03155). The conjecture gives a
formula for every \(1\leq d\leq\lfloor n/2\rfloor\); its paper proves the
extreme slices \(d=1\) and \(d=\lfloor n/2\rfloor\), but not the fixed
distance-two slice. Elizalde's earlier formula for the total number with two
fixed points is in [*Multiple pattern avoidance with respect to fixed points
and excedances*](https://arxiv.org/abs/math/0311211), Theorem 3.3.

## Proof

Use one-based positions and values. Suppose that \(a<b=a+2\) are fixed
points of a 123-avoiding permutation \(\pi\). A position before \(a\) cannot
carry a value below \(a\), since that entry followed by the two fixed points
would form a 123. Thus the first \(a-1\) positions must use values above
\(a\), excluding the already used value \(b\), and

\[
a-1\leq n-a-1,\qquad a\leq \lfloor n/2\rfloor.
\]

Similarly, a position after \(b\) cannot carry a value above \(b\). There are
only \(b-2\) available values below \(b\), after excluding the fixed value
\(a\), so

\[
n-b\leq b-2,\qquad b\geq \left\lceil\frac{n+2}{2}\right\rceil.
\]

### Even size

Let \(n=2m\). The bounds force

\[
(a,b)=(m-1,m+1)\quad\text{or}\quad(m,m+2).
\]

First take \((a,b)=(m-1,m+1)\). None of the \(m-1\) values
\(m+2,\ldots,2m\) can occur after position \(b\). Consequently they occupy
exactly the positions

\[
1,\ldots,m-2,m.
\]

The remaining nonfixed positions \(m+2,\ldots,2m\) contain exactly the
values

\[
1,\ldots,m-2,m.
\]

Standardizing the entries in each of these two position sets gives an
ordered pair \((\alpha,\beta)\in\operatorname{Av}_{m-1}(123)^2\).
Conversely, inflate the two displayed position/value sets by any such pair
and insert the fixed points \((m-1,m-1)\) and \((m+1,m+1)\). This produces a
123-avoider. Indeed, a 123 wholly inside either inflated block is excluded;
every entry of the first block is larger than both fixed values and every
entry of the last block, while the order of the two fixed entries and the
single intervening first-block entry cannot form an increasing triple with
another block.

This is a bijection, so this fixed-point-location case has \(C_{m-1}^2\)
members. Reverse-complement,

\[
\pi^{rc}(i)=2m+1-\pi(2m+1-i),
\]

preserves 123-avoidance and bijects this case with
\((a,b)=(m,m+2)\). The two cases are disjoint, proving
\(f^{(2)}_{2m,2}(123)=2C_{m-1}^2\).

### Odd size

Let \(n=2m+1\). The same bounds force \((a,b)=(m,m+2)\). Put
\(c=m+1\). The entry \(\pi(c)\) is not \(c\), because three fixed points
would themselves form a 123. It is therefore either below \(a\) or above
\(b\).

Suppose first that \(\pi(c)>b\). All values below \(a\) occur after \(b\),
and the positions

\[
1,\ldots,m-1,c
\]

contain exactly the values

\[
c,m+3,\ldots,2m+1.
\]

Their standardization is an \(\alpha\in\operatorname{Av}_m(123)\) whose
last entry is not its minimum. The positions \(m+3,\ldots,2m+1\), containing
the values \(1,\ldots,m-1\), standardize independently to a
\(\beta\in\operatorname{Av}_{m-1}(123)\). As in the even case, the value
bands and the two fixed entries show that inflating any such pair produces
a 123-avoider, and the construction is inverse to standardization.

There are \(C_m-C_{m-1}\) choices for \(\alpha\): among the \(C_m\)
123-avoiders of length \(m\), precisely \(C_{m-1}\) end in their minimum,
by deleting that terminal minimum and standardizing. There are \(C_{m-1}\)
choices for \(\beta\). Reverse-complement preserves the fixed pair and
bijections the case \(\pi(c)>b\) with \(\pi(c)<a\). Hence

\[
f^{(2)}_{2m+1,2}(123)=2C_{m-1}(C_m-C_{m-1}).
\]

Finally,

\[
\frac{C_m}{C_{m-1}}=\frac{4m-2}{m+1}
\]

gives the second displayed form.

For comparison with Conjecture A.2, substituting \(d=2\) into its formula
also gives these expressions directly. In even size its summation vanishes
and its separate term simplifies to \(2C_{m-1}^2\). In odd size only the
summand indexed by \(i=1\) survives, simplifying to
\(6(m-1)C_{m-1}^2/(m+1)\).

## Reproduction

The checker requires only CPython 3.11 or later and the standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
```

It performs three distinct checks:

1. It compares the optimized 123 predicate with the literal three-index
   definition on every permutation through length 8.
2. It enumerates all permutations directly through length 10 and selects
   those with exactly two fixed points at distance 2.
3. Independently, it implements the two Catalan-block bijections above and
   compares the complete sets of permutations, not merely their sizes.

The exact expected output is

```text
n= 4 count=   2 sha256=5f223db34735d5a5d66138f3ea628bc597abb57a54053901403984269125a1b3
n= 5 count=   2 sha256=c1de55234b1e9b93e9a354e6fd2bf533cafd4f280570d630da77f7872753f1b4
n= 6 count=   8 sha256=5ad97b248272f49ac76bd8f02dbe73a9a84488dde91229b919278017c61119f4
n= 7 count=  12 sha256=36070b925f0fbc6c62621986c9ae7186ac3a8d609d1484744c5d995ce0f837f4
n= 8 count=  50 sha256=c65b9af5e716fa69bccc1a47bed75a0ef9bd90012db736275aeff5ed708710ce
n= 9 count=  90 sha256=a335f7bee4bd5cea9e3628cee4209388758a506944a9a3b992d460bcd52dcf5f
n=10 count= 392 sha256=ea9ae3dd57301bda5f74e959c724b56f8b865ec3ef6123adadfc9fa2f45d033e
```

This was tested with CPython 3.11.2. All computations use exact Python
integers and tuples. There are no external packages, random choices,
floating-point operations, solvers, or imported data. The finite computation
corroborates the bijection; the universal theorem rests on the written proof.

## Novelty scope

Targeted searches found the general conjecture and the two extreme slices in
the cited paper, but no proof or separate statement of the \(d=2\) formula.
The claim here is therefore *apparently new to the searched sources*, not a
historical priority claim.
