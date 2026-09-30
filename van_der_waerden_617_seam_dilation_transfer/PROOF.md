# Dilation transfer for affine QR617 seam repair constraints

Author: **six-vdw-3**, role **researcher**. An elementary transfer theorem
with two explicit exact computer-assisted numerical dependencies. The new
complete direct checker is by the same author; no independent peer review
or proof-assistant formalization of this transfer is claimed.

## Reference words and candidate quantifiers

Coordinates are integers. Let $p=617$ and let $q(r)=0$ on nonzero
squares modulo $p$, $q(r)=1$ on nonsquares. Leave $q(0)$ unspecified.
At a seam $b$, use the partial reference

\[
T(x)=\begin{cases}q(x-b+s),&x<b,\\
q(x-b+t)\oplus g,&x\ge b,\end{cases}
\]

where $0\le s,t<p$, $g\in\{0,1\}$, and $(s,t,g)\ne(s,s,0)$.
There are $2p^2-p=760761$ such incompatible keys. The reference is
defined only at nonpoles. A candidate is **any** binary coloring avoiding
all monochromatic seven-term integer APs with positive difference.
Its pole colors and every other value are arbitrary. Count its edits only
where the reference is defined.

Nonzero affine slopes on either side are included: at nonpoles,
$q(\alpha z+\beta)=q(\alpha)\oplus q(z+\beta/\alpha)$.
Normalize each side, then exchange all colors to make the left orientation
zero. No affine or periodic assumption is imposed on the candidate.

## Transfer theorem

Let $R,k$ be positive integers. Suppose every incompatible key has $k$ pairwise disjoint, pole-free,
monochromatic crossing seven-term APs within $[-R,R)$. Then for every
positive integer $m$ with $p\nmid m$, every incompatible seam has

\[
\boxed{\text{at least }k\text{ edits in each class }x-b\equiv j\pmod m
\text{ within }[b-mR,b+mR),\quad 0\le j<m.}
\]

In particular the interval requires at least $km$ nonpole edits. Both
adjacent reference segments must have length at least $mR$, so that the
reference is available on the entire interval. The base hypothesis can
instead be stated directly as the corresponding all-candidate $k$-edit
lemma; the same pullback proof applies.

### Proof

Translate $b$ to zero. For a fixed $j\in\{0,\ldots,m-1\}$, the map

\[
z\longmapsto mz+j,\qquad -R\le z<R,
\]

is a bijection onto the class $j$ in $[-mR,mR)$. Since $j<m$,

\[
mz+j<0\quad\Longleftrightarrow\quad z<0.
\]

Thus the seam is preserved exactly, including the two half-open endpoints.
Put $u=m^{-1}\pmod p$, $s_j=u(s+j)$, and $t_j=u(t+j)$.
Multiplicativity gives

\[
q(mz+j+s)=q$m$\oplus q(z+s_j),\qquad
q(mz+j+t)=q$m$\oplus q(z+t_j)
\]

at nonpoles, with poles corresponding exactly. Multiplication by $u$
is injective, so $(s_j,t_j,g)$ is incompatible whenever $(s,t,g)$ is.
The two pulled-back orientations differ by the same $g$; $q$m$$ is
one whole-color exchange.

Pulling back the candidate preserves AP avoidance: an integer AP with
difference $d>0$ becomes an integer AP with difference $md>0$.
Apply the base edit lemma to this pullback. Its $k$ required edits lie in
class $j$. Alternatively, lift the base packing: disjointness is preserved
within the class, and different classes are disjoint. Each monochromatic
nonpole AP requires an edit. Summing the $m$ class counts proves $km$.
This proves the transfer for every positive $m$ prime to $p$, without
enumerating the infinitely many dilations. The condition $p\nmid m$ is
needed for this inverse and incompatibility argument.

## Numerical dependencies and the 3704-point profile

The [44-edit base](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_seam_edit_packing)
has $R=617,k=44$, source commit
`6958adbebd0535e4c2ba71f4f5b1ef4f5edc4946`, graph
`bafkreig7wwk62osibqv4fbbjnuiy4v73btgifnrwnkgirvdb5nmx2hoa34`.
The [18-edit base](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_local_seams)
has $R=308,k=18$, source commit
`b4f4ca0ad27c9d3d4d536ff0d099a2b1186df4e1`, graph
`bafkreicmuyhhl7y6hlsjasnkrczca5epwa5brwrp3n23fqzqlxlteg7xee`.
These two numerical results are explicit mathematical dependencies.

For $I=[0,3704)$, $b=1852$, the theorem gives simultaneously:

| Base $R,k$ | $m$ | Window | Edits in each class modulo $m$ | Total lower bound |
|---|---:|---|---:|---:|
| 617,44 | 1 | [1235,2469) | 44 | 44 |
| 617,44 | 2 | [618,3086) | 44 | 88 |
| 617,44 | 3 | [1,3703) | 44 | **132** |
| 308,18 | 1 | [1544,2160) | 18 | 18 |
| 308,18 | 2 | [1236,2468) | 18 | 36 |
| 308,18 | 3 | [928,2776) | 18 | 54 |
| 308,18 | 4 | [620,3084) | 18 | 72 |
| 308,18 | 5 | [312,3392) | 18 | 90 |
| 308,18 | 6 | [4,3700) | 18 | 108 |

Each class is measured relative to $b$. In particular every AP-free
3704-point word differs from **every incompatible affine QR617 seam
reference** at at least **132 nonpoles**, already in [1,3703).
The three classes each require 44. This assertion needs only 1851 reference
positions on each side of one seam. The two extreme target positions are
unused. Profiles at different dilations generally overlap; their numerical
totals cannot be added without a separate disjointness or capacity argument.

This provides constraints within narrower windows and on the distribution
of edits among arithmetic sublattices. None of the constants is asserted
optimal or sufficient to repair a template.

## Direct complete check and independent arithmetic check

`check_lifts.cpp` reads the two source-generated base transcripts with strict
full-domain headers, exact lengths, and EOF. For every target key and each
of the nine profiles, it independently calculates the transformed key,
loads its selected base APs, and directly checks the lifted APs. It uses
Euler's criterion for target colors, the target integer coordinates, positive
differences, seam crossing, interval containment, exact class membership,
nonpoles, monochromaticity, and global vertex disjointness across all classes
of that profile. It imports no generator half-color table or search state.

The complete run checks 760761 keys per profile, 20540547 classes,
488408562 APs, and 3418859934 point incidences. The largest profile consists
of 132 disjoint APs per key. `expected.json` contains the complete compact
profile counts. A requested proper phase range reports `full_domain:false`
and cannot establish the full finite application.

`verify_transfer.py` independently uses Python integer/set arithmetic to
check the class partitions, the seam boundary, phase permutations and every
point/phase identity for the six target dilations. The written proof supplies the all-dilation quantifier; this finite check covers the six target dilations. The numerical bases
are regenerated and directly checked before the lifted check. Input hashes
identify the published deterministic base transcripts; positive AP checking
supplies the mathematical evidence.

All products and decoded coordinate expressions fit signed32-bit integers;
the largest possible malformed lifted endpoint is below three million.
Counts of incidences use unsigned64-bit arithmetic. The stamp index is below
seven million. There is no floating-point arithmetic or solver verdict.
The proof trusts exact integer semantics, the explicitly cited base lemmas,
the simple decoder/checkers, and the unformalized transfer and hitting-set
arguments. Generated base transcripts and all experimental corpora remain
outside publication; only compact source and evidence are needed.

## Positioning

The [equal-phase opposite-orientation geographic result](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_opposite_phase_edit_geography)
and its [independent review and color refinement](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_seam_review2)
quantify a smaller phase domain and separate inner/exterior edits. They are
context, not numerical inputs to this transfer. The fixed QR617 endpoint
repair profile and period618 construction fibers use different reference
words. Their constants are not transferred.

Monroe's [primary Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
were refreshed on 2026-09-30: the inspected length7/two-color seed is
>3703, with modulus617. Monroe writes $W(\text{length},\text{colors})$.
Here $W(2,7)$ means symmetric two colors/seven terms. Arithmetic dilation,
quadratic-character multiplicativity, and disjoint AP hitting are elementary
ingredients; no historical priority is claimed for them. The specific
class-resolved quantitative application uses the two cited campaign bases.
Bounded primary and graph/source inspection found no duplicate of this
application; this is not an exhaustive novelty or current-best claim.

This supplies no length3704 witness, unrestricted coloring exclusion, new
van der Waerden lower bound, or exact value. A length3704 AP-free witness
would establish $W(2,7)\ge3705$. The unrestricted target remains open here.
