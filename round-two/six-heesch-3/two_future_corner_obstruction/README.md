# Two fixed fourth prefixes have no two further surrounds

Actual author **six-heesch-3**, role **researcher**.

The [proof](PROOF.md) and [compact exact checker](check.py) remove the
private prescribed-mate/registered-grid assumptions from two literal
T7 fourth-prefix obstructions. Arbitrary added rotations, translations
and reflections are permitted. Three original-corner forces use only
ONE future surround; the final60-degree domain exclusion needs TWO.
The210-degree gap has a complete finite motion domain because an edge
would leave30 degrees, below the prototype's minimum60-degree angle.

The prefixes have74 copies/counts[1,6,10,21,36]. The first has an actual
55-copy fifth corona, included in `fixtures.json`. Thus one future
surround is explicitly preserved. Both fixed fourths have no extension
through a sixth. T7's global finite Heesch upper, a seventh-corona lower
construction and the campaign's finite-seven target remain unresolved.
This author-checked computer-assisted lemma is independently unreviewed
and unformalized; no historical priority is asserted.

Tested with CPython3.12.14, standard library only, one process/thread.
From this directory run:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py
```

The checker compares complete evidence with `expected.json`, including
every pinned pose, blocker, pair occurrence and positive-prefix geometry.
Expected counts per case:18,18,48 complete unit suppliers followed by
14 final-gap suppliers;50 odd30-degree candidates retained. Actual
positive corona depths are[6,5]; eight damaged certificates are rejected,
including an omitted odd motion and a missing second-surround license.
Optional `--out PATH` saves full evidence and resource metrics and
refuses to overwrite. Complete evidence SHA256:

    051dc00f54a2196948ebada32ac10c0faa9656b637718a600f0f6e2a9380b5ce

Normal67.389s/29216KiB; optimized44.549s/32636KiB. The two replay processes briefly overlapped; each used one thread and both exited successfully. No parallelism is required by the checker.

`fixtures.json` contains all required finite inputs as compact
rows[a,f,x,y,level]. The T7 five-corona construction and Bašić's
169-copy T6 six-corona control are the already published fixtures from
[source0bc5ae35](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/two_copy_strip_obstruction/README.md).
The second fourth's literal rows are also included. The geometry
reader requires simple disc prefixes, strict nesting and contact of
each new copy with the preceding corona.

`geometry.py` copies the previous exact integer convex-atom/boundary
primitives. `field.py` supplies the same-author Q(sqrt(3)) extension,
with exact rational arithmetic and squared comparisons for sign. These
shared polygon routines and normal/-O agreement are not independent
review or formal proof. The standalone checker does not use the
private search engine, a solver, an enumeration dump, ledger, remote
input or prescribed-mate code. The written completeness reduction
allows arbitrary motions; the algebraic field is a consequence of
matching the listed corners and rays.

The only upper-side external mathematical dependency is the
[uniform two-copy obstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/two_copy_strip_obstruction/PROOF.md),
actual lemma9783, verified source0bc5ae35b48015e64ac07d9ae25e0ba85d26ed7f.
A forbidden pair confined to an uncovered final layer is admissible.
The checker preserves that distinction on the actual fifth.

Primary construction background is
[Bašić2021](https://doi.org/10.1007/s00283-020-10034-w),
[Kaplan2021/2022](https://arxiv.org/abs/2105.09438) and
[the author census/conventions](https://cs.uwaterloo.ca/~csk/heesch/).
No older record theorem is claimed as new, and T7's terminal
half-triangle is not declared an original-grid unmarked polyform.
