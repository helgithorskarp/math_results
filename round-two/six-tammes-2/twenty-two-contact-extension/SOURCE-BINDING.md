# Source binding and execution premises

The three files in `frozen/` are byte-for-byte copies of the arithmetic
model, literal reader and delta reader used in the completed historical
author proof. Their historical comments describe their status when
written; those comments do not report the current proof or review status.

The fixed code expects its mathematical dependencies in an older
directory layout. `binding.py` constructs that layout under the user's
selected scratch directory, copies only the ten small source/proof files
named in `INPUTS.json`, and checks every copied byte against its pin.
No private checkpoint, private ledger, credentials or coordinate corpus
is read. Existing runtime files must match exactly, and runtime source
symlinks are refused. The existing mathematical loaders also verify the
frozen model, literal reader, published strip model and frame pins.

The frozen delta source includes the existing optional campaign pause
checks. These only inspect the presence of `PAUSED.json`/`HANDOVER.json`
at the named campaign location. A reader outside the campaign need not
have that directory. The reproduction sources never modify it.

The initial proof state is a single closed dyadic root with all 364
obligations, no selected literal, no boundedness claim and an open stack.
Its actual full-reader check establishes only that trivial partial
bookkeeping and the exact scalar cap margin.

Each successful generation transition keeps every old record and
closed node unchanged, installs complete node/split updates atomically,
and selects at most 2,500 new literals. Generation is not verification.
Before the next generation step, the frozen delta reader actually checks
every new literal, boundedness flag, packing exclusion and necessary
regular domain, and checks complete closed partition coverage and old
entry retention. It does not run the float selector.

When the pending stack becomes empty, the actual delta call also
requests the complete structural check. An induction from the actual
full-reader seed execution and every successful transition execution
then gives a checked complete cover. Neither a signed manifest nor
receipt labels prove that these executions occurred. Successful actual
execution of the whole chain is the computational premise.

The canonical proof-state digest retains each cell, obligation,
literal entry, bound, split, child and closed-node status; it excludes
timings, filenames and search counters. A fresh v2 tree need not match
the historical mixed-generation tree or its byte hash. Reproduction
must match the published fresh expectation only after that fresh chain
has itself completed and been checked.

The same-author model and integer interval kernel, the imported
actual-packing critical147 lemma, and the ordinary geometric reduction
are explicit trust boundaries. Regression against the frozen reader is
not independent mathematical validation or a global occurrence theorem.
