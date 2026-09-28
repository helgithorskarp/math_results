# Axis forcing for a full middle-third reflected Schur fibre

**Certified conditional result at modulus 545.** Let I={37,...,72} in
Z109. In any valid reflected-fibre construction, if a common fibre Ci is
exactly kI for a unit k, then its axis class Ei is contained in kI and
contains both 37k and 72k (all coordinates modulo 109).

In particular Ei cannot be empty. This strengthens the
[earlier empty-axis exclusion](../schur6_full_middle_third_545/README.md).
Moreover, if any construction with Ci=kI exists, recolouring some axis
points gives another valid construction with Ei=Ci=kI. Existence in this
remaining case is **unresolved**. There is no new bound for S(6), and no
claim that every valid word already has Ei=Ci.

The equality Ci=kI is essential to the stated scope. The result does not
cover only Ci contained in kI or Ci union (-Ci)=kI, and it does not exclude
arbitrary reflected constructions or arbitrary classical six-colourings.
Repeated summands x=y are included throughout.

## Construction and exact criterion

Let A=Z_a. Symmetric sets E0,...,E5 partition A minus {0}; R,C2,...,C5
partition A with 0 in R. Define six classes on (A x Z5) minus {(0,0)}:

    K0 = E0 x {0} union R x {1} union (-R) x {4},
    K1 = E1 x {0} union R x {2} union (-R) x {3},
    Ki = Ei x {0} union Ci x {1,2} union (-Ci) x {3,4}, i=2,...,5.

The common fibres and R may be asymmetric. The
[criterion](../schur6_reflected_fibres/README.md), with a separate
[independent review](../../schur_s6_reflected_fibres_review1/REVIEW.md), is:
every Ei and every Ci union (-Ci) is sum-free; E0 union E1 avoids R-R;
and Ei avoids Ci-Ci for each common colour. CRT identifies the product
with Z_(5a) when gcd(a,5)=1. A full valid word at a=109 would colour
[1,544], but none is supplied here.

## Two maximal axis supports cover the full-fibre family

The following reduction holds for every odd a>=7 with gcd(a,15)=1. Set
m=floor((a-1)/3), h=(a-1)/2, and I={x:a<3x<2a}. Normalize the distinguished
common fibre to C2=I by a unit automorphism and common-colour relabelling.

Let J=(A minus {0}) minus (I-I). E2 must be a symmetric sum-free subset
of J. If T is a symmetric sum-free subset of J containing E2, we may
enlarge E2 to T and remove the newly recoloured points from all other
axis classes. Every other sum-free and difference-avoidance condition is
preserved under taking subsets. The conditions on R and the Ci do not
change. Thus this recolouring preserves validity. It is a dominance
reduction for existence, not a symmetry of every colouring.

If a=3m+2, then I=[m+1,2m+1], I-I={0} union +/-[1,m], and J=I.
Hence E2 can always be enlarged to I.

If a=3m+1, then I=[m+1,2m], I-I={0} union +/-[1,m-1], and
J=[m,2m+1]. Its signed orbit representatives are m,...,h. An equation
u+v=w among these representatives is impossible since 2m>h. A modular
Schur equation among signed representatives therefore reduces to
u+v+w=a; the sum cannot be 2a since 3h<2a. As each summand is at least m,
the only possibility is {m,m,m+1}. Thus the only forbidden orbit support
is the pair {m,m+1}. The two maximal permitted supports are

    T0 = +/-[m+1,h] = I,
    T1 = +/-([m,h] minus {m+1}).

Every permissible E2 lies in at least one of these sets and can be
enlarged to it. This argument includes E2 empty.

## Certified forcing at a=109

Here m=36 and h=54. The two saturated axis supports have representatives

    T0: 37,38,...,54;
    T1: 36,38,...,54.

The exact model with C2=I and E2=T1 is UNSAT. Its CNF has 720 variables
and 21,923 clauses. A binary DRAT proof was checked by DRAT-trim.

If a valid construction had 37 absent from E2, its E2 would be contained
in T1 and the dominance reduction would give this impossible saturated
case. Therefore 37 and, by symmetry, 72 belong to E2. The forbidden
orbit pair {36,37} excludes 36 and 73. Since all other allowed axis
points already lie in I, we obtain E2 contained in I. Finally enlarge
E2 to I to obtain the stated remaining existence problem. Undoing the
unit automorphism and common-colour permutation proves the claim for
every k and i.

The T0 target returned UNKNOWN after 1,000,000 conflicts. This is not a
nonexistence result. The T1 certificate, together with the dominance
proof, establishes the forcing statement without using the earlier
empty-axis certificate.

## Encoding and checks

Outside I the first fibre has states R,3,4,5 on +/-[1,m], with 0 in R.
The axis now allows all six colours. Auxiliary P(u,c) variables express
Q(u,c) or Q(-u,c), for c=3,4,5. Because 3m<a, the symmetric support
+/-Pc is modular sum-free exactly when Pc is ordinary sum-free. The
CNF also includes every axis Schur constraint, every difference
compatibility, and the unit clauses specifying the saturated E2.

Common labels 3,4,5 are ordered by first occurrence, scanning
Q(u),Q(-u),E(u); the Q entries are skipped for u>m. The first special
axis colour is 0. These clauses lose no construction: the common palette
may be permuted, and E0 and E1 may be exchanged independently on the axis.
No coordinate normalization E(1)=0 and no asymmetry condition is imposed.

`audit.py` independently projects every literal modular equation through
the full-word rule. It checks and eliminates the auxiliary OR definitions
and compares the two clause sets by mutual explicit subsumption, before
palette clauses and saturation units. At a=109 it covers 147,968 pairs,
including doublings: 27,935 projected clauses and 27,827 expanded reduced
clauses, with 108 redundant projected clauses explicitly subsumed. The
audit also runs at a=7 and 47.

At a=7 every one of 55,296 complete assignments is checked against literal
sums; 5,760 are valid and all have a palette-normalized representative.
A separate literal test checks all 8,748 allowed saturation images of
these valid words. The axis-cover audit reconstructs J and its Schur
equations independently and checks all 524,288 subsets of the 19 allowed
axis orbits at a=109; precisely 393,216 are valid and all are covered by
T0 or T1. These are transcription checks; the all-parameter dominance
argument is the proof above.

`controls.json` contains complete valid words through 34, 234 and 304.
The 34-point word uses the T1 branch at a=7, showing that its exclusion
is specific to the target modulus. The two 234-point words are before
and after saturating an empty axis class to I. The 304-point word has
E2=C2=I at a=61, with class sizes 36,36,100,42,42,48.
`verify.py` imports no encoder or SAT solver and checks all ordinary and
modular sums, the full reflected rule, support properties, and the exact
recolouring between the paired controls. These are calibration words,
not record Schur partitions.

## Reproduce and trust boundary

Use standard-library Python 3.11 or later. From this directory:

    sha256sum -c SHA256SUMS
    python3 -B verify.py
    python3 -B audit.py
    python3 -B model.py /tmp/schur-axis545.cnf

The Python verifiers print PASS and the reports in expected.json. The
generated target CNF has 411,114 bytes and SHA-256

    aad9f09ccc92f42fd7a0b7b5c843f6db08efac92a5c612edd401cdac9d256686

The unresolved T0 model can be generated with `model.py --branch 0`.

Build [CaDiCaL](https://github.com/arminbiere/cadical) 1.9.5 at commit
`146207318796f094dcded87349a64f0c6927309e` and
[DRAT-trim](https://github.com/marijnheule/drat-trim) at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, using their build instructions.
Then run

    python3 -B prove.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim

This requires CaDiCaL exit 20 with UNSAT and DRAT-trim exit 0 with VERIFIED.
The reference proof has 57,503,666 bytes and SHA-256

    25057d902fe6ac8e6aa802c632b73e13978ea908a3918c25f9bfc436c435eab5

Generation and checking took about 59 and 71 seconds respectively;
runtime varies. A different proof hash is acceptable if the audited CNF
is unchanged and the proof checker verifies it. The bulky proof is kept
in the research workspace and regenerated by this source, not uploaded.
The runner uses temporary storage and removes its outputs afterward.

The mathematical trust boundary is the criterion, the dominance and
palette arguments, the literal clause audit, and the independent proof
checker. A solver status or matching hash alone is not a proof. The new
forcing result has not yet received a separate peer review.

The classical reference bound remains S(6)>=536, from
[Fredricksen and Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
and also used by the [July 2026 template paper](https://arxiv.org/abs/2607.15034).
No historical-priority claim is made for the elementary saturation argument.
