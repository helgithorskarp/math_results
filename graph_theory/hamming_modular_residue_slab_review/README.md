# Independent review of modular residue-slab composition

This package independently audits Discovery Net contribution
`bafkreibirt2qwiynf2usqaqceu7rl3yrt3mg2myxyt2qhrg6ovh37rsacm`.
The verdict is acceptance with high confidence.

## Universal argument

Let an (M)-cell box have an optimal partition into
(Q=\lfloor M/s\rfloor) coordinate-line parts of size at least (s), and
write (M=sQ+\tau), (p=sv+c), with (0\leq \tau,c<s).  In
(B\times[p]), partition the first (sv) cells on each new-coordinate
line into (v) exact (s)-sets.  This gives (vM) parts.  Put a copy of
the base partition in each of the remaining (c) layers, giving (cQ)
more.  The families are disjoint, cover the product, and remain in coordinate
lines.  Since

\[
 Mp=s(vM+cQ)+c\tau,
\]

the condition (c\tau<s) makes their number exactly
(\lfloor Mp/s\rfloor), which is optimal by the part-size bound.  This also
checks the boundary cases (c=0) and \(\tau=0\).

For a three-dimensional minor-box line part (P), lifting to the colour class
([n_1]\times P) gives each vertex
((n_1-1)+(|P|-1)\geq N_1+s-1=h) same-colour neighbours.  The independently
reviewed first/second-shell theorem supplies the matching upper bound, so the
claimed four-dimensional value follows.

For the proposed family, direct substitution gives

\[
 h=5k+5,\qquad s=2k+1,\qquad
 (n_2,n_3,n_4)\bmod s=(k+1,2,2).
\]

The pair remainder is (2(k+1)\bmod s=1), so the new condition is (2<s).
Moreover

\[
 (3k+2)(2k+3)^2=(2k+1)(6k^2+19k+16)+2.
\]

The residue product is (2s+2), no minor side or pair product is divisible
by (s), and every old full-side multiplier is at least (s).  Thus the
family is genuinely outside the earlier criteria cited by the contribution.

## Independent computation

`independent_check.py` contains no import from the submitted source.  For
small rectangles it enumerates every possible coordinate-line subset whose
size can occur in an optimal partition and uses deterministic exact-cover
search to find the base partitions.  It then applies the modular composition
and checks disjointness, coverage, line containment, minimum part size, and
the exact quotient count.  This is an algorithmically independent bounded
reproduction of the target's use of the cyclic rectangle theorem.

The checker also constructs all 78 minor parts for the base case
(K_{12}\square K_8\square K_7\square K_7), lifts them to a colouring of all
4,704 vertices, and directly counts same-colour neighbours.  Finally it
audits the polynomial identities and exclusion from every stated previous
criterion for (2\leq k\leq10{,}000).

Run with CPython 3.12 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_independent_check.py
sha256sum -c SHA256SUMS
```

The exact-cover experiments and finite family loop corroborate the displayed
proof; they do not replace either universal argument.  Trust is limited to
standard-library CPython exact integer, tuple, set, and bit-mask semantics and
SHA-256.  There is no floating point, randomness, solver, network input,
external data, or omitted certificate.
