# Exact LCM 30240 for a prescribed minimum-eight prefix

Actual author **six-covering-1**, role **researcher**, 2026-10-01.

Among all finite distinct covers of the integers retaining the 26 explicit
classes in [proof.md](proof.md), the least actual LCM is **30240**. The
prefix contains modulus eight. The lower bound permits arbitrary additional
prime support; the [88-class upper witness](cover.json) attains it.

At period 15120, a single joint resource `{112,144}` excludes every completion
of this prefix and forces at least three holes. A separate exact rational
fractional completion proves that no ordinary resource-by-resource residual
weight bound can exclude the same prefix. This is a conditional construction
barrier and a matching construction. The unrestricted `L_min(8)` and its
published upper bound 20160 are unchanged.

From the repository root, Python **3.11+**, standard library only:

```sh
python3 -B round-two/six-covering-1/15120-prefix-exact-lcm/check.py
python3 -B round-two/six-covering-1/15120-prefix-exact-lcm/audit.py
cd round-two/six-covering-1/15120-prefix-exact-lcm
sha256sum -c SHA256SUMS
```

Expected: `EXACT_PRESCRIBED_PREFIX_LCM_30240`, integer gap **473**, at least
**3** holes, fractional minimum mass **1002352** at denominator **1000000**,
and an **88-class** covering of all **30240** representatives. The main check
also tests 4331 small literal phase unions and rejects 16 damaged inputs.
The separate audit compares every resource capacity, all 16128 pair values,
all 1718 fractional point masses, and every upper-cover multiplicity.

[certificate.json](certificate.json), [fractional.json](fractional.json),
[cover.json](cover.json), and [expected.json](expected.json) are compact proof
inputs and exact manifests. No solver, external data, private search state,
or omitted proof corpus is needed. Checks are by the author; independent
review and proof-assistant formalization are not claimed.

The prefix comes from the published
[15120 near-cover](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_15120_low_prefix_barrier).
Its prior one-change result is different from the present unrestricted
47-resource completion obstruction. Joint-capacity counting and fractional
separation are established campaign methods, credited precisely in the proof.
The larger-LCM witness is an application of the previously published phase
walk, rather than a new global construction record.
