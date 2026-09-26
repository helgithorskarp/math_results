# Three extremal types with two six-point planes

**Theorem.** Every 70-point line-free subset of \(\mathbb F_5^3\) having
two six-point plane sections is affinely equivalent to one of the three
explicit constructions in [seeds.json](seeds.json). The three types have
respectively five, seven, and four six-point planes, so they are distinct.
Every such set has zero coordinate sum and is inclusion-maximal.

**Consequence for the unresolved 71-point decision.** Its seven-point
plane sections would be pairwise disjoint on the selected set. If \(f\)
counts these planes, \(\mu=\sum_{x\in S}x\), and
\(\epsilon=1_{\{\mu\in S\}}\), then
\[
 f+3\epsilon\le4.
\]
This strengthens the previous \(f+3\epsilon\le5\) constraint.
Every 71-point candidate would consequently have at least 43 distinct
70-point deletions with nonzero coordinate sum and no six-point plane.
No 71-point set is constructed or excluded by this contribution;
the exact value remains 70 or 71.

The [proof](PROOF.md) reduces the classification to 7,464 quotient
matrices in 262 affine classes. Exactly seven classes lift, with 48
normalized point sets. All 48 are supplied in [models.json](models.json),
including explicit affine maps from the three seeds. A separate checked
UNSAT proof in every quotient class establishes that no further model
exists. No symmetry is assumed for an unknown set.

## Reproduce

Requirements: Python 3.11+, GCC 12.2 or a compatible C++20 compiler,
the pinned Python-SAT package, and the official DRAT-trim checker.
The tested checker is at upstream commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, without modifications.

From this directory:

```sh
python3 -m pip install -r requirements.txt
git clone https://github.com/marijnheule/drat-trim /tmp/two-six-drat-trim
git -C /tmp/two-six-drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /tmp/two-six-drat-trim
python3 verify.py --out /tmp/two-six-check \
  --drat-trim /tmp/two-six-drat-trim/drat-trim
```

Expected status: `TWO_SIX_EXTREMALS_CLASSIFICATION_VERIFIED`.
[EXPECTED.json](EXPECTED.json) records all stable counts and hashes.
The sorted quotient catalogue has SHA-256
`4659cde5bfafcaec4bfb5b7deec5762fdbcc5d5010f62a87b2952b1848ef1d6c`.
The run checks every positive object from its point list, all affine
certificates, both complete enumerators, all 3,144,000 affine maps in the
orbit audit, and all 262 DRAT proofs.

For the same full run with C++ sanitizers and Python assertions disabled:

```sh
python3 -O verify.py --sanitize --out /tmp/two-six-sanitize \
  --drat-trim /tmp/two-six-drat-trim/drat-trim
```

All mathematical checks remain active under `-O`. UNKNOWN, an extra
SAT model, incomplete coverage, or a failed proof check terminates the
run with an error. The verifier tests rejection of a false proof and
recovery of a deliberately omitted positive model.

Raw traces, formulas, logs, and binaries are generated outside Git.
The release run produced about 55 MB of proof traces; these are omitted
and regenerated. A trace's particular bytes can vary with solver builds.
The theorem uses its successful independent check, not a historical hash.

This is an ordinary computer-assisted proof, not a proof-assistant
formalization. The trust boundary includes the written reduction,
enumeration programs, compiler, formula encoding, and DRAT-trim.
Independent peer review of this new classification is pending.
See [SOURCES.md](SOURCES.md) for dependencies and attribution.
