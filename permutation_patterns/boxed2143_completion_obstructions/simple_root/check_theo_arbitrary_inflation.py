"""Only the unchanged helper used by the accepted root reviewer."""

def minimum_interval(p):
    intervals = [(end - first, first, end) for first in range(len(p))
                 for end in range(first + 2, len(p) + 1)
                 if end - first < len(p) and set(p[first:end]) ==
                 set(range(min(p[first:end]), max(p[first:end]) + 1))]
    return min(intervals) if intervals else None
