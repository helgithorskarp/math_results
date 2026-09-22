# Normalized counting spectra for all finite groups

For a finite group $G$, let $c(G)$ and $s(G)$ count cyclic subgroups and
all subgroups, including the trivial subgroup. Put
$\eta(G)=c(G)/2^{\omega(|G|)}$ and
$\lambda(G)=s(G)/2^{\omega(|G|)}$.

**Result.** For every $K\ge1$, groups with $\eta(G)\le K$ have bounded
order after their central cyclic Sylow factors are removed. Consequently
the set of pairs $(\eta(G),\lambda(G))$ with $\eta(G)\le K$ is finite.
Both normalized spectra are locally finite on **all finite groups**.

[PROOF.md](PROOF.md) gives the complete argument and explicit bounds.
One intermediate estimate is
$
|G/R(G)|\le \frac{8388608}{15015}\,\eta(G)^4,
$
where $R(G)$ is the solvable radical. The proof then bounds noncentral
normal cyclic Sylow subgroups and uses induction at the largest prime.

This extends the [solvable-group result](../normalized_cyclic_count_finiteness).
Its new steps handle an arbitrary nonsolvable quotient and arbitrary
normal subgroups in the relative counting argument. The smaller prime
bounds in the solvable theorem remain stronger in that setting.
No complete classification or sharp general order bound is claimed.

## Reproduce

Python 3.11 or later; standard library only. From this directory:

~~~
python3 verify.py --expect EXPECTED.json
python3 -O verify.py --expect EXPECTED.json
sha256sum -c SHA256SUMS
~~~

The two runs produce identical JSON and fail if any mathematical
comparison or the expected output differs. Explicit checks also reject
noncoprime scalar extensions, a nonhomomorphic action, a threshold below
one, and an inexact floating-point threshold. Checks remain enabled
under optimized Python.

The compact [expected output](EXPECTED.json) contains:

- 12 explicit group fixtures, including $A_5$, $S_5$, $\mathrm{SL}_2(5)$,
  $\mathrm{GL}_3(2)$, and $\mathbb F_2^4\rtimes A_5$;
- 28 relative normal-subgroup pairs, including 9 with nonsolvable
  distinguished subgroups, 22 solvable-kernel quotients, and 38 relative
  quotient triples;
- 443 cyclic-subgroup instances of the imported Lucchini inequality;
- $C_7\rtimes S_5$ and $C_{49}\rtimes S_5$ with sign action and
  nonsolvable centralizer $A_5$;
- literal cyclic counts for $A_5\times A_5$, $A_5\times C_{49}$, and
  $A_5\times C_7^2$, plus exact arithmetic bound controls.

Element counts are cross-checked against literal sets of powers.
Normal subgroups are enumerated through joins of normal closures;
solvability is decided by derived series, and radicals are obtained
from all solvable normal subgroups of each fixture. Larger product
controls enumerate powers without allocating quadratic product tables.

These are finite controls of the proof mechanisms. The universal proof
is in PROOF.md; it imports Richards's minimum, Amiri's order-divisibility
bijection, and Lucchini's Lemma 1.1(a). [SOURCES.md](SOURCES.md) identifies
the primary sources and distinguishes prior results. The checks do not
prove those inputs, enumerate all bounded cores, or constitute independent
mathematical review or formal verification.
