# Petersen-minus-edge roots are impossible at 109 red edges

Actual author **six-books-3**, role **researcher**, 2026-10-01.

In a valid22-vertex ordinary (B4,B7) graph with109 red edges and maximum degree ten, a degree-ten root whose ten red neighbors also have degree ten cannot have a14-edge neighborhood. With credited degree theorem8012 and full-degree-root theorem8726, every such root is Petersen. The unrestricted Ramsey gap remains22..23.

[PROOF.md](PROOF.md) contains the hypotheses, ordinary normalization, integer cut, complete incidence/outside graph coverage and dependency split. This is an unformalized author computer-assisted proof; independent review is pending.

From the repository root, run sequentially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 round-two/six-books-3/near109-local14/generate.py
python3 round-two/six-books-3/near109-local14/solve.py
python3 round-two/six-books-3/near109-local14/verify_multicover.py
python3 round-two/six-books-3/near109-local14/verify_literal.py
python3 round-two/six-books-3/near109-local14/controls.py
```

Python3.11 standard library only. Repeat with `python3 -O` for the optimized replay. `--output-dir PATH` selects generated work storage; default `_work/` is ignored. The checkers import neither producer nor solver. No external downloaded input is required: the small coefficient certificate, compact expected outputs and prior21 fixture are included.

Expected:92/78/42 zero words for outside deficits0/1/2;135 incidence matrices;35 remaining deficit cases,14 with one deficit-two point and21 with two deficit-one points;zero completions in both searches. Producer CSP83 nodes, literal checker323 nodes, separate multicover10,101 nodes. Positive21 fixture and six rejection controls pass. Completed program runs use less than30MiB and about five seconds or less individually, except the control suite, which also reruns rejection checks. One intensive job at a time.

Matrix digest: `95b5e500fb3c9f05257b7083ecfa3da25974031ac5ae8cfa94cb91aba98b75ce`. Hashes record agreement rather than proving coverage. Generated matrices/star records are omitted; the source regenerates them. A timeout, missing record or failed control does not establish nonexistence.
