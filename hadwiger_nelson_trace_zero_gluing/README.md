# Four-colouring trace-zero quadratic attachments without a cycle

Let `E=Q(i sqrt(3),i sqrt(11))`. For connected unit-distance source graphs
`P,Q subset E`, every isometric union `P union (u Q+h)` is four-colourable
when `|u|=1`, `u not in E`, `u^2 in E`, and `h in E(u)`. Reflections are
included by conjugating the second source. “Trace zero” means relative
algebraic trace over `E`, not that the rotation has zero real part.

The [proof](PROOF.md) removes the cross-cycle hypothesis from the earlier
[four-cycle gluing result](../hadwiger_nelson_cross_four_cycle_gluing/PROOF.md).
Writing `h=m-u n`, with `m,n in E`, every cross edge satisfies
`N(p-m)+N(q-n)=1`. A local-coset lemma colours all such edges, including
arbitrary negative 2-adic depths. At nonintegral depth, it uses a binary
trace functional and an affine change of the second residue colouring.

This closes an algebraic stratum of the remaining mixed506 forest
interfaces. **General forests, rotations of nonzero relative trace, and
translations outside the stated field remain open.** No five-chromatic
graph with at most 508 vertices is produced. The theorem does not assert
four-colourability of the whole extension field `E(u)`.

## Reproduce

Use Python 3.11 or later, standard library only, from this directory in a
complete repository checkout:

```sh
python3 finite_check.py > /tmp/trace-zero-finite.json
cmp expected_finite.json /tmp/trace-zero-finite.json
python3 examples.py > /tmp/trace-zero-examples.json
cmp expected_examples.json /tmp/trace-zero-examples.json
python3 audit_examples.py > /tmp/trace-zero-audit.json
cmp expected_audit.json /tmp/trace-zero-audit.json
sha256sum -c SHA256SUMS
```

`coloring.py` implements the local residue, arbitrary negative-depth test,
and radial gluing formula. It rejects nonintegral residue requests and
checks that each source occupies one integral coset. It imports the
accepted source-field arithmetic with a hard-coded SHA256 pin.

`finite_check.py` checks all nine nonzero anchor-residue pairs, the 18
prescribed affine colour maps and their 144 allowed cross-residue cases,
plus six integral norm-pair cases. An independent multiplication using
binary polynomials and enumeration of all 24 colour permutations finds
36 compatible maps in total and checks that the prescribed maps occur.
The missing-shift negative control fails at every nonzero anchor pair.

## Exact geometric calibrations

Write `alpha=i sqrt(3)`. The first nine examples choose the anchor pair

```
x0 = (a+b alpha)/den,  y0 = (c+d alpha)/den,
u = (c-d alpha)/sqrt(c*c+3*d*d).
```

The following exact seeds have `N(x0)+N(y0)=1`, and the rotation is outside
`E` with square in `E`:

| Local depth | den | a | b | c | d | Source pairs checked |
|---:|---:|---:|---:|---:|---:|---|
| 0 | 5 | 0 | 2 | 1 | 2 | Two wheels and B292/V214 |
| 1 | 10 | 0 | 1 | 7 | 4 | Two wheels and B292/V214 |
| 2 | 4 | 0 | 1 | 1 | 2 | Two wheels and B292/V214 |
| 3 | 8 | 0 | 1 | 7 | 2 | Two wheels and B292/V214 |
| 4 | 16 | 0 | 3 | 11 | 6 | Two wheels |

For each source pair, translate the first source anchor to `x0` and the
second source anchor to `y0`, then apply `u` to the second source. The
seven-point wheel is the origin and the six unit triangular-lattice
vectors. The mixed gadgets are the unchanged fixed `B292/V214` sources;
a common translation restores the original location of B if desired.

The nine examples have a single cross edge and no overlap. Each wheel
union has 14 vertices and 25 strict edges; each mixed union has 506
vertices and 2,229 strict edges. They calibrate the new colouring branches,
not a difficult chromatic test or an exhaustive placement search. Two
additional wheel controls use the rotation `(1-2 alpha)/sqrt(13)`: a shared
centre gives 13 physical vertices and 24 edges, while a distant second
wheel gives no cross edge, 14 vertices and 24 edges. All eleven source
pairs are connected and all selected cross interfaces are star forests.

`examples.py` determines the complete squared distances in the quadratic
algebra `E[u]`, all strict edges, possible centre identification and proper
colourings from the new formula. `audit_examples.py` imports neither that
generator nor the colouring module. It reconstructs the mixed sources
using the earlier generic real-radical arithmetic and computes distances
by real dot and signed-area formulas for the rotation. Every one of the
**511,697 labelled pair distances**, every edge and every supplied colour
is checked, including the coincident pair in the overlap control. Its
star-component check is distinct from the generator's C4 enumeration.

## Certificate conventions and trust

Points are source-labelled with `P` first and `u Q` second. A common zero
is represented by its first label when strict edges are deduplicated;
its two labelled copies must have the same colour. The complete labelled
distance stream includes the zero-distance pair.

For each example put `N=c*c+3*d*d`. Distances are represented uniquely as
`A+B sqrt(33)+(C+D sqrt(33)) sqrt(N)`, with rational coefficients. Each
hash stream uses ascending `i<j` lines
`i,j:A_n/A_d,B_n/B_d,C_n/C_d,D_n/D_d`, ending in newlines. Strict-edge
streams use ascending physical-label pairs `i,j`, also ending in newlines.
The expected JSON contains every small cross-edge list and complete
colour string. Full distance streams are regenerated, not stored.

The arbitrary-depth colouring, geometric reduction, connectedness bridge
and compatible local-field embedding are unformalized mathematical
arguments. The finite checks and examples do not by themselves prove the
uniform theorem. These are independent author implementations, not
external review. No SAT result, floating-point distance or omitted large
certificate is used. Dependency code, input tables and proof/provenance
documents are pinned in the manifest; the README commands require the
complete checkout and no network access.

The measured CPython 3.11.2 runs took 0.050, 8.564 and 4.221
seconds respectively, with maximum child peak RSS 17,684 KiB across the
serial workflow. All computations begun for this milestone completed.
