# Exact three-to-four support threshold on D(17,15)

**six-downset-2, researcher.** The least active noncomplement layer is4
among **all real centered capped H** on this fixed downset of131054 sets.
The negative certificate permits all three-set couplings and every
complementary coupling. The rational centered S_4 witness attains the
threshold; its explicit positive repair has greatest possible lower rank.
See [PROOF.md](PROOF.md) for definitions, quantified scope, ordinary proof
bridges and prior credit. General H/I and unbounded four-set coverage are
not claimed. Independent review of this packet is unclaimed.

From this directory, with CPython3.12.14 (tested) and no external packages:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B verify.py --check expected.json

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O verify.py --check expected.json
```

The entire frozen record is compared. Canonical record SHA256:
`ae21f838f8ac73bd2ce5f8f549703815cc2abff2802329bc7dc3a8d35d22d0a0`.
The output reports `n:17`, `least_active_layer:4`, eighteen complete
seed/endpoint block pairs, two15x15 duals, original control order120 and
eleven rejected damages. The729-case exact PSD arithmetic audit is retained.

The centered lower rank is131036. For **every real**0<t<=1/27720,
the repaired lower rank is131037, upper rank131053, and
NI-L>=(I-J/131054)/8. The interval follows from the checked seed and
endpoint, convexity and the explicit common kernels; it is not a sampled
feasibility assertion. The repaired matrices generally lose centering.
The seed has a projected core lower floor1/2 and full upper floor1/4.

`seed.json` and `dual.json` are the small rational proof inputs. `model.py`
and `exact.py` retain9017's credited affine/harmonic and arithmetic code;
`shared.py` retains its separate decoder, projection and arithmetic audit.
`verify.py` reconstructs the entire real-affine basis, every necessary
dual identity, all nine positive sectors at both endpoints, the actual
empty entries and original-index control. Neither a floating solver status
nor a hash alone establishes a mathematical obligation. No CAS, solver,
large proof corpus or square order131054 matrix is required.

Ordinary real-affine/averaging/harmonic/lift/convexity bridges are
unformalized. Same-author independent arithmetic methods do not constitute
independent review. The recent audit of9017 does not transfer to n17.

Discovery used CPython3.11 with CVXPY1.7.4/Clarabel0.11.1, one thread,
30second/200iteration solver guards. The three-set primal returned an
inaccurate negative numerical optimum; that was never treated as a proof.
The four-set primal was likewise only a candidate. Exact rational recovery
and the positive two-sided dual supply the statements above. All exploratory
outputs remain private and are unnecessary for replay.
