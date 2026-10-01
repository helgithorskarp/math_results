# A depth obstruction for normal profiles on hat ports

Actual agent **six-heesch-3**, role **researcher**, round two, 2026-10-01.

Every aligned hat reference patch with three complete surrounds forces all
14 full-port normal functions to vanish. Two surrounds already suffice if
the final reference union is a topological disk. The corresponding depths
are sharp for the port equations: an eight-hat disk first surround and a
23-hat hollow second surround admit an explicit nonzero polynomial profile.

The hypotheses retain the reference port incidences and endpoint order.
General motions of deformed tiles, partial-port matches, and universal
endpoint rigidity remain outside this result. The finite-seven target is
still open. This is a construction-route obstruction, with no Heesch record
or exact finite Heesch number asserted.

[proof.md](proof.md) gives the geometric definitions, completeness argument
and function-valued odd-walk proof. [check.py](check.py) independently
regenerates the finite search using two implementations. It permits holes
in every partial patch. It requires no primary atlas, solver, external
package or network access.

| Exact search stage | Result |
|---|---:|
| All grid-aligned touching neighbours | 58 |
| Complete first surrounds | 414 |
| First surrounds with bipartite lifted components | 112 |
| Their complete second surrounds | 1305 |
| Second surrounds still having bipartite components | 4 |
| Those four extendible to a third surround or a disk | 0 |

Each exception contains sealed single-kite gaps. The four fixtures are in
[exceptions.json](exceptions.json); the checker regenerates them and
verifies that every possible aligned hat covering such a gap overlaps the
fixed patch. No intermediate topology test is used to establish exhaustion.

From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B round-two/six-heesch-3/hat_corona_profiles/check.py --expected
```

CPython 3.11.2, standard library. About three seconds and 24 MiB on one CPU.
The output must equal [expected.json](expected.json). Expected hashes cover
all generated first surrounds, all examined second surrounds, and the four
exception fixtures. Five malformed controls reject. No large enumeration
dump is published or needed.

The primary geometry and aligned-tiling context come from Smith, Myers,
Kaplan and Goodman-Strauss, [An aperiodic monotile](https://arxiv.org/html/2303.10798v3),
and their [hatvalidate source](https://github.com/isohedral/hatvalidate),
commit `38f59ed540d4075f213e98abbadb6bc01d2a64a8`. Their tilability and atlas
are prior art. This search starts with all 58 neighbours and does not import
their pruned neighbour lists or precomputed two-surround data.

The earlier [25-hat result](../hat_patch_rigidity/proof.md) treats one fixed
network, including its endpoint Jacobian. This result answers the next
profile question uniformly across the indicated reference coronas. Its
proof restates the pairing argument and imports no sibling executable.
No independent review verdict is assumed.
