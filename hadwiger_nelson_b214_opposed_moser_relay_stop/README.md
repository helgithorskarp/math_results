# Exact stop for one B214–opposed-Moser relay

The fixed complete unit-distance graph below has **217 distinct plane
points, 985 edges, and chromatic number four**. Its proposed second marked
centre is isolated. A saved complete B214 colouring extends, and the two
marked centres admit both equal and different colours. The intended
forced-equality relay therefore fails. This is one construction stop, not a
five-chromatic graph, record improvement or complete B214 relation census.

## Frozen geometry and the missing-terminal diagnosis

Let B be the 214 exact points in `source214.tsv`, in the native Parts frame.
A row `(a,b,c,d)` denotes

```
(a + b sqrt(33) + i(c sqrt(3)+d sqrt(11)))/12.
```

Put

```
rho=(1+i sqrt(3))/2, t=(5+i sqrt(11))/6,
M=(0,1,rho,1+rho,t,t*rho,t*(1+rho)),
C=i sqrt(3)/2, O=0,
U=M union (-conjugate(M)) union (B+C),
X=U union {C}.
```

The two B214 marked tips `+/-3/2+C` coincide with the opposed Moser outer
tips, so their distance-three incidence is exact. The opposed Moser input
has 13 points and 23 complete unit edges, and admits equal colours at those
tips. B214's published unequal-tip semantics motivated the attempted relay;
that imported negative theorem is not used in the stopping proof.

Exact merging gives **216 points and 985 edges in U**. Eleven of the 13
opposed Moser points already lie in B+C; only two new points remain. The
full graph has two unit contacts beyond the inherited B214 and opposed-Moser
edge sets. Their labels, with B214 first, are `(58,214)` and `(61,215)`.

The original selection mistakenly treated the geometric centre C as a B214
vertex. Reconstruction catches that it is absent from U. Checking the
intended terminal explicitly gives **zero unit neighbours in U**. Thus X
has 217 points, the same 985 edges, and components of orders 216 and 1.
Adjoining C records the omitted marked point; it is not a new driver or a
second construction search. No alternative centre or placement was tried.

The raw bound must correspondingly be 226 rather than 225: the 13-point
opposed input and B214 have the two prescribed tip overlaps, and C costs
one more point. Actual merging is stronger, but does not repair the force.

## Colouring and failed finite completion

The certificate supplies one complete B214 four-colouring, in its native
index order. Its colours on the old neighbours of the two new vertices are

```
N(214) = [5,58,89,110], colours [1,1,2,2];
N(215) = [2,61,89,113], colours [3,2,2,0].
```

Giving vertices 214,215 colours 0,1 extends that same full input. The
isolated C can independently take any colour. Two literal whole four-words
therefore witness equality and inequality of O,C. A separate proper word
uses all five colours, but proves no five-chromatic lower bound. The retained
seven-point Moser spindle has no three-colouring, verified by exhaustive
`3^7` enumeration, so the ordinary chromatic number is exactly four.

The proposed route was explicit: if a half forced O=C, their distance
`sqrt(3)/2` would permit a second copy rotated about O by
`(1+2i sqrt(2))/3`. Its two C images would be unit apart, contradicting their
forced common colour. The corrected raw two-half bound would be 451; the
actual marked half would give at most 433 before other collisions. Neither
count is a construction because the needed equality is false. The two-copy
physical graph was not built or classified; incidental contacts in that
unconstructed graph are outside this result. Every subgraph of X retaining
O,C inherits a witness against their forced equality.

This package does **not** assert that every complete B214 input extends,
that another pair is neutral, or that every relay between forcing gadgets
fails. It stops the one selected frame, full-input word and centre pair.
No source-word, pole, phase, host, copy-count or deletion sweep follows.

## Reproduce

From the repository root, with CPython 3.11+ and no extra dependency:

```sh
python3 -B hadwiger_nelson_b214_opposed_moser_relay_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_b214_opposed_moser_relay_stop/verify.py --check-expected
python3 -B hadwiger_nelson_b214_opposed_moser_relay_stop/controls.py
(cd hadwiger_nelson_b214_opposed_moser_relay_stop && sha256sum -c SHA256SUMS)
```

The verifier constructs both Cartesian coordinates over
`Q(sqrt(3),sqrt(11))`, derives M from its formula, merges all equal points and
checks all 23,436 unordered pairs. The controls independently specialize the
complex-coordinate norm and compare every squared norm and unit edge; four
semantic corruptions are rejected. These are author-side checks, not an
independent review. Final replay uses no SAT result or floating-point test.
See [PROVENANCE.md](PROVENANCE.md) for inputs and the single discovery query.
