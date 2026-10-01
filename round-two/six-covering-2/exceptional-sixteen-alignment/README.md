# A necessary sixteen-phase in the exceptional period 10080 case

Actual author: **six-covering-2, researcher**. For any distinct cover with
minimum modulus **exactly 8** and every modulus dividing 10080, suppose the actual 12-class
has eight parity and no present modulus 10 opposes eight parity. Then16 is PRESENT and
its phase difference from 8 is **4 modulo 8**. Such an exception exists exactly
when the fixed six-class root ((8,0),(9,0),(10,0),(14,1),(12,10),(16,4))
has a covering completion. That root remains **OPEN**.

This sharpens the published exceptional-phase-alignment lemma 8837. It
excludes the two added sixteen-phases1/2 by complete ordinary trees; actual
odd/valuation-one phases are reduced by checked affine units. The public
five-class frontier remains14forms; global L_min(8) candidates 10080,15120,20160
are unchanged. No covering or numerical improvement is asserted.

From a checkout of this repository, install the parent's pinned discovery
requirements only if generating trees. Generation used Python 3.12.14,
NumPy 2.4.6 and SciPy 1.17.1. Numerical threads must be1; run sequentially.

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
      python3 -B round-two/six-covering-2/exceptional-sixteen-alignment/reproduce.py \
      --generate --generated /tmp/covering-sixteen-trees --require-manifest

After generation, the same command without --generate uses Python>=3.10
standard library only. The two bulky trees are omitted; no private input is
needed to regenerate them. Each generation job has unchanged180s/700new-node
allowances. Sixteen jobs per root is a voluntary wrapper allowance; if it is
exhausted, the wrapper reportsINCOMPLETE and asserts no exclusion. Discovery
timeouts, statuses and counts are not proof premises. Any complete exact
certificate in the assigned domain can be replayed; --require-manifest also
matches the author's hashes.

Expected replay: author_manifest_match=true;5649nodes/692expansions;15188actual
branch phases/14097transports;2957432pair entries;80640exceptional six-phase
tuples with10080allowed; remaining_root_status=OPEN; five_class_frontier=14.
The wrapper directly checks the two new roots. The intrinsic statement imports
8837(and its credited affine/parity/twelve lemmas); those earlier exclusions
are not independently replayed here. See [proof.md](proof.md), [manifest.json](manifest.json)
and [phase_controls.py](phase_controls.py). Source pins are enforced before
replay. Written proof unformalized; author validation, no reviewer verdict.

The checked [open comparison fixture](application-next.json) supplies 5408
physical residual points, all 59 unused resources and four free top resources.
It is a research input and establishes no completion. Final author wrapper
173.296 s/129704 KiB; all six domain/fixture corruption controls reject.
