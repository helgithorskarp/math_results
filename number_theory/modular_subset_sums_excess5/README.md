# Excess-five modular subset sums: the complete long-chain case

For every integer **n >= 5**, let **N = 2^n + 5**. Consider n-element
subsets of Z/NZ whose 2^n subset sums, including the empty sum, are all
distinct. We classify the entire family containing a signed unit
doubling chain of length n-2, up to common unit dilation and independent
sign changes.

There are exactly **three equivalence classes**, represented by:

- B0: the powers 1, 2, ..., 2^(n-1);
- B1: the powers through 2^(n-2), together with 2^(n-1)+1;
- B2: the powers through 2^(n-3), together with 2^(n-2)+1 and 2^(n-1)+1.

The lists indicated by powers contain powers of two only. These are
published constructions; the new obligation addressed here is their
necessity throughout the chain-containing family. Its exact number of
subsets in the fixed labeled group is **3 * 2^(n-1) * phi(N)**.

The proof normalizes the chain, expresses subset sums as four translates
of an interval, and reduces the two remaining elements to exactly six
forms. Explicit dilations identify them with B0, B1 and B2. A signed
doubling graph proves inequivalence and determines their stabilizers.

Two further statements apply to **every** admissible set:

- At most one element is a nonunit; it has gcd 3 with N and occurs only
  for even n. If present, the five missing sums have residue counts
  (3,1,1) modulo 3, in some order.
- The signed doubling graph is a union of directed paths; any nonunit
  is isolated. Every set outside the classified family has all path
  components of order at most n-3.

The unrestricted classification remains open here. The remaining sets
need not contain a long chain. The exact class count above is a count
of the proved subclass, not an unrestricted upper bound.

## Proof and exact controls

[proof.md](proof.md) proves the uniform theorem, its count, and the
residual assertions without a computational premise. The finite replay
checks every normalized pair for n=5,...,10, all six unit identities,
the graph invariants and stabilizers, and every admissible signed-class
set for n=5,6. Both small censuses consist entirely of the three classes.

From this directory, run:

```sh
python3 reproduce.py
```

Tested with CPython 3.11.2; only the Python standard library is required.
Run normally, with assertions enabled. The expected status is
`EXCESS_FIVE_CHAIN_PACKAGE_VERIFIED`; the complete signed-class counts
at n=5,6 are 54 and 66, and the actual subset counts are 1728 and 4224.
The replay takes about one second on the development machine.

The compact expected evidence has SHA-256:

```text
5c1c87a650c2d1ae0c17e53880cfacb6c4f85a0625085d096eb4e8d2889ba568
```

- `generate.py` uses exact integer bit masks and a complete prefix
  enumeration. A colliding prefix can have no admissible extension.
- `verify.py` imports no generator code. It uses literal subset-sum
  lists, unit orbits and an unpruned combinations census at n=5. At
  n=6 it checks every listed set and every unit orbit; enumeration
  completeness there relies on the generator and its pruning argument.
- `reproduce.py` compares every generated evidence entry with
  `expected.json`, invokes the independent implementation and confirms
  rejection of a deliberately corrupted equivalence certificate.
- `normal_forms.json` contains the six offsets and their multipliers.
- `SHA256SUMS` records the compact source/evidence hashes.

The written proof, not finite extrapolation, establishes the all-n
claim. There is no SAT/MILP solver, floating-point calculation, external
dataset or reconstruction theorem in its trust base. The package has
not undergone independent peer review or proof-assistant formalization.
No large external certificate is needed for replay.

## Literature and scope

The underlying open problem is in Cambie, Gao, Kim and Liu,
*The Erdős distinct subset sums problem in a modular setting*, Acta
Arithmetica 217 (2025), 295–307:
[publisher record](https://doi.org/10.4064/aa231107-13-9),
[open author manuscript](https://arxiv.org/abs/2308.03748).
The source classifies excesses through three and proposes perturbation
classifications and counting bounds at larger excesses. Its general
question is eventual; the campaign's n >= 5 formulation is a deliberate
sharpening. See [literature.md](literature.md) for precise attribution,
access limitations and novelty caveats.
