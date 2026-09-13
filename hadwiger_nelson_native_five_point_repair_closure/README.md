# The native 503-point base cannot be repaired with five host points

**Every graph obtained by adding at most five points of the native contact
host to its fixed 503-point record base is four-colourable.** This resolves
the concrete repair question left open in the
[native contact construction](../hadwiger_nelson_native_contact_repair/README.md).
It supplies no smaller five-chromatic graph and no global Hadwiger–Nelson
vertex bound.

Let A be the archived Parts `v159e646` point set, D its 30 oriented unit
differences, and

```
rho = (7+i sqrt(15))/8
L = A union (A+D)
H = L union rho L.
```

H has 3,919 distinct plane points and 29,125 strict unit edges. Let B be the
503 points shared with the displayed Parts509 realization. Its six missing
zero-based original labels are `25,74,106,107,298,336`. The exact result is

> For every S contained in H minus B with |S| at most five,
> the unit-distance graph on B union S has chromatic number at most four.

At least six additions are therefore necessary **with this base and this
host fixed**. Dropping points of B, using other points of the plane, and
arbitrary subgraphs of H remain outside the theorem. The host itself and
the earlier 1,090-point subset remain five-chromatic.

## Reproduce

From a complete repository checkout, using Python 3.11 and a C++17 compiler:

```sh
python3 -B hadwiger_nelson_native_five_point_repair_closure/verify.py \
  --work /tmp/hn-native-five-verify
```

The expected final status is
`EVERY FIXED-BASE REPAIR WITH AT MOST FIVE HOST POINTS IS FOUR-COLOURABLE`.
No SAT, MILP, computer-algebra package, external service, or solver proof
file is required. The default replay runs both exact transversal checks.
All generated graphs, executables and enumeration files go under `--work`.

An optimized-Python/undefined-behaviour-sanitizer replay is:

```sh
python3 -O -B hadwiger_nelson_native_five_point_repair_closure/verify.py \
  --work /tmp/hn-native-five-ubsan --sanitize --skip-python-cover
```

The omitted Python cover check is already included in the default command.
`controls.py --work /tmp/hn-native-five-controls` checks the enumeration and
cover algorithms against small exhaustive instances and rejects malformed
colourings. `enumerate_esu.cpp` supplies the original connected-set
enumeration; the principal verifier instead uses spanning-tree shapes.

## Certificate and proof mechanism

[certificate.json](certificate.json) contains 126 partial four-colourings
of H. A dot denotes an omitted point. Every word retains B; all retained
unit edges are checked directly. A non-four-colourable repair must include
at least one omitted point from each word.

Relative minimality permits requiring every new point to have degree at
least four in the repaired graph. Exact connected-component enumeration
and the partial colourings dispose of every five-point selection having
a component of size at least three. The remaining selections are built
from 585 eligible singletons and 1,238 adjacent pairs involving a point
with exactly three base neighbours. Their total cost must be at most five.

Two exact computations independently show that no such selection hits all
126 omission sets. The C++ computation separates zero, one and two pairs.
The Python computation uses weighted residual-cover recursion. Neither
uses a SAT solver or floating-point feasibility verdict. See
[PROOF.md](PROOF.md) for coverage, padding and encoding arguments.

The full replay rebuilds all 7,677,321 host point pairs through the pinned
Cartesian radical implementation from the accepted parent package. The
new combinatorial enumeration uses a separate spanning-tree algorithm;
its 18,965 triples and 175,654 quadruples agree entrywise with the original
enumeration. All qualified five-point spanning-tree maps are covered.

The certificate is about 494 KB. It is compact positive evidence, not a
search log. Heuristic colourings were used only to discover its words;
the verifier does not need that heuristic to reproduce the theorem.
[SOURCE_PINS.json](SOURCE_PINS.json) pins the geometry implementation,
coordinate input and parent base specification.

## Construction consequence and limits

This closes an actual candidate construction family that previously had
unresolved 93,061-variable and 11,599-variable selectors. The standard
SAT encoding of the final reduced instance still timed out after 180
seconds; its unfinished 507 MB trace is not a proof and remains local.
The finite exact cover computation supplies the exclusion instead.

A bounded successor probe allowed six new points, aiming to obtain a
509-point non-four-colourable graph and then delete an old point. Ten
actual 509-point candidates were checked four-colourable before another
master timeout. The ten 509-point words and seven new 508-point positive controls are in
[search_controls.json](search_controls.json) and checked by the full replay.
No 509-point five-chromatic signal, six-addition exclusion, or sub-509
improvement follows from that probe.

The next construction needs to change the fixed base or the allowed
geometry. Merely extending the old five-addition search cannot succeed.
This result is author-validated computer-assisted mathematics, awaiting
independent-author review. It is not a proof-assistant formalization or a
claim of a new general graph-colouring method.
