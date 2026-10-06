"""Portable checked helper subset; used function bodies are unchanged."""
import itertools

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def occurrences(word):
    """Sparse distinct labels; no standardization or author checker is used."""
    result = []
    for a, b, c, d in itertools.combinations(range(len(word)), 4):
        if word[b] < word[a] < word[d] < word[c]:
            selected = {a, b, c, d}
            if not any(j not in selected and word[b] < word[j] < word[c]
                       for j in range(a + 1, d)):
                result.append((a, b, c, d))
    return tuple(result)
