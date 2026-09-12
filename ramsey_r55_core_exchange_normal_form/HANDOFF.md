# Exact receiver contract

This package exposes a new globally covering normal form on the complete
maximal-K4 carrier. It does not operate any owner queue or change task verdicts.

**Input:** a complete physical graph (`n:43`, `red_hex`:226 lowercase hex digits,
bit k red for the kth lexicographic pair u<v), plus `red`, `blue`, `core` lists
partitioning the vertices. The red/blue blocks are monochromatic K4s; the
non-red residual is red-K4-free and the core blue-K4-free. There must be at
least five red blocks. These preconditions hold for the inherited good43 cover.

```sh
python3 -B ramsey_r55_core_exchange_normal_form/destination.py \
  /path/to/catalog source.json destination.json
python3 -B ramsey_r55_core_exchange_normal_form/verify_destination.py \
  /path/to/catalog source.json destination.json
```

The descent keeps the graph's edges unchanged, increasing `(r,q,e_red(core))`.
The destination gives an exact original-registry task ID, physical edge word
and full new-to-old permutation. It uses all catalog orders 3,7,11,15. The
standalone checker verifies the endpoint independently of the producer; it
does not verify intermediate event history. A local domain failure instead
carries a literal monochromatic five-set in the original physical labels.

The status `ORDERED_CARRIER_NO_RAMSEY_VERDICT` means base pair/star membership
with a terminal normal packing. It does not claim full Ramsey validity or
membership in every separately filtered carrier. Every good43 destination
also obeys all genuine Ramsey constraints and the inherited maximality/contact
filters by the written proof.

**Constraint emitter:** provide q, r and the exact graph6 core record as a
single shell-quoted argument. This writes the complete all-row normal-form
CNF over physical variables 1–903, with no auxiliary variables:

```sh
python3 -B ramsey_r55_core_exchange_normal_form/exchange.py clauses \
  10 10 'B?' /tmp/example-core-exchange.cnf
```

`B?` is the empty order-3 core; the command is only an emitter example, not a
target result. At each block/core incidence the guard asserts three contacts
in the block's color and one in the opposite color. The consequent bounds
red contacts from the displaced row to the remaining core by the original
core vertex's red degree. Fixed core edges are a precondition. Map variables
explicitly if integrating with an assumption formula that uses another
physical/free-variable convention.

**Global cover semantics are mandatory.** A violating assignment may redirect
to another core or another q/r stratum. During red-maximality repair r can
increase while q decreases. Appending these constraints to an old task and
proving UNSAT is not an original-task UNSAT certificate. A complete reduced
cover or explicit redirect joins are required. This package does not supply
RUP derivations from an old fixed-task Ramsey formula.

The measured bound is an exact rational comparison to the reviewed
maximal-residual whole-carrier upper, with safe minima for overlapping contact
predicates. It is not a conditional fraction for any solver queue, q10 child,
orientation branch, or degree-filtered family. No runtime improvement is
claimed. All q8 task bounds improve; q9 and q10 have explicit unchanged entries.

**Next lane milestone:** a complete original-task consequence, useful whole
subclass closure, or repeatable retirement. The current result supplies the
complete all-q receiver restriction already; counting a third/fourth row
alone is not the planned next milestone. R2 retains ownership of execution
and proof accounting, and chooses its detailed consumption method.
