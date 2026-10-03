"""Portable local reproduction policy; no campaign state, account or network."""


def operations_check():
    # Stage and control subprocesses receive all numerical thread settings=1.
    # Wall/conflict limits are checked by their serial supervisors. Run this
    # reproduction in a one-CPU/two-GiB process scope, as in the author run.
    return dict(local_reproduction=True,threads=1,CPUs=1,GiB=2,
                native_conflicts=50000,native_seconds=30)
