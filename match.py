# Nick Haliday
# String Matching Algorithms


def compute_pi(pattern):
    """compute_pi(pattern) -> list of integers

    Return the prefix function pi[q] as an array of length len(pattern) + 1.
    pi[q] = max{ k: k < q and pattern[:k] is a suffix of pattern[:q] }
    Runs in O(len(pattern)) time."""

    m = len(pattern)
    pi = [-1] * (m + 1)
    k = 0

    for q in range(1, m):
        while k > -1 and pattern[k] != pattern[q]:
            k = pi[k]
        k += 1
        pi[q + 1] = k

    return pi


def kmp_match(pattern, text):
    """kmp_match(pattern, text) -> generator

    Yields all valid shifts in text using the Knuth-Morris-Pratt
    algorithm. Runs in O(len(pattern) + len(text)) time."""

    m = len(pattern)
    n = len(text)

    pi = compute_pi(pattern)
    q = 0
    for i in range(n):
        while q > -1 and pattern[q] != text[i]:
            q = pi[q]
        q += 1
        if q == m:
            q = pi[q]
            yield i - m + 1


def compute_z(S):
    """compute_z(S) -> list of integers

    Return the Z function Z_i as a list. Z_i is the longest common prefix of
    S and S[i:]. Runs in O(len(S)) time."""

    m = len(S)
    Z = [0] * m
    Z[0] = m
    
    l = 0
    r = 0

    i = 1
    while i < m:
        if i >= r:
            while i + Z[i] < m and S[Z[i]] == S[i + Z[i]]:
                Z[i] += 1

            l = i
            r = i + Z[i]
        else:
            Z[i] = Z[i - l]

            if i + Z[i] >= r:
                Z[i] = r - i

                while i + Z[i] < m and S[Z[i]] == S[i + Z[i]]:
                    Z[i] += 1
                
                l = i
                r = i + Z[i]
        i += 1

    return Z


def z_match(pattern, text):
    """z_match(pattern, text) -> generator

    Yield all valid shifts using the Z algorithm. Runs in O(len(pattern) +
    len(text)) time."""

    S = pattern + '$' + text
    Z = compute_z(S)

    m = len(pattern)
    n = len(text)

    for i in range(m + 1, m + 1 + n):
        if Z[i] >= m:
            yield i - m - 1
