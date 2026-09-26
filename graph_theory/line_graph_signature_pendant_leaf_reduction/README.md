# Pendant-tree optimization reduces exactly to leaf subsets

For every fixed connected host `H`, the maximum line-graph signature over
all pendant-forest attachments is attained by attaching at most one leaf
per host vertex. The proof gives a local replacement rule valid even when
the host matrix is singular. This replaces infinitely many rooted-tree
states by two choices for maximizing this objective.

Read [PROOF.md](PROOF.md) for the theorem, antecedent invariant, complete
proof, and limitations. The sharp cyclomatic conjecture remains open.

Reproduce the compact exact author audit with Python 3.11 or later,
standard library only:

```sh
python3 verify.py > /tmp/pendant-leaf-audit.json
diff -u EXPECTED_OUTPUT.json /tmp/pendant-leaf-audit.json
sha256sum -c SHA256SUMS
```

No catalogue or generated dataset is required. The numerical kernel
search that motivated this work is not evidence for the theorem and is
not part of the package. See [SOURCES.md](SOURCES.md) for graph dependencies
and the limited literature search.

Validated on CPython 3.11.2 in 7.02 seconds, peak resident memory 16.6 MiB.
The expected record audits 3,047 rooted trees, 1,205 forests through nine
vertices, 102,778 local inequalities including 231 singular host matrices,
all 646 leaf subsets of the 44 connected labelled hosts through four
vertices, and 180 simultaneous forest attachments. Characteristic-polynomial
counts check 200 rooted matrices and 90 further literal line graphs.
The printed `record_sha256` hashes the canonical JSON record before that
hash field is added; `SHA256SUMS` separately checks the package files.
