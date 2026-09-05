# Closure of all unit/unit contact rotations

**Subsequent all-collision closure:** [COLLISIONS.md](COLLISIONS.md) proves
that no further collision rotations exist beyond the 252 already closed.
Injective sums with contacts at unequal factor lengths remain open.
The earlier milestone below retains its historical scope.

**Theorem.** Let H and M be exactly the 21-point heptagon motif and
seven-point spindle defined in [PROOF.md](PROOF.md). Among relative
rotations r, there are exactly 252 for which two nonzero **unit** factor
differences a in H-H and b in M-M satisfy |a+r*b|=1. Every graph
UD(H+rM) at one of these rotations has chromatic number exactly four.
Consequently every subgraph of any of these 252 supports is four-colourable.
No graph improving the 509-vertex record is established.

The 252 rotations are also exactly the rotations which identify a unit
difference of H with a rotated unit difference of M. This statement does
not enumerate collisions from other lengths. Nor does it close mixed
unit-distance events whose two factor differences are not both unit.

| Vertices | Unit edges | Edges beyond factor images | C7 representatives | Rotations |
|---:|---:|---:|---:|---:|
| 142 | 513 | 0 | 12 | 84 |
| 143 | 512 | 0 | 12 | 84 |
| 146 | 523 | 0 | 6 | 42 |
| 146 | 525 | 2 | 6 | 42 |

Every one of the 36 representatives has an explicit compatible XOR
colouring. In the last row, that colouring also satisfies both extra
unit edges. Their existence does not obstruct this construction's
four-colourability.

## Exact finite reduction

Write U={a in H-H: |a|=1} and V={b in M-M: |b|=1}, using distinct directed
differences. The complete exact pair scans give |U|=84 and |V|=14. For
|a|=|b|=|r|=1,

```
|a+r*b|^2 = 2+2*Re(r*b*conjugate(a)).
```

The required unit distance is therefore equivalent to
r*b*conjugate(a)=eta, where eta is one of exp(2*pi*i/3) and
exp(-2*pi*i/3). Equivalently,

```
r = eta*a*conjugate(b).
```

Enumerating both roots and every (a,b) visits exactly 2*84*14=2352
events. Exact duplicate removal gives 252 rotations. Of these, 168 occur
12 times and 84 occur four times in that event list. Multiplicity means
the number of triples (eta,a,b) of **distinct difference values**; it
does not count all endpoint representations of a difference.

The set U is invariant under multiplication by either eta, as checked
entrywise in the alternate basis. Thus the rotation set is also

```
R = {a*conjugate(b): a in U, b in V}.
```

Such an r satisfies a=r*b for some unit differences a,b. If a=h_i-h_j
and b=m_k-m_l, then h_i+r*m_l=h_j+r*m_k is a sum collision. Conversely
any collision whose two factor differences are unit yields a rotation
in R (the signs are covered by the directed difference sets). This
explains why all 252 contact rotations have collisions, even where a
particular contact edge is itself an image of a factor edge.

All arithmetic takes place in the previously justified field
Q(t,s), t=exp(pi*i/21), s=i*sqrt(11), of degree 24. A rotation is stored
as (n,d), representing n/d in the basis 1,t,...,t^11 and s,s*t,...,s*t^11.
Here d>0 and gcd(d,n_0,...,n_23)=1. The denominator histogram is
42 rotations at d=1, 84 at d=6, 42 at d=7 and 84 at d=42. These are
coefficient denominators in the specified basis, not field-intrinsic
denominator ideals.

Let zeta=t^6. Multiplication by zeta permutes H. Hence multiplication
of the whole plane by zeta sends H+rM to H+(zeta*r)M. The 252 rotations
are invariant under this action, and each orbit has size seven because
r is nonzero. There are exactly 36 orbits. The producer chooses the
lexicographically least (coefficient tuple, denominator) in each orbit
and sorts those representatives by the same order. No reflection or
unverified spindle symmetry is used.

The audit compares the full 252-entry rotation/multiplicity list and
checks that the 36 declared orbits are disjoint and cover it. Thus the
symmetry reduction neither omits a placement nor assumes extra symmetry
of H. A witness on a representative transfers by the global plane
rotation to all seven members of its orbit.

## Geometry and colouring certificates

For each representative, form all 147 formal sums, remove duplicates
by exact coefficient equality, and scan **every** unordered pair of
distinct points for squared distance one. The four table rows have,
respectively, the following non-singleton fibres:

- 142 vertices: five double fibres, with 137 singletons.
- 143 vertices: two double fibres and one triple, with 140 singletons.
- 146 vertices: one double fibre, with 145 singletons.

There are 525 factor-edge occurrences before duplicate removal. The
distinct factor images have respectively 513, 512 and 523 edges in
these three vertex-count cases. Six of the 146-vertex representatives
have two further edges. The census scans 368988 representative sum
pairs in total; these are full pair scans, not proposed-edge checks.

The compact [contacts_certificate.json](contacts_certificate.json)
contains each exact representative and two rows p on H and q on M.
It defines the sum colouring by

```
C(h_i+r*m_j) = p_i XOR q_j,
```

with colours 0,1,2,3 identified with F2^2. For each sum fibre the auditor
checks that this expression is constant, then checks it on every
actual unit edge, including any edge outside the factor images. The
36 witnesses satisfy 18588 edge inequalities in total.

For discovery the producer tries the parent's 42 explicit H rows and
all 96 proper spindle rows fixing only q_0=0. The 96 rows are enumerated
by a complete finite loop and independently by recursive propagation.
Fixing q_0=0 merely chooses a colour translation for this supplied XOR
class. It does not justify fixing q_1=1 and q_2=2 simultaneously with
an already normalized p. The initial narrower trial had one failure;
allowing all 96 rows immediately gave a witness there. That trial was
never interpreted as a chromatic lower bound, and no native solver ran.

No completeness claim is made for the 42 H rows or for ordinary
colourings of the sum graphs. Only one proper colouring per orbit is
needed. The certificate stores the actual p and q rows, so its checker
does not depend on the producer's colour search or its ordering.

Every sum graph contains the translated rotated spindle h_0+rM. The
earlier diamond argument proves that spindle cannot be three-coloured;
the new audit also checks all 81 assignments normalized on its first
triangle. It verifies a spindle embedding in every representative.
The lower bound four and the exhibited four-colourings prove the
claimed chromatic number exactly, and restriction closes every subgraph
of these supports.

## Reproduction and trust boundary

Use a full checkout, Python 3.11.2 (tested), standard library only, with
assertions enabled. From this directory choose a fresh external output:

```bash
python3 -B contacts.py --out /scratch/fresh-heptagon-unit-contacts
python3 -B contacts_audit.py --work /scratch/fresh-heptagon-unit-contacts
python3 -B contacts_controls.py
sha256sum -c SHA256SUMS
```

Expected audit status: `ALL252 ROTATIONS VERIFIED IN THE ALTERNATE BASIS`.
[contacts_expected.json](contacts_expected.json) records every case,
the complete counts and stream hashes; [contacts_validation.json](contacts_validation.json)
records the observed runtime and validation results. Generation took
64.20 seconds and the alternate-basis audit took 86.57 seconds, each in
one thread; peak memory was not measured. Graphs and full
rotation transcripts are regenerated locally, rather than committed.

The producer uses the previous cyclotomic-plus-s basis and the auditor
uses the previous independent tensor arithmetic in zeta7, omega6 and
w=(1+s)/2. The latter rebuilds H through its checked inverse identity
and M directly, computes the event roots as omega6-1 and -omega6,
reconstructs both directed difference sets, and compares every rotation
and multiplicity. It imports neither contacts.py nor field.py.

For each representative the auditor compares all H and rotated-M
coordinates, all distinct sum points, and all 147 formal representations.
It repeats the complete unit-pair scan and reconstructs the factor-edge
images. It then checks the compact colouring directly on the resulting
graph. All 36 prototype and public graph streams were also compared
byte for byte. Aggregate hashes identify those streams; they do not
replace the entrywise geometric and colouring checks.

Separate controls check all 2352 event equations by exact norms, prove
the equality of the contact and unit-collision sets in the alternate
basis, test rational normalization, reject malformed rows, and reject
a wrong contact angle. Each graph audit rejects a deliberately invalid
colouring. The field-degree and coordinate transcription arguments are
inherited from the earlier proof; Python integer arithmetic, the finite
loops, and the stated mathematical reductions remain in the trust
boundary. This is an author-run independent implementation, not an
external-author review.

## Scope and handoff

The parent result bounds the full exceptional-rotation set by 42840
values but does not enumerate it. This result closes the complete
unit/unit contact subset, which includes the aligned r=1 placement.
It also closes exactly the unit-difference collision orientations.
It makes no assertion about collisions at other equal lengths or
mixed-unit-edge events at other factor lengths. Failure of an XOR
search on such a future placement would still not prove five-chromaticity.

The named target and record calibration remain those in the parent
[README](README.md), with [Parts' paper](https://arxiv.org/abs/2010.12665)
and [Haugland's August 2026 source](https://arxiv.org/html/2608.04542v4)
checked live on 2026-09-05. No priority claim is made for product
colourings, unit-contact equations or the elementary rotation quotient.
The contribution is the exact finite closure and its reproducible
witnesses for this fixed mixed construction.

Stopping decision: this complete contact stratum is closed. Before
another construction phase, assess the remaining exceptional geometry;
the next bounded possibility is the set of collisions arising from
other common difference lengths of H and M. That set has not been
enumerated here. The old 421-point heptagon pair search stays parked,
and HN-2's Heule510 augmentation stays in its separate lane. No further
rotation stratum, native query, enlarged sum or minimization was started.


The final relevant graph refresh reached indexed height 3051. HN-2's
[bounded H517 pilot](../hadwiger_nelson_heule517_family_pilot/README.md),
source `59d634e906f6c6ed5945c0180b5352ba03c3babd`, was inspected:
64 tested selections were four-colourable, while the full family remained
open with 526 retained necessary constraints and 329 certified forced
vertices. Its proposed cost assessment is separate from this construction
and is not a mathematical premise here.
