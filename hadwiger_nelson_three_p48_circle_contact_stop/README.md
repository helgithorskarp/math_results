# One translated triple-P48 support is four-chromatic

The frozen support below has **505 distinct plane points and 1,375 complete
unit edges**. A literal four-colour word checks on every edge, and an embedded
Moser spindle excludes three colours. Its chromatic number is exactly four.
This is a stopping certificate for one whole physical construction, not a
sub-509 candidate or a classification of translated triangular patches.

The graph is connected and has no articulation vertex. Three 169-point
patches contribute 456 internal edges each. There are two shared points and
seven additional unit edges: six between the first two patches and one
between the second and third. These contacts and the shared points form a
cycle of patch interactions. The complete graph, including all incidental
contacts, was decided directly; no terminal relation was substituted.

## Frozen exact geometry

In complex plane coordinates put

```
omega = (1+i sqrt(3))/2,
P = {a+b omega : a,b integers, a^2+ab+b^2 <= 48},
r = (5+i sqrt(11))/6,
A = 2+omega,  B = r*A,  D = B-A,
v = D*(1+i sqrt(35)/7)/2,
S = P union r*P union (A+v*P).
```

Both r and v have unit norm. The raw budget is 3*169=507; the two collisions
leave 505 physical points. The first two copies share 0; the first and third
share A; the second and third are disjoint. C=A+v has unit distance from B.
All three full underlying lattices have no common point, so the construction
is outside the common-origin P48 theorem and its common-point full-lattice
extension for the displayed lattices. The support is also not centrally
symmetric, excluding any isometric presentation as common-centred P48 copies.

However, a separate **existing field-colouring theorem already covers this
placement**. For E=Q(i sqrt(3),i sqrt(11)), the relative trace of v over E is
D and its squared complex norm is 7/3. Thus this trace is a local unit in the
accepted unramified 2-adic embedding. The
[unit-trace field theorem](../hadwiger_nelson_integral_trace_gluing/PROOF.md)
four-colours all of E(v), which contains S. This coverage was identified
while checking the selected frame. The explicit ordinary four-word supplies
a self-contained finite certificate; that theorem is not a premise of the
finite graph decision. No alternate anchor, circle branch, phase, radius or
copy count was tried after this stop.

## Reproduction

From the repository root, using CPython 3.11 or later and its standard library:

```sh
python3 -B hadwiger_nelson_three_p48_circle_contact_stop/verify.py
python3 -O -B hadwiger_nelson_three_p48_circle_contact_stop/verify.py
python3 -B hadwiger_nelson_three_p48_circle_contact_stop/controls.py
python3 -O -B hadwiger_nelson_three_p48_circle_contact_stop/controls.py
sha256sum -c hadwiger_nelson_three_p48_circle_contact_stop/SHA256SUMS
```

The verifier independently builds Cartesian coordinates using positive
squarefree radicals, merges all collisions, and checks all **127,260** physical
pairs. It imports neither the producer nor its imaginary-generator arithmetic.
`certificate.json` contains the four-word, a proper five-word obtained by
recolouring one vertex, and compact geometry identities. The five-word does
not imply that five colours are necessary. `EXPECTED.json` gives exact output;
nine altered certificates must be rejected. Normal and optimized runs agree.

The optional producer uses Kissat 4.0.4 to find a positive word:

```sh
python3 -B hadwiger_nelson_three_p48_circle_contact_stop/produce.py \
  --work /tmp/hn-three-p48-new-run --kissat /path/to/kissat
```

The work directory must not exist. The one ordinary four-colour query used
60-second / 1,000,000-conflict caps and returned SAT in about 0.04 seconds.
Generated coordinates, CNF, solver log and trace remain outside this compact
package. No solver verdict is trusted by `verify.py`.

The scope is exactly S above. Other translated placements are not classified.
Author-side checks are not independent peer review. The supported unrestricted
record remains [Parts's 509 points and 2,442 edges](https://arxiv.org/abs/2010.12665),
also identified by [Haugland v4](https://arxiv.org/html/2608.04542v4).
