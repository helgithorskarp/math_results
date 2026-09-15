# Exact golden-distance lens completion: a 40-point three-colour stop

This package tests one globally coupled, coordinate-producing construction at
the campaign's admission boundary.  Start with the exact 16-point Parts
two-distance configuration.  For each of its 28 pairs at distance
`phi=(1+sqrt(5))/2`, add **both** intersections of the two unit circles centred
at that pair.  The raw accounting is therefore

```
16 + 2*28 = 72 addresses.
```

The construction is frozen at this definition; no phase or radius is a search
parameter.

## Exact outcome

Exact collision merging leaves 40 distinct physical points.  Reconstructing
all pairs gives 92 strict unit edges: 76 distinct prescribed edges and 16
additional contacts.  Despite the heavy merging and extra contacts, the whole
graph has chromatic number exactly three.  `certificate.json` supplies a
proper three-colouring of all 92 edges and the odd cycle

```
0--16--4--5--2--0,
```

which gives the matching lower bound.  The graph is triangle-free.

Thus this complete support fails the required chromatic-coordinate admission
gate.  It is **not** a five-chromatic candidate and is **not** record progress.
Per the declared stop rule, no terminal-relation mining or nearby lens-family
sweep follows from this result.

The scope is only the fixed all-golden-edge, both-lenses completion above.  It
does not classify arbitrary common-neighbour augmentations of the Parts source.

## Exact coordinate model

Let `zeta=exp(2*pi*i/5)` and `q=1/|1-zeta|`.  The stored integer row
`(a,b,c,d)` is the exact physical point

```
q * (a + b*zeta + c*zeta^2 + d*zeta^3).
```

If the golden pair is `(p,r)`, its two added points are

```
p + phi^-1*(-zeta^3)*(r-p),
p + phi^-1*(-zeta^2)*(r-p).
```

The producer uses arithmetic in `Q(zeta)`.  The independent verifier rebuilds
the construction in
`Q(sqrt(5), i*sqrt(10+2*sqrt(5)))`, reconstructs every unit edge, checks every
collision and digest, and checks the upper- and lower-bound witnesses.

## Reproduction

Python 3 and the standard library suffice.

```bash
python3 produce.py
python3 verify.py
```

Expected verifier summary is recorded in `EXPECTED_OUTPUT.txt`.
