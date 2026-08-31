# Rectangular three-torus obstruction for exact 7-step domination

## Result

Let

$$
G=C_m\mathbin{\square}C_n\mathbin{\square}C_p
=\operatorname{Cay}(\mathbb Z_m\times\mathbb Z_n\times\mathbb Z_p,
\{\pm e_1,\pm e_2,\pm e_3\}),
\qquad m,n,p\ge3.
$$

Then $G$ has no exact $7$-step dominating set of cardinality $4$ or $6$.

This is a noncyclic extension of the cyclic degree-six obstruction. It covers
every rectangular three-dimensional discrete torus with its standard six
coordinate steps, but not arbitrary generating triples of a finite abelian
group.

## Finite reduction and exact sphere formula

Let $T=\{x:d_G(0,x)=7\}$. If $S$ is an exact $7$-step dominating set,
the translates $s+T$, $s\in S$, partition the group. Hence

$$
mnp=|S||T|.
$$

A distance-seven endpoint is represented by an integer coefficient triple of
$\ell_1$-norm seven, so $|T|\le4\cdot7^2+2=198$. A four- or six-center
witness therefore has $mnp\le1188$, and its order is divisible by four or
six.

The distance enumerator of a cycle is

$$
P_q(x)=1+2\sum_{j=1}^{\lfloor(q-1)/2\rfloor}x^j
+\begin{cases}x^{q/2},&q\text{ even},\\0,&q\text{ odd}.
\end{cases}
$$

Because Cartesian-product distances add,

$$
|T|=[x^7]P_m(x)P_n(x)P_p(x).
$$

It is therefore enough to inspect the $1{,}369$ unordered triples
$3\le m\le n\le p$ with $mnp\le1188$. Of these, $1{,}089$ have order
divisible by four or six. Exact coefficient evaluation leaves no four-center
counting candidate and only three six-center candidates:

$$
(m,n,p,|T|)=(7,8,9,84),\ (8,8,9,96),\ (8,9,9,108).
$$

## Projection obstruction for the last three cases

Write the group as $\mathbb Z_m\times B$, and define the first-coordinate
fiber profile

$$
f_r=|T\cap(\{r\}\times B)|,\qquad r\in\mathbb Z_m.
$$

If $c_r$ is the number of centers having first coordinate $r$, summing the
translate partition over each fiber gives the cyclic convolution identity

$$
c*f=|B|\mathbf 1_{\mathbb Z_m}.
$$

Thus, at every nontrivial $m$-th root of unity $\zeta$,

$$
C(\zeta)F(\zeta)=0,
\quad C(x)=\sum c_rx^r,\quad F(x)=\sum f_rx^r.
$$

The exact profiles for the three candidates, projecting onto their first
coordinate, are

```text
(7,8,9):  6,10,14,15,15,14,10
(8,8,9):  6,10,14,15,12,15,14,10
(8,9,9):  8,12,16,16,12,16,16,12
```

For modulus seven, a degree-at-most-six rational polynomial vanishes at a
nontrivial seventh root exactly when it is a multiple of
$\Phi_7=1+x+\cdots+x^6$. The first profile is not constant, so its transform
is nonzero at every nontrivial seventh root.

For the two modulus-eight profiles, the exact remainders at the three
nontrivial cyclotomic factors are

```text
                         F(-1)   F mod Phi_4       F mod Phi_8
(8,8,9)                    -4    (-10,0)           (-6,-5,0,5)
(8,9,9)                    -4    (-12,0)           (-4,-4,0,4)
```

Here $\Phi_4=x^2+1$ and $\Phi_8=x^4+1$. Hence these transforms are also
nonzero at every nontrivial root. In each case the convolution identity forces
$C$ to vanish at all nontrivial characters, so the integer profile $c$
must be constant. This would require $m\mid|S|=6$, impossible for
$m=7$ or $8$. Therefore none of the three counting candidates tiles.

## Complete computation and independent check

The C++ enumerator directly scans every vertex to construct each sphere and
uses an exact difference-clique search for translate tilings. It reports

```text
radius=7
maximum_group_order=1188
dimension_triples=1369
eligible_dimension_triples=1089
four_center_counting_candidates=0
six_center_counting_candidates=3
four_center_tilings=0
six_center_tilings=0
```

The independent Python checker rescans the full dimension universe using
polynomial convolution, reconstructs the three spheres with full graph BFS,
checks the cyclotomic projection certificates, and replaces the clique search
by direct translate exact cover. It reproduces all counts and zero tilings.

The three-line candidate descriptor has SHA-256

```text
6bc9130ade1542361c6074212fd46ae3af60414e9eaac67b824378c94d187627
```

## Reproduction

Tested with GCC 12.2.0 and Python 3.11.2. Generated candidates and command
output belong under `/scratch`.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_rectangular_tori.cpp \
  -o /scratch/enumerate_rectangular_tori

/scratch/enumerate_rectangular_tori \
  /scratch/rectangular-tori-candidates.txt

python3 check_rectangular_tori.py \
  /scratch/rectangular-tori-candidates.txt

sha256sum /scratch/rectangular-tori-candidates.txt
```

Source SHA-256 values:

```text
enumerate_rectangular_tori.cpp  abc0ae6b308bfca047fc85e6b7464ad8440a32193548bd1d989ce2f0ff6937d2
check_rectangular_tori.py       a74fb76b5197dce4ad5f99a6bf348e86deee898618eefb5a7a1a8f1982a39baa
```

## Status, trust boundary, and novelty scope

This is an exact computer-assisted theorem with a short algebraic obstruction
for every surviving counting case. Its trust boundary consists of the
translate-partition and order reductions, the cycle distance polynomial, the
complete dimension-triple scan, the exact profile calculations, the
projection-convolution argument, the two implementations, and their
compiler/runtime. All operations are exact. No heuristic output, proof log,
or external solver certificate enters the claim.

Targeted searches through 2026-08-31 found the foundational exact-step papers
and work on other exact-distance conventions, but no prior unique-coverage
exact-seven obstruction for rectangular tori. The result is therefore
apparently new to the searched sources, not a claim of priority.

- P. Hersh, *On exact n-step domination*, Discrete Mathematics 205 (1999),
  235--239, <https://doi.org/10.1016/S0012-365X(99)00024-2>.
- L. K. Williams, *On Exact n-Step Domination*, Ars Combinatoria 58 (2001),
  13--22,
  <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.
- S. Das, S. Das, and A. Sadhukhan, *Exact-Distance Domination in Grid
  Graphs*, arXiv:2607.29648 (2026), <https://arxiv.org/abs/2607.29648>.
