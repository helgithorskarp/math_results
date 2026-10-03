# Seven productive tails for the marked minimum-eight prefix

Actual author: **six-covering-2**, role **researcher**, 2026-10-03.
Author-checked computer-assisted BASE bound and an ordinary combinatorial
tail-allocation proof. The ordinary reductions are unformalized and
independent review is pending. Global LCM bounds remain unchanged.

## Exact domain and result

Consider a finite covering of all integers with pairwise distinct ORIGINAL
moduli dividing 10080, minimum modulus EXACTLY 8, containing

```
8:0, 9:0, 10:1, 14:0, 12:10, 16:2, 28:4, 32:6.
```

The notation `m:a` means (a\pmod m). Assume EXPLICITLY that the placed
classes at original moduli **16 and 32 are essential**: deleting either
destroys the covering. This result does not establish that hypothesis
from presence alone.

BASE is ALL selected original divisors of 2520. Its holes are uncovered
residues modulo 2520. Every other original divisor of 10080 is (16d)
or (32d), (d\mid315). A selected TAIL class is productive when it
covers a physical 10080-period lift of a BASE hole. The productive count
(T) includes the placed classes at 16 and 32. All other phases and
omissions are free; the actual LCM is initially required only to divide
10080.

**Theorem. Every such covering has (T\ge7).**

Two precise intermediate results establish this:

1. Every BASE inventory containing the six literal BASE classes
   `8:0,9:0,10:1,14:0,12:10,28:4` leaves at least **177 holes**.
   This part does not assume either essentiality or any TAIL selection.
2. In the marked essential domain above, exactly six productive TAIL
   classes can cover at most **150 BASE holes**, all in parents 2 and 6
   modulo 8. The abstract capacity 150 is sharp.

The [previous five-tail lemma](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-five-tail-capacity/proof.md)
(graph 9920, source 2f198b4dd8c11b17a5b79b7164315bab1ffb8b58)
proves (T\ge5) and the corresponding five-tail capacity 120, under
the SAME explicit hypotheses. Since (177>150>120), neither five
nor six productive tails suffice, proving the theorem.

This is a condition on a literal prefix and divisor inventory. It does
not normalize every minimum-eight cover to this prefix, prove existence
with seven tails, exclude the entire prefix, or improve (L_{\min}(8)).

## 1. Complete BASE bound from 270 raw phase pairs

Let (R) be the residues modulo 2520 missed by the six literal BASE
classes. Direct arithmetic gives (|R|=1396). Their occupied labels
are removed from the list of divisors of 2520 at least 8. The complete
35 unused ORIGINAL BASE labels are

```
15 18 20 21 24 30 35 36 40 42 45 56 60 63 70 72 84
90 105 120 126 140 168 180 210 252 280 315 360 420
504 630 840 1260 2520.
```

Original 21 is included. All 9251 raw phases of these labels are
allowed. Omissions are allowed as well.

Fix the actual raw phases (a\pmod{15}) and (b\pmod{18}). There
are exactly (15\cdot18=270) pairs, with no symmetry quotient. Let
(F_{a,b}\subset R) be their union inside R. For each of the remaining
33 ORIGINAL labels (m), define

\[
M_m(a,b)=\max_{0\le c<m}|(R\setminus F_{a,b})\cap(c\pmod m)|,
\qquad K(a,b)=|F_{a,b}|+\sum_m M_m(a,b).
\]

For any extension of this phase pair, its entire BASE union covers at
most (K(a,b)) points of R. Each remaining original chooses at most
one phase; summing its individual maximum may overcount overlaps, which
preserves the upper bound. Every remaining original, including 2520,
is retained in this sum.

The exact complete computation gives

\[
1051\le K(a,b)\le1219\quad\hbox{for all 270 raw pairs}.
\]

Therefore the completed BASE inventory leaves at least
(1396-1219=177) holes. Completing an omitted BASE original by any
phase can only reduce holes, so the same lower bound holds for every
allowed partial inventory. The full phase-domain reduction is just
these 270 pairs followed by valid independent marginal upper bounds;
there is no unfinished search subtree.

The [producer](generate.py) groups R into 1396 compact bit positions.
The [literal audit](audit.py) imports no producer module: it constructs
all BASE labels from prime powers, uses physical 2520-position masks
for arithmetic progressions, and visits phase pairs and marginals in
reverse order. It compares EVERY phase, union size, all 33 marginal
values and the final bound in all 270 rows, not only extrema. The row
stream is hashed in increasing 15/18 phase order:

```
c214c028ebc73a49983861a523d6b7b9755193d97927d1bfc135b83775ac817c
```

One audit checks 8910 original marginal values and 2488860 physical
phase intersections. Ten semantic damages, with repaired row hashes,
must be rejected: cutoff, first phase, last bound, last original
marginal, deleted row, duplicated row, omitted original 21, changed
14 phase, wrong initial hole count, and a false 178 lower-bound record.
Valid input is accepted in both interpreter modes. The exact 177 bound
is not asserted optimal for the actual BASE union.

## 2. Six productive tails: the complete allocation split

Each BASE hole has four physical lifts modulo 10080. A (16d) class
meets zero or two, a (32d) class zero or one. Each class lies in one
parent modulo 8. Essentiality of placed 16 and 32 gives exclusive
witnesses and hence nonempty parents 2 and 6. Parent 2 requires at
least two productive classes; the placed 32 class in parent 6 requires
at least three classes there. These are the same ordinary four-lift
arguments as in graph 9920.

For (T=6), no third parent has holes: it would require at least two
more productive classes, in addition to the compulsory (2+3).
The only allocations to parents 2 and 6 are therefore (2+4) and
(3+3).

The initial odd shadow in either parent is

\[
U=\{y\pmod{315}:y\not\equiv0\pmod9,
        \ y\not\equiv1\pmod3,\ y\not\equiv0\pmod7\},\quad |U|=150.
\]

The [9920 CRT product formula](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-five-tail-capacity/proof.md)
gives the exact one-congruence capacities (C(d)):

| d | 1 | 3 | 5 | 7 | 9 | 15 | 21 | 35 | 45 | 63 | 105 | 315 |
|---|---|---|---|---|---|----|----|----|----|----|-----|-----|
| C(d) | 150 | 90 | 30 | 25 | 30 | 18 | 15 | 5 | 6 | 5 | 3 | 1 |

Every additional (16d) or (32d) has (d>1): original 16 is already
used in parent 2 and original 32 in parent 6. Distinct ORIGINAL 16-type
labels have distinct d's globally, and likewise for 32-type labels.
A 16-type and 32-type resource may share d. From this table:

* Two distinct unused 16-label footprints have total capacity at most
  (90+30=120); three have total capacity at most (90+30+30=150).
* An intersection for two distinct unused 32 labels has capacity at
  most 30. Its odd lcm cannot be 3, 5 or 7, which have only one divisor
  greater than one; its least possible lcm is 9.
* For three distinct unused 32 labels the capacity is at most 18:
  an odd lcm smaller than 15 has fewer than three divisors greater
  than one. The table bounds every allowed lcm at least 15 by 18.

Incompatible odd congruences have empty intersection; otherwise their
intersection is one class modulo their lcm. For a union, the sum of
individual C bounds is valid regardless of overlaps. Additional BASE
classes only shrink the initial shadow.

### Allocation (2+4)

The second resource in parent 2 MUST be an extra 16-type class. One
16-type class and one 32-type class cover at most three lifts. Its
footprint contains every hole in this parent.

In parent 6 there are three classes besides placed 32. If all three
were 16-type, any fully covered hole would have active opposite
halves among those classes. They would already cover all four lifts
without placed 32. This would hold at every BASE hole in this parent,
and placed 32 meets no other parent. Deleting it would preserve the
covering, contrary to essentiality. Thus the remaining possibilities
are exactly:

| Types besides placed 32 in parent 6 | Necessary footprint bound | Total bound |
|---|---|---:|
| two 16-type, one 32-type | Every hole lies in at least one extra 16 footprint | 150 |
| one 16-type, two 32-type | Every hole lies in the extra 16 footprint | 120 |
| three 32-type | Every hole lies in their triple odd intersection | 108 |

For the first two rows, without any active extra 16 class there are
at most two or three active singleton lifts, respectively. The total
bounds use three or two globally distinct unused 16 labels across
BOTH parents. In the last row all three extra singleton classes must
be active at every hole, giving at most (90+18=108).

### Allocation (3+3)

In parent 6 the two classes besides placed 32 must be one extra
16-type and one extra 32-type. Two extra 32 classes cannot cover four
lifts. Two extra 16 classes would both have to be active with opposite
halves at every hole, again making placed 32 redundant. Every hole in
parent 6 lies in the extra 16 footprint.

Parent 2 has two classes besides placed 16. These are exactly:

| Other types in parent 2 | Necessary footprint bound | Total bound |
|---|---|---:|
| two 16-type | Every hole lies in the union of their footprints | 150 |
| one 16-type, one 32-type | Every hole lies in the extra 16 footprint | 120 |
| two 32-type | Every hole lies in their odd intersection | 120 |

In the middle row, an inactive extra 16 leaves at most three covered
lifts. In the last, both singleton classes must be active to fill the
half missed by placed 16, so their intersection has capacity at most
30. Parent 6 contributes at most 90. The first two rows again use
globally distinct unused 16 labels across both parents. This proves
the six-tail capacity bound 150 and exhausts all allocations.

## 3. Sharp abstract 150-hole model

In parent 2 use (U\cap((2\pmod3)\cup(3\pmod9))), of size 120;
the two component footprints are disjoint and have sizes 90 and 30.
In parent 6 use (U\cap(0\pmod5)), of size 30. The six original TAILs

```
16:2, 32:6, 48:26, 144:138, 80:30, 160:150
```

cover all 600 lifts of these 150 abstract holes. Each has an exclusive
witness: 2, 230, 26, 138, 30, 150 respectively. The [six-tail checker](six_tail.py)
verifies all literal AP memberships, all 321 binary type/active-footprint
controls, and the full two-/three-label capacity rows.

This is abstract capacity sharpness. It does not supply a BASE inventory
realizing these holes or a full covering. Indeed the 177 BASE lower bound
prevents such a realization in the stated literal domain.

## 4. Reproduce the complete evidence

From this directory, Python 3.11+ standard library only:

```sh
python3 -B verify.py
```

The [driver](verify.py) regenerates all records from the three source
files, then runs the producer, literal audit and six-tail checker normally
and with optimization, sequentially. Every child has a 20-second guard;
numerical thread settings are all one. The BASE producer retains its
18-second soft cap and 300-retained-tuple cap. Its FIRST complete 270-row
stage closes; later configured stages are neither needed nor executed.
Timeout, cap failure or incomplete output establishes no exclusion.

The [expected manifest](expected.json) pins the ENTIRE deterministic
mathematical records, including every phase, all marginals, every
capacity/type row and all rejection controls. Only the producer's elapsed
wall time is excluded from record comparison. Generated full records
remain outside the published source and are regenerated in an ignored
directory. No private certificate, old negative root, native solver,
floating-point result or external numerical table is a premise.

Ordinary divisor completion, union upper bounds, four-lift transport,
essentiality/redundancy and complete allocation arguments remain
unformalized. CPython/runtime and finite integer enumeration are explicit
trust boundaries. Two different representations and both interpreter
modes are SAME-AUTHOR checks, not independent review.

The complementary [9859 five-tail result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/five-productive-tail/proof.md)
credits generic four-lift and original-label geometry. Its prefix uses
1 modulo 14; its numerical 127-hole and later private capacity tables
are not imported here. The BASE 177 calculation is freshly generated
for 0 modulo 14 and fixed 4 modulo 28. The precise dependency on 9920
is its same-domain compulsory-tail/five-tail argument and CRT shadow
capacities, not any private presence theorem.

Primary family context was reopened live 2026-10-03:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) reports the minimum-seven
LCM claim; [Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644)
studies restricted prime support. Neither paper supplies a numerical
certificate here. No historical priority is claimed.

The remaining task is compatibility of seven or more productive tails
with the full BASE inventory. The modulus-32 representative 10 is a
different remaining root; no seven-tail bound is transferred to it.
