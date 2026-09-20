# The complete `a=1` boundary for BHR support `{1,2,11}`

This directory supports the following computer-assisted constructive theorem.

> For all positive integers `b,c`, every admissible multiset
> `{1,2^b,11^c}` has a Hamiltonian-path realization in the cyclically
> labelled complete graph on `b+c+2` vertices.

For this family, admissibility is equivalent to

```text
b+c+2 >= 22, and if 11 divides b+c+2 then b >= 9.
```

This closes the full `a=1` face of the still-open support problem. It does not
settle `a=2` and therefore does not prove the BHR conjecture for all
`{1^a,2^b,11^c}`.

## Five missing even-parity mantles

Earlier transition-closed cap, boundary, and odd-`b` constructions reduce the
`a=1` face to 29 clamped symbolic cells in five residue classes. The five new
safe seeds are:

| `c mod 11` | seed `(a,b,c)` | order | growth cuts `(2,11)` |
|---:|---:|---:|---:|
| 1 | `(1,12,23)` | 37 | `(6,17)` |
| 6 | `(1,10,28)` | 40 | `(27,11)` |
| 7 | `(1,10,29)` | 41 | `(18,29)` |
| 8 | `(1,10,30)` | 42 | `(30,19)` |
| 10 | `(1,14,21)` | 37 | `(34,10)` |

Each displayed path in `certificate.json` is simultaneously 2- and
11-growable at the stated cuts. Its two critical intervals are disjoint, all
edges have length at most `D=11`, and

```text
2D + 2 + 11 = 35 <= order.
```

The safe-margin refinement lemma therefore preserves both transported cuts
and makes the two growth operations commute. A seed `(1,B,C)` realizes every
`(1,B+2q,C+11r)`, `q,r>=0`. The five resulting orthants cover exactly the 29
previous residual cells.

See [PROOF.md](PROOF.md) for the coverage reduction, proof boundary, and
dependency list.

## Reproduction

The proof checks require only CPython 3.11 or later and its standard library:

```bash
python3 verify.py certificate.json --grid 5
python3 independent_check.py certificate.json
python3 audit_coverage.py coverage_data.json certificate.json
python3 -m unittest -v test_verify.py
```

Or run all four with:

```bash
./run_checks.sh
```

Expected highlights:

```text
seeds=5
commuting_squares_checked=180
prior_residual_patterns=29
final_residual_patterns=0
INDEPENDENT_CHECK=PASS
```

`coverage_data.json` is a compact deterministic extraction of five pinned
upstream certificates. `build_coverage_data.py` reproduces it when those
files are supplied; their hashes are enforced by `audit_coverage.py`.

The optional discovery generator uses OR-Tools 9.14.6206:

```bash
python3 -m venv /tmp/bhr-a1-venv
/tmp/bhr-a1-venv/bin/pip install -r requirements.txt
/tmp/bhr-a1-venv/bin/python find_seed.py --counts 1 12 23 --seconds 300
```

With one worker and random seed 1 this reproduces the first stored path and
cuts. CP-SAT is outside the theorem's trust boundary: every stored witness is
checked directly.

## Files

- `certificate.json`: the five explicit paths and growth cuts;
- `verify.py`: definition-level path, growth, safe-margin, and commuting-grid
  checker;
- `independent_check.py`: separate distance/gap implementation checking all
  source squares;
- `coverage_data.json`: compact prior-frontier data with pinned source hashes;
- `audit_coverage.py`: complete 502-cell `a=1` symbolic cover audit;
- `build_coverage_data.py`: deterministic compact-data extractor;
- `find_seed.py`: optional CP-SAT witness generator;
- `test_verify.py`: reference and mutation tests.

## Literature and scope

Chand and Ollis leave `{1,2,11}` as the possible exception in their
three-element classification: [arXiv:2202.07733](https://arxiv.org/abs/2202.07733).
Ağırseven and Ollis retain `a in {1,2}` for odd third length in their
large-order theorem: [arXiv:2402.08736](https://arxiv.org/abs/2402.08736).
Targeted primary-source and exact-parameter searches found no prior complete
`a=1` theorem. This is search-relative evidence, not a historical-priority
claim.
