# Interval obstructions for shifted reflected Schur fibres

**An all-parameter obstruction and a sharp necessary fibre-size bound.**
For the cyclic construction below with short factor 5 or 7, a common fibre
equal to the undilated middle third cannot give an endpoint above 484.
At modulus 545, even a common fibre merely contained in {37,...,72} must
have at most 32 elements. Equality forces one of 16 explicit supports and
forces its colour at axis coordinate 32 (integer position 160).

The size bound is sharp for the elementary difference constraint, not
asserted attainable by a complete Schur colouring. All 16 target cases
remain unresolved. There is **no new S(6) bound** and no exclusion of the
whole shifted family or of arbitrary symmetric colourings. Equal summands
are included. The classical convention is the greatest colourable endpoint.

## Cyclic construction and exact criterion

Let a>=3 be odd, p be 5 or 7, t=(p-1)/2, and n=pa. Symmetric sets
E0,...,E5 partition Z_a minus {0}. Sets R,C_t,...,C5 partition Z_a.
For 1<=b<=t and 0<=q<a, assign position pq+b the special colour b-1
if q belongs to R, and common colour i if q belongs to Ci. Give its
reflected position n-(pq+b) the same colour. Give position pq colour i
when q belongs to Ei, for q!=0. These rules partition [1,n-1].

In quotient/remainder coordinates, high short residues use the fibre
at a-1-q. This is a cyclic word with actual addition carries, not the
earlier [CRT product family](../schur6_reflected_fibres/README.md).
No coprimality between a and p is required; the target p=7,a=77 has n=539.

The word is sum-free modulo n if and only if:

1. Each Ei is sum-free modulo a.
2. Each common Ci is sum-free modulo a and -1 does not belong to Ci+Ci+Ci.
3. The union of the special E0,...,E_(t-1) avoids R-R.
4. Each common Ei avoids Ci-Ci.

In particular 0 belongs to R: otherwise 1+1=2 is monochromatic. If
gcd(a,3)=1, the unique solution of 3q=-1 also belongs to R.

For the criterion, the special short pair {b,-b} is sum-free in Z_p.
Its cancelling pairs and sums with the axis give exactly R-R avoidance.
For a common class, two positive short coordinates sum to at most p-1.
When their sum is <=t, the first-coordinate equation is q+r=s. When
their sum is >t, the result is a reflected position and the equation is
q+r+s=-1 modulo a. Both cases occur: 1+1=2 and t+t>t. Equations involving
negative positions reduce to these by changing signs and rearranging,
or cancel onto the axis and give Ci-Ci. Two axis positions give condition 1.
This proves necessity and sufficiency, including repeated summands.

The exact criterion permits common-colour permutations and independent
permutations of the special axis classes, since only their union occurs.
The model uses first-occurrence order for these palettes. It imposes no
coordinate normalization E(1)=0 and no asymmetry condition.

## Full middle-third obstruction for every parameter

Write I={q:a<3q<2a}. Suppose a common Ci equals I.

If 3 divides a, global negation symmetry already prevents a valid word:
n/3 and 2n/3 have the same colour and n/3+n/3=2n/3.
If a=3m+2, then I=[m+1,2m+1] contains q=2m+1 and 3q=2a-1.
The triple-sum condition therefore fails.

It remains that a=3m+1. Here I=[m+1,2m] is sum-free, its threefold sum
lies in [a+2,2a-2], and I-I contains every nonzero residue of signed
size at most m-1. Thus colour i cannot appear on axis positions pq
with 1<=q<m. In the integer prefix [1,pm-1], all other positions have
quotient q<m: a lower short position uses q outside I, while a reflected
upper position uses a-1-q>=2m+1, also outside I. Colour i is absent
throughout this prefix. The other five colours must colour it.

Use the established theorem [S(5)=160](https://arxiv.org/abs/1711.08076).
We obtain pm-1<=160. Since a is odd, m is even. For p=5, m<=32 and
a<=97, so n-1<=484. For p=7, m<=22 and a<=67, so n-1<=468.
These are upper bounds for the stated family; no endpoint attainment is
asserted. In particular full middle-third fibres cannot meet the new-bound
target. This argument requires the exact undilated interval; arbitrary
unit dilations cannot be normalized without preserving the carry rule.

## Contained fibres at modulus 545: at most 32 points

Now a=109, p=5, and a common Ci is any subset of I=[37,72]. Its colour
cannot occur off the axis in [1,161]: lower positions use q<=32 outside I,
and upper ones use q>=77 outside I. Since [1,161] cannot be five-coloured,
colour i must occur at 5d for some 1<=d<=32. Therefore d belongs to Ei
and d is absent from Ci-Ci.

For any such d, form the graph on the 36 consecutive points of I with
edges joining points at difference d. Its components are paths in the
residue classes modulo d. A path with ell vertices has independence
number ceil(ell/2). Hence the maximum size of a subset avoiding difference
d is

    alpha(36,d) = sum over r=0,...,d-1 of
                  ceil((1+floor((35-r)/d))/2).

For d=1,...,32 the values are

    18,18,18,20,20,18,21,20,18,20,22,24,23,22,21,20,
    19,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32.

Thus |Ci|<=32. Equality is possible for this necessary constraint only
at d=32. The difference graph then has four edges

    {37,69}, {38,70}, {39,71}, {40,72}

and 28 isolated vertices. Every maximum independent set keeps all isolated
vertices and one endpoint of each edge. These are exactly 16 supports.
Each has every difference 1,...,31 and omits 32, so necessarily 32 belongs
to Ei. This characterizes the capacity boundary, not its Schur feasibility.

## Audits, complete controls, and unresolved computation

The theorem above is an elementary argument using the external S(5)=160
theorem. This package does not recheck that theorem's large proof.
No new UNSAT result or unchecked solver status is used as evidence.

`audit.py` fills symbolic cells from the lower short positions and their
reflections, independently projects every literal modular equation, and
compares exact clause sets with the criterion encoder. It runs at five
parameter pairs. Target counts are 144722 pairs / 32487 distinct Schur
clauses at modulus 539, and 147968 / 73148 at modulus 545. All 9216
complete assignments at a=5,p=7 are checked against literal sums;
258 are valid and each admits both palette normalizations. Every normalized
image is checked as a full word. The prefix audit checks explicit omitted
colour positions. A separate bitset enumeration checks all 58905 size-32
subsets of I and recovers exactly the 16 supports above.

`controls.json` supplies four complete valid words through 34,64,234,304.
The endpoint-304 word has p=5,a=61,C2=[21,40], first occurrence of colour2
at position100, and class sizes 44,42,100,38,40,40. The endpoint-64 control
uses a different saturated axis support. `verify.py` imports no encoder or
solver; it checks the full rule, criterion, every modular and integer sum,
and the printed interval properties. These are calibration examples only.

The full-family targets 539 and 545 remained UNKNOWN at 100000-conflict
budgets (the 539 run used 100001 conflicts). Both full-I target branches
also returned UNKNOWN before the elementary prefix obstruction was found.
All 16 size-32 boundary cases remained UNKNOWN at approximately 10000
conflicts each. A shared prefix relaxation through161 remained UNKNOWN at
100000 conflicts. None supplies a negative certificate or a full witness.
The unrestricted target models in model.py remain open. See expected.json
for compact records; exploratory logs are not part of this publication.
These exploratory runs used CPython 3.12.14, python-sat 1.9.dev15 and its
CaDiCaL 1.9.5 backend, in one process with default solver settings.

## Reproduce and scope

Only Python 3.11 or later and its standard library are required:

    sha256sum -c SHA256SUMS
    python3 -B verify.py
    python3 -B audit.py
    python3 -B model.py /tmp/shifted545.cnf
    python3 -B model.py /tmp/shifted539.cnf --axis-factor 77 --short-factor 7

The verifiers print PASS and reproduce expected.json. The generated target
CNFs are exact search models; neither is supplied with an UNSAT claim.
The external theorem, mathematical criterion and prefix arguments, sound
palette normalization, and literal audits are the trust boundary. These
checks are not separate peer review. No historical-priority claim is made
for the criterion, prefix obstruction, or path independence calculation.

The [2026 shifted S-template paper](https://arxiv.org/html/2607.15034v1)
also tracks addition carries but uses a different expansion rule, with
shifted references to a base colouring. It still uses S(6)>=536. This
work neither changes that bound nor re-creates the old 536 construction.
