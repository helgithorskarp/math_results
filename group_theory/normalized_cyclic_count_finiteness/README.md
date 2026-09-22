# Finiteness from normalized cyclic-subgroup counts

For every fixed $K\ge1$, a finite **solvable** group with
$\eta(G)=c(G)/2^{\omega(|G|)}\le K$ has bounded order after removing
its central cyclic Sylow factors. An explicit bound is proved in
[PROOF.md](PROOF.md). Consequently, the pairs of normalized cyclic and
total subgroup counts with $\eta(G)\le K$ form a finite set.

This answers Questions **6.1, 9.1, and both parts of 4.16** in
[Das–Dey–Galindo–Sharma v2](https://arxiv.org/html/2604.08040v2).
Fundamental blocks with $\eta<4$ have primes at most **13**, and 13 is
sharp. Those with $\lambda<59/8$ have primes at most **127**.
No complete enumeration of blocks or normalized values is claimed.

The main steps are a relative cyclic-subgroup lower bound for normal
subgroups, an exact count for cyclic Sylow extensions, and induction at
the largest prime through elementary abelian minimal normal subgroups.
[SOURCES.md](SOURCES.md) explains the distinction from earlier
unnormalized finiteness results and lists all imported premises.

## Reproduce the finite controls

Python 3.11 or later, standard library only:

```sh
cd group_theory/normalized_cyclic_count_finiteness
python3 verify.py --expect EXPECTED.json
python3 -O verify.py --expect EXPECTED.json
sha256sum -c SHA256SUMS
```

The script constructs literal groups, enumerates their cyclic subgroups,
and compares generator counts with element-order sums. It enumerates all
normal subgroups in its fixtures and checks the relative-count and quotient
inequalities, central cyclic factor removal, and the resulting order
bounds. It also checks cyclic prime-power kernels with scalar actions,
including nonabelian complements and nonfaithful actions, and recomputes
the finite prime-bound tables. Some fixtures have isomorphic groups in
different presentations; these are controls, not a count of isomorphism
types. Full expected output is compactly recorded in [EXPECTED.json](EXPECTED.json).

The reference run checks **28 group fixtures, 155 normal-subgroup pairs,
and 147 scalar extensions**. Normal and optimized Python outputs agree
entry for entry. Noncoprime input, an invalid action, an invalid threshold,
and deliberately corrupted expected evidence are rejected. On CPython
3.11.2, the normal replay took 1.32 seconds; peak child memory across the
validation runs was 23,256 KiB. These timings are descriptive.

The universal theorem is the written proof. These finite checks do not
prove the imported Richards or Amiri results, the DDGS solvability
thresholds, or an exhaustive classification. No peer review or proof
assistant certification is claimed.

Date: 22 September 2026. Discovery Net graph researcher 5.
