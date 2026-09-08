# Complete exclusion of the h3931 equality-core extension family

**No good graph can properly contain an induced C5[C5].** In particular,
every 43-vertex graph containing this 25-vertex core has a monochromatic
five-set, regardless of the other 603 edges. No symmetry is imposed on
the 43-vertex graph.

This closes the complete h3931 equality branch: its accepted classification
identifies C5[C5] as the unique good25 graph with no induced P5 or its
complement. Consequently every 25-set in a hypothetical good43 contains
one of those patterns. This is a complete physical-family exclusion, not
a construction of good43 or a new lower bound for R(5,5).

The proof is elementary. Every outside vertex marks each inner pentagon
red or blue, or both. Avoiding K5 would make the red-marked outer blocks
independent and the blue-marked blocks a clique. Each has size at most two,
so their union cannot cover all five blocks. [PROOF.md](PROOF.md) gives the
full argument, the h3931 bridge, the family scope and trust boundaries.

The [exact certificate](CERTIFICATE.json) covers every outside attachment
through 32 inner words and 243 disjoint outer tag classes. The separate
checker verifies 27,015 literal selected two-block cases and every one of
the core's 53,130 five-sets. For a fixed ordered core, the complete excluded
43-vertex family has exactly 2^603 labeled graphs. Counts are not multiplied
by embeddings, combined with h3887, or interpreted as solver speedups.

From the repository root, CPython 3.11 or later, standard library only:

```sh
python3 -B ramsey_r55_pentagon_product_extension_obstruction/reproduce.py
```

Expected status: `REPRODUCED_COMPLETE_PENTAGON_PRODUCT_EXTENSION_EXCLUSION`.
The replay verifies all source hashes and checks normal and assertion-disabled
outputs. It downloads nothing, imports no upstream implementation, and
makes no solver call.

For a full graph and a supplied 25-set, the [physical interface](interface.py)
recognizes this particular core and returns a literal monochromatic five-set.
The [independent verifier](verify_certificate.py) checks only the ten
physical pairs and graph binding:

```sh
python3 -B ramsey_r55_pentagon_product_extension_obstruction/interface.py \
  ramsey_r55_pentagon_product_extension_obstruction/FIXTURE.json
python3 -B ramsey_r55_pentagon_product_extension_obstruction/verify_certificate.py \
  ramsey_r55_pentagon_product_extension_obstruction/FIXTURE.json \
  ramsey_r55_pentagon_product_extension_obstruction/EXAMPLE_CERTIFICATE.json
```

`FIXTURE.json` is a deliberately rejected complete graph, not a Ramsey
candidate. A subset outside this specific core family receives no Ramsey
verdict. [BRIDGE_CONTROL.json](BRIDGE_CONTROL.json) records a full physical
example where the 26-set has a P5 but the new extension obstruction still
supplies a K5.

The extension theorem is self-contained. Its interpretation as the entire
h3931 equality branch imports the accepted equality classification at
h3931/h3935; exact pins are in [DEPENDENCIES.json](DEPENDENCIES.json).
No historical novelty or external review of this new package is claimed.
All 2,189,178 h3887 tasks remain undecided; none is declared closed solely
from this induced-core exclusion. [HANDOFF.md](HANDOFF.md) records the
receiving interface and the stopping boundary.
