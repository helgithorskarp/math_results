# FC(4,9): classification replay and a smaller explicit witness

This package audits Mingchang Liu's September 2026 result **FC(4,9)=16** and
its counterexample to Pulaj–Wood's lexicographic conjecture. It also replaces
the published 138-point negative extension by an explicit **19-point,
242,283-set union-closed family**, with every original point strictly scarce.
All ten added points are abundant.

The independent checks are a direct integer convolution of the entire new
family, a new flow-certificate verifier for the positive lex segment, and an
alternative SAT proof. The unrestricted upper bound is checked by replaying
the author's complete classification; its orbit enumeration has not been
independently reimplemented here. The asymptotic theorem is outside scope.

See [PROOF.md](PROOF.md) for the mathematics and trust boundaries,
[SOURCES.md](SOURCES.md) for attribution, [EXPECTED.json](EXPECTED.json) for
results and artifact hashes, and [VALIDATION.json](VALIDATION.json) for measured runs.

## Small independent checks

From this directory, with Python 3.10 or later:

```sh
python3 witness.py
python3 -m venv /tmp/fc49-audit-venv
/tmp/fc49-audit-venv/bin/pip install -r requirements.txt
/tmp/fc49-audit-venv/bin/python lex_flow.py
```

The first check uses only the standard library. It enumerates all 524,288
possible subsets and verifies closure and frequencies, with negative controls.
Expected size: 242283; original-point imbalances:
`[-5,-5,-5,-5,-31,-31,-55,-49,-49]`.

The second checks 3015 tree nodes, 1508 leaves, and 6,204,558 individual arc
flows. Each leaf has a directly checked flow of at least 1254. These checks
establish the lower bound and the lexicographic counterexample without the
full classification. Neither is a counterexample to Frankl's conjecture.

## Complete upstream classification replay

Keep the external source and generated files outside this publication directory.
Use a C++17-capable GCC and Python with assertions enabled:

```sh
git clone https://github.com/michaeliu4/frankl-complete-four-sets.git /tmp/fc49-upstream
git -C /tmp/fc49-upstream checkout 17002022f9bb033fb6b40e7b5d1484e78ceb0ac2
python3 replay_upstream.py --source /tmp/fc49-upstream --workers 4 --output /tmp/fc49-replay.json
```

The source snapshot has 12,318 tracked files. Expected certificate totals are
4333: 3954 positive, 379 negative. The positive trees contain 26,456,004 nodes.
The eight-point boundary has 52, 13, and 3 types at sizes 9, 10, and 11.

| Final traversal | Visited states | Survivors |
|---|---:|---:|
| All pruning rules | 253611 | 0 |
| Without seven-point pruning | 714494 | 0 |
| Without interim degree pruning | 364570 | 0 |

The driver actually runs all checks and regenerates coverage. It does not
accept a previously saved PASS report as a replacement for execution.

## Alternative SAT certificate

This route needs several minutes and generates about 253 MB of local CNF and
proof files. They are intentionally omitted from the repository. Install the
additional pinned requirements and compile the pinned DRAT-trim source:

```sh
/tmp/fc49-audit-venv/bin/pip install -r requirements-sat.txt
git clone https://github.com/marijnheule/drat-trim.git /tmp/fc49-drat-trim
git -C /tmp/fc49-drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /tmp/fc49-drat-trim drat-trim
/tmp/fc49-audit-venv/bin/python positive_sat.py --output /tmp/fc49-sat --drat-trim /tmp/fc49-drat-trim/drat-trim
```

The 257519-clause formula asks for a union-closed, generator-stable family of
negative weighted share. A verified refutation rules one out. The strict checker
uses actual unit-propagation conflicts, not solver status or an unchecked empty
clause. PB-to-CNF translation remains a library trust boundary for this route;
the separate flow proof does not share it.

The recorded proof hashes identify this run. Different solver or platform
builds may produce different valid traces; successful strict verification,
rather than matching a proof-file hash, is the required outcome.
