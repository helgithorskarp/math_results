# Every good43 is maximally vertex-connected in both colors

This computer-assisted theorem excludes the complete global family of
43-vertex Ramsey colorings with vertex connectivity smaller than minimum
degree in either color. Thus a hypothetical good43 satisfies
**kappa(G) = delta(G)** and **kappa(complement(G)) = delta(complement(G))**.
No symmetry or fixed component graph is assumed.

The [proof](PROOF.md) combines degree bounds with a capacity cover of
all vertices of a hypothetical separator. Its 14 possible component-order
cases are all excluded. The new finite lemma is regenerated from the
empty graph, without an external catalog-completeness premise.

The package also supplies a [literal good23](UNEXTENDABLE_CORE.json)
that has **no good24 extension**, hence no good43 completion with twenty
additional unrestricted vertices. A direct checker verifies the core and
all 2^23 new-vertex stars by a product of exhaustive side certificates.
This is a complete decision for that induced-core family, not a target.

## Reproduce

From the repository root, with Python 3.11 and GCC 12 available:

```sh
python3 -B ramsey_r55_maximal_vertex_connectivity/reproduce.py
```

Only the Python standard library and a C++17 compiler are required. The
command verifies the source manifests, replays the complete pinned
[separator18 prerequisite](../ramsey_r55_separator18_classification),
regenerates the marked graphs in normal and `-O` Python modes, and checks
every physical graph and certificate using independent enumeration and
dense verification. It compiles and runs both release and full address/
undefined-behavior-sanitized native enumerations. Outputs and binaries
are placed in a temporary directory and removed on success or failure.
Any mismatch, incomplete run, malformed input, or nonzero exit fails
the replay. See [PROVENANCE.md](PROVENANCE.md) for bounds and commands.

Compact expected results:

- [SUMMARY.json](SUMMARY.json): all 39 complete marked jobs, core orbit
  representatives, beta histograms, and per-job witness hashes;
- [AUDIT.json](AUDIT.json): 34,294 labeled cores and 46,911 marked graphs
  checked entry by entry; 1,896 triangle-cover certificates; all 14
  global order cases excluded;
- [CORE-AUDIT.json](CORE-AUDIT.json): 33,649 literal five-set checks and
  9,216 side-word certificates covering 8,388,608 joint stars;
- [CONTROLS.json](CONTROLS.json): algebraic identities, boundary checks,
  and rejection of invalid physical cores and cut inputs.

## Use in complete physical searches

[HANDOFF.md](HANDOFF.md) states the degree-guarded cut implication and
the interface contract. `guarded_cut.py` produces symbolic clauses with
physical edge labels. A consumer must encode or establish the degree
predicates; no solver numbering or new solver result is supplied.

This is an exact computer-assisted theorem with an unformalized
structural proof, not an external review or proof-assistant certificate.
It imports R(4,5) <= 25 and the pinned separator18 theorem. No priority
claim is made. **All 2,189,178 packing tasks remain undecided; no good43
or improved Ramsey lower bound is established.** The h3887 carrier and
immutable handoff remain unchanged.
