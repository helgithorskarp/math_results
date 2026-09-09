# q9 contact interface

**Result:** exact reduction by 85.30904627855% of the full current h4035 bare carrier, with 88.35995846143% removed from its q9 part. All 1,810 q9 task IDs retain positive carriers; every individual reduction exceeds 59.24%. This is a carrier-domain change, not an UNSAT ledger update or a measured solver acceleration.

The contact palette now treats each block's 28 physical core-contact edges jointly. `COUNTS.tsv` provides 362 exact plain and augmented sizes and complement certificates. These restrictions are already implied by the original full Ramsey CNF. Their downstream effect is that a constructor or enumerator using the palette never proposes the excluded physical contact assignments.

Generate local tables with `reproduce.py`, or directly:

```sh
g++ -std=c++20 -O3 ramsey_r55_q9_core_contact_domains/row_count.cpp -o /tmp/r55-contact-row
/tmp/r55-contact-row /tmp/r55-contact-inputs/r44_7.g6 /tmp/r55-contact-counts.tsv 362 /tmp/r55-contact-prefix.bin
python3 -B ramsey_r55_q9_core_contact_domains/contact_codec.py /tmp/r55-contact-inputs /tmp/r55-contact-prefix.bin bo1-q9-r5-c000000 0
```

For Python use `Contacts(cache, tables)` and `PhysicalCarrier(task, cache, contacts)`. `size`, `unrank(index)` and `rank(graph)` define a bijection for each q9 task. Graph format is `{n:43, red_hex:226 lowercase hex digits}`, lexicographic physical edges, bit zero=(0,1), red=1. Task names stay `bo1-...`; the integer index belongs to the **new** contact carrier. Never reinterpret it as an old bo1 index.

For an existing complete original q9 carrier graph, save `{task, graph}` to a JSON file and run:

```sh
python3 -B ramsey_r55_q9_core_contact_domains/classify.py /tmp/r55-contact-inputs /tmp/r55-contact-prefix.bin /tmp/r55-q9-input.json
```

Possible statuses:

- `RAMSEY_REJECT`: inspect the returned physical monochromatic five-set.
- `PACKING_REDIRECT_REQUIRED`: two explicit red K4s certify the unchanged h4035 exchange. Consume the existing h4045 normalizer after its original source checks, including red maximality. The two-clique witness alone does not establish those preconditions, and this status is not a taskwise Ramsey rejection.
- `CONTACT_CARRIER_ADMITTED_NOT_A_TARGET`: the graph has a contact-carrier index. Global five-set and maximality checks still remain.

This interface consumes only complete q9 graphs. It requests no transfer of team-r55-1's 161 q10 child inputs and has no claimed effect on their ledger. h3987 remains 99 certified closures/161 unknown; h4001 remains separately 518 exclusions/122 unknown, leaving 2,188,660 whole task IDs undecided.

The coherent gate is complete after the independent counts and physical checks. Do not automatically spend a new milestone on another q, contact marginal, matching rule, or encoding refinement. A follow-up should first name a complete target family and a further measurable physical consequence.
