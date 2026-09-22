# Nonsolvable equality in the cyclic-subgroup bound

For a finite **nonsolvable** group $G$, let $c(G)$ count its cyclic
subgroups, including the trivial subgroup, and let $\omega(|G|)$
count distinct prime divisors. Then
$$
c(G)=2^{\omega(|G|)+2}
\quad\Longleftrightarrow\quad
G\cong A_5\times C_m,
\qquad m\text{ squarefree},\quad \gcd(m,30)=1.
$$
The choice $m=1$ is included.

[PROOF.md](PROOF.md) proves the classification, a general theorem
transferring a simple-group count bound and its equality cases to
all nonsolvable groups, and an exact formula for the change in cyclic
subgroup count in a coprime elementary abelian extension.

The inequality and these examples are already in
[Das–Dey–Galindo–Sharma, arXiv:2604.08040v2](https://arxiv.org/abs/2604.08040v2).
The addition is the necessity of this list for arbitrary nonsolvable
groups. We import their simple-group estimates and explain precisely
why their comparisons are strict outside $A_5$.
[SOURCES.md](SOURCES.md) records the literature and claim boundary.

The proof is mathematical. The finite checks below are corroboration:
they are not an enumeration of all finite groups or an independent
verification of the imported simple-group theory.

## Reproduce

Requires CPython 3.11 or later, standard library only. Tested with
CPython 3.11.2. A recorded replay took 3.17 seconds and about 20 MiB
of peak resident memory.

~~~sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
~~~

Expected status: `VERIFIED`, matching every entry of
[EXPECTED.json](EXPECTED.json). The run checks:

* Literal cyclic subgroups of 15 explicit groups, including $A_5$,
  $A_6$, $S_5$, $\mathrm{SL}(2,5)$, its projective quotient,
  $A_5\times A_5$, and nine cyclic direct-product examples.
* 168 coprime extensions, including all matrices of coprime order in
  eight specified general linear groups, nonfaithful actions, and a
  nonabelian complement.
* Each coset's complete element-order distribution, using literal
  multiplication, against the fixed-space derivation.
* The characteristic-two exception: 106 nontrivial actions attain
  the direct-product count. For odd characteristic, equality requires
  the action to be trivial.
* Rejection of a noncoprime extension; the formula assumes coprimality.

The checker independently compares matrix ranks with literal fixed-vector
counts. It also checks the generator multiplicity of every enumerated
cyclic subgroup. These are checks of the written argument, not independent
peer review. No solver, floating-point arithmetic, external dataset,
large certificate, or third-party Python package is needed.

To check evidence rejection, alter any field of a temporary copy of
`EXPECTED.json` and run `python3 verify.py --check --expected /path/to/copy`.
A mismatch exits unsuccessfully, including under `python3 -O`.

Solvable groups at the same numerical value, a gap above the threshold,
and any priority claim beyond the searched sources are outside this result.
