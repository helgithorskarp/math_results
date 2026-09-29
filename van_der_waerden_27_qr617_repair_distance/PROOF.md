# An exact repair-distance exclusion for the QR-617 construction

Author: **six-vdw-2**, role **researcher**, 2026-09-29.
Status: computer-assisted lemma with a small independently checked transcript.

Let \(p=617\), \(L=6p=3702\), and
\[
D=\{x\in\{0,\ldots,L\}:p\nmid x\},\qquad |D|=3696.
\]
For \(x\in D\), define \(q(x)=0\) if \(x\bmod p\) is a nonzero
quadratic residue, and \(q(x)=1\) otherwise. All coordinates below are zero
based. Translation \(x\mapsto x+1\) gives the usual interval \([1,3704]\).

**Lemma.** If \(c:\{0,\ldots,L+1\}\to\{0,1\}\) has no monochromatic
nonconstant seven-term arithmetic progression, then
\[
29\leq |\{x\in D:c(x)\ne q(x)\}|\leq3667.
\]
The seven values at \(0,p,\ldots,6p\), and the new value at \(L+1\),
are arbitrary. The claim applies to every coloring, without a periodicity
or symmetry hypothesis on \(c\).

## The exact inference rule

Write \(S=\{x\in D:c(x)\ne q(x)\}\). Suppose toward a contradiction
that \(|S|\leq r=28\). A seven-term AP \(A\subseteq D\) is *critical
at* \(v\in A\) when all six points of \(A\setminus\{v\}\) have color
\(1-q(v)\) under \(q\). Then
\[
v\in S\quad\Longrightarrow\quad
S\cap(A\setminus\{v\})\ne\varnothing.\tag{1}
\]
Otherwise changing \(v\) alone within \(A\) makes all seven colors equal.
This argument uses only the prescribed colors on \(D\).

Maintain a set \(U\subseteq D\) known to contain \(S\), initially \(U=D\).
For a critical AP at \(v\in U\), its current *petal* is
\((A\setminus\{v\})\cap U\).

* An empty petal proves \(v\notin S\) by (1).
* If there are \(r\) pairwise disjoint nonempty petals at \(v\), then
  \(v\in S\) requires at least one distinct member of \(S\) in each
  petal, in addition to \(v\) itself. This requires \(|S|\geq r+1\),
  a contradiction. Thus \(v\notin S\).

Either inference permits deleting \(v\) from \(U\). It does not require
enumerating possible sets \(S\) or trusting a search procedure's negative
answer.

## Certificate and full coverage

`certificate.json` lists **1848** records. A record stores a vertex \(v\)
and either one critical AP or 28 critical APs, each encoded as `[start, step]`.
Every record also deletes the reflected vertex \(L-v\), using reflected
APs with start \(L-(a+6d)\) and step \(d\).

The checker verifies both deductions separately against the current \(U\).
It tests every AP's bounds, positive step, absence of exceptional points,
critical colors, and the required petal emptiness or disjointness. It then
deletes both vertices. Reflection of the color table is checked directly;
the unknown coloring and \(S\) need not be reflection invariant.

The checker uses modular exponentiation and Euler's criterion to compute
\(q\). The generator instead constructs the set of squares and searches
intersection graphs of critical APs. The checker imports no generator code,
does not trust its enumerated AP list, and requires complete coverage of
all 3696 vertices. On the supplied transcript it verifies **307** packing
records and **1541** empty-petal records. Consequently \(U=\varnothing\)
and \(S=\varnothing\).

## The new endpoint cannot be colored

Once \(S=\varnothing\), two APs settle the endpoint:

* \(1,618,1235,1852,2469,3086,3703\): the six old points have prescribed
  color 0. Therefore \(c(3703)\ne0\).
* \(3421,3468,3515,3562,3609,3656,3703\): the six old points have
  prescribed color 1. Therefore \(c(3703)\ne1\).

The checker validates these modular colors directly. Neither AP includes
an exceptional old position. This contradiction proves the lower inequality.
Applying the same statement to \(1-c\) gives
\(3696-|S|\geq29\), hence the upper inequality.

## Relation to the published seed and its use in search

Monroe's Table 1 gives the two-color/seven-term lower bound \(>3703\),
and Table 2 gives prime 617. His argument order is progression length first.
The author-hosted Heule certificate has 3702 color characters, prescribing
the QR pattern on positions \(1,\ldots,3702\). It must not be mistaken for
a literal 3703-character file because its trailing newline is a byte.

`verify_baseline.py` checks the QR coloring on \(\{0,\ldots,3702\}\)
with all seven exceptional colors 0, and again with all seven 1. In each
case the only monochromatic seven-term AP is \(0,p,\ldots,6p\).
Any AP monochromatic under an arbitrary exceptional assignment would be
monochromatic under one of these two constant assignments. Thus every
mixed exceptional assignment is valid, giving \(2^7-2=126\) old templates
per color orientation. This is validation of the old construction.

The new exclusion covers all these templates simultaneously, their color
complements, and extensions at either end. For extension at the left, reflect
\(x\mapsto L-x\); nonzero quadratic-residue colors are preserved.

A target-search encoding may add the exact cardinality cut
\[
29\leq\sum_{x\in D}(c(x)\mathbin{\mathrm{xor}}q(x))\leq3667.
\]
Small repairs cannot improve this construction. This restricted exclusion
does not establish a global upper bound or a new lower bound for \(W(2,7)\).

## Evidence and limitations

The 117906-byte transcript has SHA-256
`6ddaaaaed5497f8e2d5f6f9a24263eb1276e11540fc7f545939ab0ccfa36952b`.
The trust boundary is the mathematical induction above, the independently
readable verifier, and exact Python integer/set operations. There is no SAT
solver, floating point, imported proof corpus, or external witness required.
This proof has not been formalized in a proof assistant or independently
peer reviewed.

The same packing-elimination method stalled when trying to exclude 29
changes: 3538 positions remained allowed. This is a limitation of that
proof attempt; it gives no coloring or mathematical exclusion at radius 29.
No minimum-distance equality or priority claim is asserted.
