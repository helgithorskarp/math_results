# Independent two-load H audit

Actual agent **six-reviewer-1**, role **independent mathematical reviewer**.
[REVIEW.md](REVIEW.md) confirms LEMMA9153's new k>=2,r>=1,n>=k+r,D>t>=1 scope, including all physical sectors, the actual empty vector, universally greatest lower rank N-k and a full upper cap. It proves the stated sharper trace repair. One-heavy imported results remain context outside this verdict. General H/I and optimal repair are not claimed.

Tested with CPython **3.12.14**, SymPy **1.14.0**, mpmath **1.3.0**. Install [requirements.txt](requirements.txt) in a dedicated environment using Python3.11+. All public mathematical input is compact source and [EXPECTED.json](EXPECTED.json); there is no downloaded polynomial certificate corpus or researcher executable dependency.

From this packet's directory, run the following **sequentially**. The generated polynomial cache goes under the working directory's scratch directory; it is not source and must not be committed.

```sh
sha256sum -c SHA256SUMS
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B verify.py --phase algebra
python3 -B verify.py --phase signs
python3 -B verify.py --phase frames
python3 -B verify.py --phase controls
python3 -B verify.py --phase arithmetic
```

Repeat the five commands with `python3 -B -O`. Each phase compares its **whole** regenerated record to the expected fixture. The algebra phase builds all8 rational functions and all16 budget entries before saving a private generated cache; the signs and controls phases require that cache's complete hash/structure to match the algebra fixture. They do not treat the expected fixture as a sign certificate: signs inspect every coefficient and verify the complete inverse shift. No phase may be skipped when establishing the complete proof. `--cache PATH` and `--expected PATH` provide explicit file locations.

Expected:51 numerator coefficient lemmas/75480 shifted terms, largest coefficient polynomial8500 terms; positive expanded denominators and complete inverse binomial identities; four original-index cases with4573 full-frame entries, seven actual type-permutation generators, exact support/rows/ranks/empty trace and original/improved repairs;64 independent Fraction budget entries and16 signed-permutation minors;16 mathematical damage rejections;2782 native fraction-field arithmetic identities with reduced numerator invariants. All exceptions remain enabled under `-O`.

[algebra.py](algebra.py) and [derive.py](derive.py) reconstruct the uniform rational functions; [signs.py](signs.py) implements a different exact integer binomial engine. [literal.py](literal.py) and [frame.py](frame.py) construct/check the original-domain vectors and every physical frame entry. [controls.py](controls.py) and [arithmetic.py](arithmetic.py) supply independent arithmetic and adversarial checks. [verify.py](verify.py) enforces exact records and phase guards. [SHA256SUMS](SHA256SUMS) fixes the published file set.

All mathematical phases keep **90s** internal guards and **30000 terms per polynomial**, with native threads1 and at most one intensive local job in the existing1CPU/2GiB scope. The independent whole algebra phase is the slowest; a resource guard ending a run means incomplete verification, not a counterexample or nonexistence result. The independent normal/optimized algebra runs took75.56/74.28s; cheap optimized phases took3.77--6.54s. Whole normal/optimized independent records match. An optional native AUTHOR algebra replay reached its own60s guard in multiplication controls before producing a sign certificate and was stopped. No author sign replay success is claimed. After that limit, expensive algebra was paused; downloaded frozen-public cheap phases and all source bytes are checked, with no further frozen-public algebra run claimed. Details are in REVIEW.md. Ordinary Gram/lift/symmetry/completeness/spectral bridges remain unformalized; neither finite cases nor author replay supply uniformity.
