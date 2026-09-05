# First negative trace: a colouring exclusion and a connected method obstruction

For quadratic unit rotations over `E=Q(i sqrt(3),i sqrt(11))` whose relative
trace has fixed local valuation `-1`, two connected E-source graphs are
four-colourable whenever both centred source cosets are integral. In
particular all placements with a shared vertex are excluded in this stratum.

In the nonintegral branch, the two cross-endpoint valuations differ by one,
and every cross endpoint on the less negative side has the same residue
colour. Permutations of the two source residue colourings glue exactly when
the other boundary omits a colour. [PROOF.md](PROOF.md) proves these statements
at every depth, for arbitrary source sizes and translations in `E(u)`.

The obstruction to extending that colouring procedure is concrete:
`u=(1+i sqrt(15))/4` admits **connected sources of 13 and 7 vertices** whose
four cross edges form a matching and defeat all residue-colour permutations.
The strict 20-vertex, 28-edge graph has a verified three-colouring. This
refutes uniform residue-permutation gluing; it is not a five-chromatic graph
or a closure of the nonintegral stratum.

For the fixed alternative B292/V214 family, a remaining candidate here must
be disjoint and have all four boundary residues on the more negative side.
The small counterexample proves that this necessary filter must be followed
by additional colouring tests. No <=508 five-chromatic graph is established.

## Reproduce

From this directory in a complete repository checkout, use CPython 3.11 or
later with the standard library only:

```sh
python3 local_checks.py > /tmp/hn-first-negative-local.json
cmp expected_local.json /tmp/hn-first-negative-local.json
python3 verify.py > /tmp/hn-first-negative-geometries.json
cmp expected.json /tmp/hn-first-negative-geometries.json
python3 audit.py > /tmp/hn-first-negative-audit.json
cmp expected_audit.json /tmp/hn-first-negative-audit.json
sha256sum -c SHA256SUMS
```

- `local_checks.py` validates the generic scaled identity and exhaustive
  modulo-eight cases: 196,608 integral triples and 110,592 scaled unit
  triples at each of depths 1, 2 and 3. These supplement the uniform proof.
- `verify.py` constructs seven exact geometries and checks every strict
  edge, source connectedness, residue gluing and positive colouring. The
  cases include two expressions of a disjoint 506-vertex placement,
  non-real trace, a common centre, nonintegral depths and the obstruction.
- `audit.py` reconstructs the points with separate source arithmetic and
  computes distances by squaring coordinates in the full real radical
  ring. It matches all 256,183 pair distances, every edge and supplied
  colour. For the two saturation cases it independently tests all 576
  pairs of colour permutations and verifies chromatic number three.

The expected JSON contains explicit source coordinates and colouring for
both 20-vertex witnesses. Other fixtures regenerate from pinned archived
coordinates. The full distance streams are hashed in label-pair order;
no large output is needed. The distance basis is
`1,sqrt(33),sqrt(5),sqrt(165)`. A stream line is
`i,j:a_num/a_den,b_num/b_den,c_num/c_den,d_num/d_den` followed by a newline.
The edge stream consists of sorted physical first-label pairs `i,j\n`.
The common-centre fixture has 14 labels but 13 distinct vertices.

The two independent representations are author checks, not external peer
review or formal proof. Trust includes the accepted base-field embedding,
the unformalized valuation proof, exact coordinate provenance, and ordinary
Python execution. There is no SAT solver, approximate distance test or
unfinished background computation. See PROOF.md for primary references and
precise boundaries. The preceding locally integral trace result remains
unchanged; the whole negative-trace family is not closed here.

The final CPython 3.11.2 replay took approximately 0.899 seconds for local
checks, 5.091 seconds for geometry generation and 5.091 seconds for the
independent audit. Maximum child peak RSS across the serial workflow was
17,904 KiB. All three deterministic output files matched byte for byte.
