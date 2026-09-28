# Exact paired-prefix maximum 109 and consequences for shifted Schur constructions

The greatest endpoint of the five-colour paired construction defined below is
**109**. A complete witness is supplied; the bare 110-point CNF is UNSAT with
a checked DRAT proof. This yields an exact endpoint maximum **334** for a
specified six-colour shared-column middle-third family. A complete 334-point
word attains that maximum. It also lowers a common-fibre capacity at modulus
545 from 32 to **24**, classifies its equality support, and gives a necessary
additional column split for the previously prepared 158-point class.

These are restrictions on particular constructions. They do **not** improve
the classical lower bound S(6) >= 536. We use the largest-colourable-endpoint
convention and include x=y in every Schur condition. No full 537-point word
is supplied. No priority claim for the restricted prefix result is intended.

## 1. The finite prefix theorem

Use colours 0,1,2,3,4. Every complete pair satisfies

* (c(5q+1),c(5q+2)) is (0,1) or (j,j), j in {2,3,4};
* (c(5q+3),c(5q+4)) is (1,0) or (j,j), j in {2,3,4}.

Multiples of five are unrestricted. An incomplete terminal pair has any
allowed first entry. These are ordinary integer prefixes; no cyclic or
reflection hypothesis is imposed on the prefix itself. Require
c(x),c(y),c(x+y) not all equal whenever 1 <= x <= y and x+y <= N.

**Computer-assisted theorem.** Such a word exists exactly up to endpoint
109. `witnesses.json` supplies a complete length-109 word. `verify.py`
checks all 2,970 unordered Schur equations, including all 54 doublings.
Restriction of a longer word preserves the definition.

For N=110, `prefix.py` assigns one indicator to each allowed state of a
pair or axis point. One-hot clauses choose a state, and each literal Schur
equation forbids its monochromatic states. The only symmetry clauses order
first occurrences of the three common colours. Any solution admits this
normalization by permuting 2,3,4; the two special colours are never exchanged.

`audit.py` independently builds the point table block by block and assembles
the complete CNF by enumerating equations by their output. It matches every
clause, including one-hot and palette clauses, with the generator. A small
exhaustive audit also compares all 11,664 four-colour assignments at N=14
against a definition-level word checker: 242 are valid, and all 242 admit
the stated normalization.

The bare N=110 instance has 286 variables and 7,827 clauses. It contains no
cover clauses or assumed values of S(4), S(5), or other Schur numbers.

* CNF: 131,765 bytes; SHA-256
  `627bb81fd23127c3f4276f536b892b93dd7eb52b8e440c3781882a75472db71c`.
* Recorded DRAT proof: 64,411,538 bytes; SHA-256
  `c03ebd7aededf8f111795cb725f51ba3420cae2925d6beb4b70f4762058f0b86`.
* CaDiCaL 1.9.5 returned UNSAT; DRAT-trim independently returned VERIFIED.

The proof is regenerated and checked by `prove.py`; its large binary output
is deliberately not distributed. Hashes record the run, rather than replace
proof checking. The mathematical encoding and palette-completeness argument,
the finite audit, the standard Python runtime, and DRAT-trim are explicit
trust boundaries. This is not a proof-assistant formalization or an external
peer review.

## 2. The shared-column construction and exact maximum 334

Let a >= 3 be odd, n=5a, and colour the nonzero residues modulo n, represented
by [1,n-1], symmetrically: c(x)=c(n-x). Partition the nonzero axis residues
modulo a into symmetric sets E_0,...,E_5, and partition Z_a into states
R,C_2,C_3,C_4,C_5. For b=1,2 set

    c(5q)   = i if q in E_i;
    c(5q+b) = b-1 if q in R, and i if q in C_i;
    c(n-5q-b) = c(5q+b).

The state column is thus shared by the two lower residues. This is the
shifted construction, using quotient and remainder coordinates, not the
earlier reflected CRT family. In any valid word, 0 lies in R. Reflection
makes ordinary and modular Schur-freeness equivalent: a modular equation
whose sum exceeds n can be reflected to an ordinary one.

Three necessary conditions follow directly from literal modular equations:
E_i is sum-free, E_i avoids C_i-C_i, and -1 is absent from C_i+C_i+C_i.
The difference condition follows by adding an axis point to a fibre point.
For the last condition use short residues 2+2+1=5 and reflection.
The exact full criterion is documented in the earlier
[shifted interval construction](../schur6_shifted_fibre_interval_obstruction).

**Restricted-family theorem.** If some C_i is the entire undilated interval

    I_a = {q in Z : a/3 < q < 2a/3},

then the maximum possible endpoint n-1 is exactly **334**.

Proof. If 3 divides a, reflection identifies the colours of n/3 and 2n/3,
contradicting doubling. If a=3m+2, then q=2m+1 lies in I_a and 3q=-1 modulo
a, contradicting the preceding triple condition. Thus a=3m+1 with m even,
and I_a=[m+1,2m]. The difference condition excludes axis residues 1,...,m-1
from E_i. The earliest off-axis occurrence of colour i is at least 5m+3.
Hence colour i is absent from [1,5m-1]. The remaining five colours form a
paired prefix. Since endpoint 110 is impossible, m >= 24 is impossible
(5m-1 >=119). Evenness gives m <=22, a <=67, n-1 <=334.

For attainment, `witnesses.json` gives a complete shared word with a=67,
C_2=[23,44], and E_2=T union(-T), where T={22} union[24,33]. Its class sizes
are 44,44,110,52,44,40. The first occurrence of colour 2 is at position 110.
The independent verifier checks all 27,889 ordinary equations and 55,778
nonzero modular equations, reflection, the shared-column pattern, and the
specified supports. Removing colour 2 from its first 109 positions gives
another positive prefix witness.

This bound concerns an **undilated full middle-third common fibre, shared
columns, and short factor five**. It does not exclude all unit dilates, the
whole shared family, independent columns, the CRT family, or factor seven.

## 3. Capacity 24 and the 64 axis extensions at a=109

**Theorem.** In a shared word modulo 545, if a common support C_i is contained
in I=[37,72], then |C_i| <=24. Equality forces

    C_i = [37,48] union [61,72],     {12,97} subset E_i.

Proof. All off-axis occurrences of i are >=183. If E_i had no d in [1,22],
the first 110 points would be a forbidden five-colour paired prefix.
Therefore some such d belongs to E_i, and d is absent from C_i-C_i.
On the 36 consecutive vertices of I, join vertices at distance d. This
graph is a disjoint union of paths. Its independence capacities for d=1,...,22
are

    18,18,18,20,20,18,21,20,18,20,22,24,23,22,21,20,19,18,19,20,21,22.

The unique maximum 24 occurs at d=12. The graph then consists of twelve
three-vertex paths, each with its unique maximum independent set of both
ends. Their union is exactly the displayed C_i. This proves both claims.

Consequently all 16 earlier size-32 boundary supports are excluded at once,
as are all supports in I of sizes 25 through 36. The corresponding statement
does not hold automatically for two independently chosen columns.

For the equality support C, its difference set is

    C-C = {0} union +/-([1,11] union [13,35]).

The allowed symmetric axis orbits have representatives {12} union[36,54],
with 12 forced. After forcing 12, all sum-free constraints among the
remaining representatives reduce to a four-cycle

    36 -- 37 -- 49 -- 48 -- 36

and the five three-vertex paths

    38--50--47, 39--51--46, 40--52--45, 41--53--44, 42--54--43.

There are exactly 2*2^5=64 maximal choices: select an opposite pair in the
cycle and either both ends or the centre in each path, then include 12.
The axis cardinalities 16,18,20,22,24,26 occur respectively 2,10,20,20,10,2
times. `boundary.py` checks all 524,288 subsets of the remaining 19 orbits;
21,875 are valid with orbit 12, and precisely 64 are maximal. Each resulting
single-colour point set also passes a literal modular sum check.

These 64 choices cover existence of a completion: enlarge E_i to a maximal
allowed set and remove those axis points from the other colours. Its own
sum and difference constraints remain valid, while all other classes shrink.
This is an axis recolouring argument, not a claim that every word was already
maximal or that all 64 choices are equivalent. A complete six-colour word
at this boundary remains unresolved. Two bounded pilots on the two choices
of axis size 26 returned UNKNOWN and establish no exclusion.

## 4. A necessary additional split for the 158-point class

In the independent-column extension, let Q_1(q),Q_2(q) be the states at
residues 5q+1 and 5q+2, reflected as above. Each state is R or a common label.
Fix common colour 2 on

    A_2 = [39,72] minus {63},
    B_2 = [37,67] union {77},
    E_2 = [41,68].

These supports define a modular sum-free class of 158 points whose smallest
point is 158. They force the nine column disagreements

    D_0 = {37,38,63,68,69,70,71,72,77}.

**Necessary split.** Any complete six-colouring with this fixed class must
also have an actual state disagreement Q_1(q) != Q_2(q) at some coordinate

    q in U = [0,21] union [87,108].

Indeed U consists exactly of the coordinates whose complete lower or
reflected upper pairs are seen through 110. Equality on U would give the
forbidden paired five-colour prefix, since colour 2 is absent there.
Since U and D_0 are disjoint, every completion requires at least ten actual
column disagreements. Thus the model allowing splits only in D_0 is
impossible. This argument does not exclude the full independent-column model
or assert that one extra split suffices. `verify.py` checks the class, its
first point, D_0, and the exact prefix-coordinate calculation.

## Reproduction

Use Python 3.11+ without `-O`. No Python packages are needed for the audits.
From this directory:

```sh
python3 -B verify.py
python3 -B audit.py
sha256sum -c SHA256SUMS
```

`audit.py` must print `ALL_AUDITS_MATCH_EXPECTED`. It checks witness and
encoding data and the finite axis classification; it does **not** substitute
for regenerating and checking the UNSAT proof.

Build [CaDiCaL](https://github.com/arminbiere/cadical) at commit
`146207318796f094dcded87349a64f0c6927309e` (1.9.5) and
[DRAT-trim](https://github.com/marijnheule/drat-trim) at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Then run:

```sh
python3 -B prove.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
```

The expected status is `UNSAT_DRAT_VERIFIED`. The recorded run used about
62 seconds for solving and 84 seconds for checking; runtimes vary.
The wrapper uses a temporary directory, a 512 MiB proof-file cap, and
300-second solver/checker limits by default. Timeouts are inconclusive.
The CNF hash is checked before solving. The proof bytes are removed only
after checking; `proof.generated.json` records the result. Exact proof bytes
can depend on the solver build, so a different proof hash is acceptable if
the same CNF independently verifies. Source hashes cover all distributed
files except `SHA256SUMS` itself.

Literature context: the classical lower bound 536 is due to
[Fredricksen and Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
and remains the reference bound in
[arXiv:2607.15034](https://arxiv.org/abs/2607.15034).
The preceding local constructions are recorded in
[shifted interval obstruction](../schur6_shifted_fibre_interval_obstruction)
and [affine/independent columns](../schur6_affine_column_normal_forms).
