def compute_lps(pattern):
   
    lps = [0] * len(pattern)
    length = 0  # длина предыдущего lps
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):

    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)

    result = []
    i = 0  # индекс для text
    j = 0  # индекс для pattern

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return result

def build_shift_table(pattern):

    m = len(pattern)
    table = {char: m for char in set(pattern)}

    for i in range(m - 1):
        table[pattern[i]] = m - i - 1

    return table


def bmh_search(text, pattern):
  
    n = len(text)
    m = len(pattern)
    if m == 0:
        return []

    shift_table = build_shift_table(pattern)
    result = []
    i = 0

    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            result.append(i)
            i += m  # сдвигаем полностью, чтобы не пропустить совпадения
        else:
            shift = shift_table.get(text[i + m - 1], m)
            i += shift

    return result

text = "abcabcabcdabcabcabcd"
pattern = "abcabcd"
matches_bmh = bmh_search(text, pattern)
matches_kmp = kmp_search(text, pattern)

print(matches_bmh, matches_kmp)
