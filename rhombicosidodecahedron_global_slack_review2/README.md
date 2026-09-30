# Independent global RID gap audit

six-reviewer-2, independent mathematical reviewer, 2026-09-30.

Confirms the original global squared-height slack 1/1200 and expanded 1/450,
and proves the stronger global necessary restriction **f(n)^2 < beta-1/445**.
The global RID non-Rupert conjecture remains open. See [REVIEW.md](REVIEW.md)
for the complete theorem, continuous reductions, exact scope, dependencies,
literature and strengthening opportunities.

From a complete repository checkout, Python 3.11+ standard library:
~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_global_slack_review2/audit.py
~~~
The default inputs are the four sibling reviewer directories. The command
prints every byte of [expected.json](expected.json). Explicit --winning-review,
--threshold-review, --contact-review and --beta-review paths can select the
same pinned public bytes. No runtime network access or target Python import.

Independent evidence: all720height orders, all64,800wall sign comparisons,
both complete8-original source circles and all56pair distances, all1800
expanded support comparisons, all840torque strata and5760direct exact
polynomial identities. Normal and -O outputs are identical; all7unsupported
controls reject. The expanded native checker separately passes all32controls
and byte-matches its expected output. Its replay is supplementary.

[INPUT.json](INPUT.json) pins both target revisions and earlier public reviewer
inputs. [VALIDATION.json](VALIDATION.json) records versions, bounds and resources.
[expected.json](expected.json) SHA256: 44668892fbec6c8ff78a12db998d6806e640563d2dca9ee06532695c3957afbe.

No original full436region enumeration or previous beta1/480cap computation
is claimed rerun. No large proof corpus, credential, private ledger, solver,
floating-point proof predicate or formal proof assistant is used.
