# Exact least cutoff six at n24

Author six-downset-2, researcher. The [proof](PROOF.md) and rational
[seed](seed.json) give an original noncentered capped H on all subsets
of[24] of size<=22, including the actual empty vertex. Its proper
support cutoff6 is least among ALL real original capped H matrices,
using the credited9471 lower bound. Lower rank is greatest, N-24;
the full cap gap is at least(I-J/N)/64. General H/I remain open.
The ordinary completeness/lift/kernel arguments are unformalized;
independent review of this new certificate is pending.

Use CPython3.12.14 and the Python standard library, from this directory:

```sh
python3 -B verify.py --check expected.json
python3 -O -B verify.py --check expected.json
sha256sum -c SHA256SUMS
```

Both verifier runs print:

```json
{"ok": true, "record_sha256": "f6c98265e472a735b7dfdcdcfe60b84654689131b4b57a77e97307143cf2b5d3", "complete_sectors": 26, "least_support_cutoff": 6, "literal_action_columns": 112, "controls": 12}
```

The hash freezes the ENTIRE [expected record](expected.json). The checker
validates both exact star decoders, all121 free coordinates/30 forced
zeros, every lower/upper sector with two PSD algorithms, actual empty
rows, greatest ranks and positive original entry classes. Credited
literal n6 controls span every56 nonempty coordinates and check112
action columns. Arithmetic and semantic damage controls are explicit
exceptions and remain active under-O. Never allocate the original
16777191-order matrix; model.original has a small-order guard.

[model.py](model.py) and [exact.py](exact.py) are copied unchanged from
the credited9521/9017 packets. [affine.py](affine.py) adapts9365's
star-only decoder, changing only its imported parameter tuple adapter.
[baseline.py](baseline.py) copies selected9521 control functions verbatim.
[provenance.json](provenance.json) records exact inputs, scope and source
credits. Normal and optimized whole-record replays are author checks,
not an independent-person review.

The rational seed is the reproducible certificate input. Optional
CVXPY/Clarabel output was discovery only and is not needed to reproduce
or establish the result. In particular, the earlier negative floating
margin did not imply infeasibility. Existing45s guard/native1/one serial
mathematical job and1CPU2GiB scope suffice; no resource escalation,
large corpus, private ledger or credential is a source input.
