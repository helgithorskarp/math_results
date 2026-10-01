# Every one-step endpoint-shift strip tiles the plane

Author: **six-heesch-2, researcher**, 2026-10-01. Status: complete written
author proof with exact sanity checks; unformalized and independently unreviewed.

## Statement and geometry

Use axial hexagon-center coordinates: the cell at $(x,y)$ is the regular
unit hexagon centered at $(x+y/2,\sqrt3y/2)$, with the usual scaling that
makes the six neighbor differences
$(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)$ share full edges.
Rotations, translations and reflections of the unmarked tile are allowed.

For an integer $k\ge1$, define the $(4k+3)$-cell polyhex

\[
P_k=\{(0,0),(-2k,k-1),(-2k-1,k+1)\}
\ \cup\ \bigcup_{r=0}^{k-1}
 \{-2r-1,-2r-2\}\times\{r+1,r+2\}.
\]

This is the strip $T_k$ from our earlier work with its far endpoint
$(-2k-1,k)$ replaced by $(-2k-1,k+1)$.
**Every $P_k$ tiles the plane periodically.** A specified period lattice
has six representatives of $P_k$ per fundamental domain. No minimal
period, isohedral-number or finite-Heesch claim is made.

The four-cell blocks form a chain of discs: consecutive blocks meet along
one connected three-edge boundary arc. The cell $(0,0)$ and the cell
$(-2k,k-1)$ each attach by one edge, and the shifted far cell attaches to
the last block by two consecutive edges. These attachments show that
$P_k$ is connected and has no hole. Its displayed cells are distinct,
so its area is $4k+3$.

## Six explicit copies

Put $L=12k+9=3(4k+3)$. The period lattice is

\[
\Lambda_k=\langle(2,5),(0,L)\rangle_{\mathbb Z}.
\]

Its index in $\mathbb Z^2$ is $2L=6(4k+3)$.
Define

\[
 A(x,y)=(-x-2k,\ x+y+k-2),\qquad
 B(x,y)=(x+1,\ -x-y+3),
\]

and the half-turn

\[
 \sigma(x,y)=(1-2k-x,\ -5k-1-y).
\]

The linear parts of $A$ and $B$ preserve $x^2+xy+y^2$, so these are
Euclidean isometries in the specified coordinates; $\sigma$ is a
half-turn. The six copies are

\[
 P_k,\quad A(P_k),\quad B(P_k),\quad
 \sigma(P_k),\quad\sigma A(P_k),\quad\sigma B(P_k).
\]

We prove that their cells represent every coset of $\Lambda_k$ exactly
once. Translating these six whole copies by all lattice vectors then
gives the required plane tiling, with no gaps or interior overlaps.

## Quotient calculation for all parameters

Write $x=2q+e$ with $e\in\{0,1\}$. The map

\[
 (x,y)\longmapsto (e,z),\qquad z=y-5q\pmod L
\]

is a complete coset invariant: two cells have the same image precisely
when their difference is in $\Lambda_k$. There are $2L$ images.

The following table gives the **unreduced integer** $z$ values of the
first three copies. In every family column, $r=0,\ldots,k-1$.
The endpoint values and the families are pairwise distinct within each
parity column.

| Copy | Even-$x$ endpoint values | Even-$x$ families | Odd-$x$ endpoint values | Odd-$x$ families |
|---|---|---|---|---|
| $P_k$ | $0,6k-1$ | $6r+6,6r+7$ | $6k+6$ | $6r+6,6r+7$ |
| $A(P_k)$ | $-3,6k-2$ | $6r-2,6r-1$ | $-2$ | $6r+4,6r+5$ |
| $B(P_k)$ | $6k+3$ | $6r+2,6r+3$ | $3,6k+4$ | $6r+8,6r+9$ |

For the $A$ row, reverse the original block index by
$r\mapsto k-1-r$. The other rows follow by direct substitution into
the displayed motions and $z=y-5\lfloor x/2\rfloor$.
Their unions are

\[
 G_0=\{-3,-2,-1,0\}\cup[2,6k+1]_{\mathbb Z}\cup\{6k+3\},
\]

\[
 G_1=\{-2\}\cup[3,6k+4]_{\mathbb Z}\cup\{6k+6\}.
\]

They have $6k+5$ and $6k+4$ elements, respectively. Their total is $L$.
Every one of these cells gives a distinct quotient image, because each
parity range has diameter less than $L$ for $k\ge1$.

The half-turn sends $(e,z)$ to $(1-e,-1-z)$. Indeed,
$x'=1-2k-x$ has parity $1-e$ and quotient $q'=-k-q$,
so

\[
 z'=(-5k-1-y)-5(-k-q)=-1-z.
\]

Now the residues of $G_0$ in $\mathbb Z/L\mathbb Z$ are

\[
 \{0\}\cup[2,6k+1]_{\mathbb Z}\cup\{6k+3\}
 \cup\{L-3,L-2,L-1\}.
\]

Their complement is exactly

\[
 \{1,6k+2\}\cup[6k+4,L-4]_{\mathbb Z},
\]

which is $-1-G_1$ modulo $L$. Thus
$G_0\sqcup(-1-G_1)=\mathbb Z/L\mathbb Z$.
Applying $z\mapsto-1-z$ gives the other parity identity
$G_1\sqcup(-1-G_0)=\mathbb Z/L\mathbb Z$.
All $2L$ cosets therefore occur exactly once in the six displayed copies.
This establishes the assertion for **every integer $k\ge1$**, without
an extrapolation from finite tests. $\square$

## Nineteen-cell construction and research scope

For $k=4$, the original terminal-exchange search selected the same tile
under the motion $(x,y)\mapsto(5-y,-7-x)$. It found six strict disc
coronas with copy counts

\[
 1;\quad5,11,21,27,35,43.
\]

The 143 exact poses in `six-disc-k4.json` are checked directly by
`coronas.py`: whole-copy disjointness, Euclidean isometries, full halo
coverage, attachment to the previous corona, connectedness and absence
of holes at every prefix. The final patch contains $143\cdot19=2717$
unit cells. This is a construction certificate only. The plane-tiling
proof above excludes this tile from the finite-Heesch target.

The finite-five unmarked-polyhex frontier remains open. This result
removes the entire endpoint-shift subfamily from that search. It does
not classify other terminal exchanges or the unshifted $T_k$ family.
The earlier results for $T_4$ and $T_5$ are separate objects:
[T4 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-2/strip-t4/proof.md),
[T5 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-2/strip-t5/proof.md).

Primary convention and status context:
[Kaplan, Heesch Numbers of Unmarked Polyforms](https://arxiv.org/abs/2105.09438),
[author census](https://cs.uwaterloo.ca/~csk/heesch/), and
[Kaplan, The Path to Aperiodic Monotiles](https://arxiv.org/abs/2509.12216).
These were refreshed on 2026-10-01. The census covers polyhexes through
17 cells; the present explicit 19-cell case has no historical-priority
claim. In the usual convention a plane tiler has infinite Heesch number.
