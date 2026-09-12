# Both colors of every good43 are 14-fault Hamiltonian

Every hypothetical 43-vertex graph with neither a clique nor an independent
set of order five has the following symmetry-free property in **both** colors:

- deleting any at most 15 vertices leaves a Hamilton path;
- deleting any at most 14 vertices leaves a Hamilton cycle; and
- deleting any at most 13 vertices leaves a Hamilton-connected graph.

Equivalently, every induced 28-set is traceable, every induced 29-set is
Hamiltonian, and every induced 30-set is Hamilton-connected, with the same
statements for all larger sets.  The quantifiers range over every vertex set,
not a catalog, chosen neighborhood, edge layer, or automorphism family.

[PROOF.md](PROOF.md) gives the short deduction.  Its target-specific input is
the independently accepted theorem that each color of every good43 has
vertex connectivity equal to minimum degree, hence at least 18.  The other
input is the classical Chvatal--Erdos Hamiltonicity theorem and its
Hamilton-connected companion.

## Endpoint-facing consequence

If a good43 exists, one may relabel a red Hamilton cycle to the standard
cycle `C_43`.  This fixes 43 red physical edges while leaving all 860 chords
independent.  It is not a cyclic/circulant graph restriction: no rotation is
required to preserve the chords.

The resulting exact physical SAT receiver has:

```text
variables                 860
clauses               1530585
fixed red cycle edges       43
removed satisfied clauses 394611
clause widths          6 through 10
```

`generate.py` deterministically emits this complete normalized formula or a
compact exact summary.  It imposes only the fixed Hamilton cycle and literal
no-red-K5/no-blue-K5 clauses.  The normalization is existence-equivalent, but
no target solve or tractability claim is made.

The theorem also forces, in each color, at least 138,712,176,296 cycles of
lengths 29 through 43.  Every physical edge in its own color lies on at least
30,273,024,984 cycles of lengths 30 through 43, including a spanning cycle.

## Reproduction

From the repository root, using CPython 3.11 or later and its standard
library only:

```sh
python3 -B ramsey_r55_fault_hamiltonicity/verify.py
python3 -O -B ramsey_r55_fault_hamiltonicity/verify.py
python3 -B ramsey_r55_fault_hamiltonicity/generate.py --summary
cd ramsey_r55_fault_hamiltonicity && sha256sum -c SHA256SUMS
```

Expected final status:

```text
VERIFIED_FAULT_HAMILTONICITY_RECEIVER
```

The verifier independently reconstructs the target clause stream and its
SHA-256, checks all arithmetic and five-set distributions, validates the
pinned source files, and checks a literal Hamilton-cycle relabeling of a
published physical good42 control over all 850,668 five-subsets.  The control
is not a 43-vertex witness or proof premise.

To write the target CNF outside the checkout:

```sh
python3 -B ramsey_r55_fault_hamiltonicity/generate.py \
  --output /tmp/r55-hamilton-normalized.cnf
```

The generated 69,753,784-byte CNF is bulky operational state and is
intentionally omitted from Git.  `EXPECTED.json` records both its full-file
SHA-256 and the canonical clause-stream SHA-256.

## Trust and status

The accepted connectivity source and review are hash-pinned in
`DEPENDENCIES.json`.  Their exact computational and imported
`R(4,5)<=25` boundaries remain inherited.  The Chvatal--Erdos theorem is
cited from its original 1972 paper; it is not formalized here.  The new
deduction is written mathematics with same-author exact software checks.

This is a reusable complete-class theorem and construction normalization. It
does not produce a good43, improve `43 <= R(5,5) <= 46`, decide a carrier
task, or exclude any edge-count layer.
