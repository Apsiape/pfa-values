"""Independent exact finite checks for the included v1.1 quantum constructions.

No code from the research or cross-family check engines is used. The quantum
side evolves the joint distribution of the actually measured basis state and
an outcome-only DFA, from squared entries of explicit rational unitaries.
The comparison side uses direct stochastic-matrix multiplication and closed
sampling probabilities. This is not a two-way compiler or timing check.
Run as: python quantum_checks.py (standard library only; Python 3.10 or later).
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def words(alphabet, maximum):
    for n in range(maximum + 1):
        yield from map(''.join, product(alphabet, repeat=n))


def walsh(d):
    require(d > 0 and d & (d-1) == 0, 'Walsh dimension must be a power of two')
    root = 1
    while root * root < d:
        root += 1
    require(root * root == d, 'rational Walsh dimension must be a square')
    return [[F((-1) ** ((i & j).bit_count()), root) for j in range(d)] for i in range(d)]


def quantum_matrices(types, coin):
    k, d = len(types) + 1, len(coin)
    n = k * d
    out = {}
    for shift, letter in enumerate(types, 1):
        u = [[F(0) for _ in range(n)] for _ in range(n)]
        for g in range(k):
            for j in range(d):
                for h in range(d):
                    u[((g + shift) % k) * d + h][g * d + j] = coin[h][j]
        out[letter] = u
    out['$'] = [[F(i == j) for j in range(n)] for i in range(n)]
    return out, k, d


def check_columns(matrices):
    count = 0
    for symbol, u in matrices.items():
        n = len(u)
        for i in range(n):
            for j in range(i, n):
                dot = sum((u[t][i] * u[t][j] for t in range(n)), F(0))
                require(dot == F(i == j), 'nonorthonormal columns: ' + str((symbol, i, j, dot)))
                count += 1
    return count


def outcome_edges(matrices):
    return {a: [[(i, u[i][j] ** 2) for i in range(len(u)) if u[i][j]]
                for j in range(len(u))] for a, u in matrices.items()}


def measured_run(word, edges, coin_dimension, initial, update):
    # Complete measurement makes this exact distributional update sufficient.
    dist = {(0, initial): F(1)}
    for letter in word + '$':
        nxt = defaultdict(F)
        for (basis, control), mass in dist.items():
            for target, probability in edges[letter][basis]:
                g, j = divmod(target, coin_dimension)
                nxt[(target, update(control, g, j))] += mass * probability
        dist = dict(nxt)
        require(sum(dist.values(), F(0)) == 1, 'quantum/controller probability conservation')
    return sum((p for (_, s), p in dist.items() if s[0] == 'accept'), F(0))


def partitions(matrices, denominator):
    out = {}
    for a, m in matrices.items():
        rows = []
        for row in m:
            require(sum(row, F(0)) == 1 and all(p >= 0 for p in row), 'PFA stochastic row')
            counts = [p * denominator for p in row]
            require(all(c.denominator == 1 for c in counts), 'not a common denominator')
            rows.append(tuple(j for j, c in enumerate(counts) for _ in range(int(c))))
        out[a] = tuple(rows)
    return out


def pfa_run(word, matrices, accepting=(2,)):
    state = [F(1), F(0), F(0)]
    for a in word:
        state = [sum((state[i] * matrices[a][i][j] for i in range(3)), F(0)) for j in range(3)]
    return sum((state[j] for j in accepting), F(0))


def exact_controller(k, table):
    def update(s, g, j):
        if s[0] != 'live':
            return ('dead',)
        _, previous, q = s
        step = (g - previous) % k
        if step == 0:
            return ('accept',) if q == 2 else ('dead',)
        if step not in (1, 2):
            return ('dead',)
        a = 'ab'[step-1]
        return ('live', g, table[a][q][j])
    return update


def sampling_controller(k, table, denominator, mutant=False):
    r = (denominator - 1).bit_length()
    def update(s, g, coin):
        if s[0] != 'live':
            return ('dead',)
        _, previous, q, active, used, value, success = s
        step = (g - previous) % k
        if step == 0:
            return ('accept',) if active == '-' and q == 2 else ('dead',)
        a = 'abcd'[step-1] if 1 <= step <= 4 else '?'
        if active == '-':
            if a not in 'ab':
                return ('dead',)
            if denominator == 1:
                return ('live', g, table[a][q][0], a, 0, 0, True)
            return ('live', g, q, a, 0, 0, False)
        if a == 'd':
            return ('live', g, q, '-', 0, 0, False) if success else ('dead',)
        if a != 'c':
            return ('dead',)
        if success:
            return ('live', g, q, active, 0, 0, True)
        value, used = 2 * value + (coin % 2), used + 1
        if used == r:
            if value < denominator:
                q, success = table[active][q][value], True
            elif mutant and value == denominator:
                # Deliberately wrong: count one rejected sample as accepting.
                q, success = 2, True
            value, used = 0, 0
        return ('live', g, q, active, used, value, success)
    return update


def parse_code(code):
    # Separate grammar reader for expected values; never reads quantum outcomes.
    letters, lengths, i = [], [], 0
    while i < len(code):
        if code[i] not in 'ab':
            return None
        letters.append(code[i])
        i += 1
        n = 0
        while i < len(code) and code[i] == 'c':
            n, i = n + 1, i + 1
        if i == len(code) or code[i] != 'd':
            return None
        i += 1
        lengths.append(n)
    return ''.join(letters), lengths


def expected_code(code, matrices, denominator):
    parsed = parse_code(code)
    if parsed is None:
        return F(0)
    raw, lengths = parsed
    result = pfa_run(raw, matrices)
    if denominator > 1:
        r = (denominator - 1).bit_length()
        for n in lengths:
            result *= 1 - (1 - F(denominator, 2 ** r)) ** (n // r)
    return result


def channel_matrix(m):
    # Matrix-unit coordinates index |i><j| by 3*i+j.
    phi = [[F(0) for _ in range(9)] for _ in range(9)]
    for i in range(3):
        for j in range(3):
            phi[3*j+j][3*i+i] = m[i][j]
    return phi


def channel_run(word, channels):
    rho = [F(1)] + [F(0)] * 8
    for a in word:
        phi = channels[a]
        rho = [sum((phi[i][j] * rho[j] for j in range(9)), F(0)) for i in range(9)]
        require(rho[0] + rho[4] + rho[8] == 1, 'channel trace')
    return rho[8]


def main():
    print('v1.1 independent exact quantum checker; arithmetic: fractions.Fraction')
    print('Scope: QFA-CL Walsh/rejection sampling and classical CPTP embedding.')
    print('No two-way counter compiler, timing, or payout is certified by this checker.')
    # Bounds computed before materializing any matrices or word collections.
    dims = [3*4, 3*16, 5*4]
    print('Planned unitary dimensions:', dims, '; largest dense matrix entries:', max(dims)**2)
    print('Planned Gram checks:', 3*(12*13//2) + 3*(48*49//2) + 5*(20*21//2))
    print('Word streams: 63 binary words per exact simulation; 341 syntax words per denominator.')
    print('Sampling cases: denominators 1,3,4,5; at most 111 padded codes per denominator.')

    dyadic = {
        'a': ((F(1,2), F(1,4), F(1,4)), (F(0), F(3,4), F(1,4)), (F(1,4), F(1,4), F(1,2))),
        'b': ((F(1,4), F(1,2), F(1,4)), (F(1,2), F(1,4), F(1,4)), (F(0), F(1,4), F(3,4)))
    }
    grams, exact_count = 0, 0
    for denominator in (4, 16):
        matrices, k, d = quantum_matrices('ab', walsh(denominator))
        grams += check_columns(matrices)
        edges = outcome_edges(matrices)
        table = partitions(dyadic, denominator)
        update = exact_controller(k, table)
        for w in words('ab', 5):
            got = measured_run(w, edges, d, ('live', 0, 0), update)
            require(got == pfa_run(w, dyadic), 'dyadic exact simulation: ' + repr(w))
            exact_count += 1

    matrices, k, d = quantum_matrices('abcd', walsh(4))
    grams += check_columns(matrices)
    edges = outcome_edges(matrices)
    sampling_count = syntax_count = malformed_count = 0
    first_positive = None
    for denominator in (1, 3, 4, 5):
        # Non-dyadic rows with a single accepting state and deterministic endpoints.
        def row(counts):
            return tuple(F(c, denominator) for c in counts)
        if denominator == 1:
            pfa = {'a': (row((0,0,1)), row((1,0,0)), row((0,1,0))),
                   'b': (row((0,1,0)), row((0,0,1)), row((1,0,0)))}
        else:
            pfa = {'a': (row((1,1,denominator-2)), row((0,1,denominator-1)), row((1,denominator-1,0))),
                   'b': (row((denominator-1,1,0)), row((1,0,denominator-1)), row((0,denominator-2,2)))}
        table = partitions(pfa, denominator)
        update = sampling_controller(k, table, denominator)
        initial = ('live', 0, 0, '-', 0, 0, False)
        r = (denominator - 1).bit_length()
        lengths = (0,1,3) if r == 0 else tuple(sorted({0,r-1,r,r+1,2*r}))
        for raw in words('ab', 2):
            for padding in product(lengths, repeat=len(raw)):
                code = ''.join(a + 'c'*n + 'd' for a, n in zip(raw, padding))
                got = measured_run(code, edges, d, initial, update)
                require(got == expected_code(code, pfa, denominator), 'padded code: '+repr((denominator, code, got)))
                sampling_count += 1
                if got > 0 and first_positive is None:
                    first_positive = (denominator, code, got)
        for code in words('abcd', 4):
            got = measured_run(code, edges, d, initial, update)
            require(got == expected_code(code, pfa, denominator), 'syntax/partial-trial case: '+repr((denominator, code)))
            syntax_count += 1
            malformed_count += parse_code(code) is None
        if denominator == 3:
            code = 'accd'
            mutant = measured_run(code, edges, d, initial, sampling_controller(k, table, 3, mutant=True))
            correct = expected_code(code, pfa, 3)
            require(mutant != correct, 'positive control failed to detect wrong sampler')
            print('Positive control: planted bad sampler detected; code accd, expected', correct, 'mutant', mutant)

    channels = {a: channel_matrix(m) for a, m in dyadic.items()}
    channel_count = 0
    for a, m in dyadic.items():
        # Choi matrix is diagonal in the |input,output> ordering, with diagonal M(i,j).
        require(all(p >= 0 for row in m for p in row), 'Choi positivity')
        for i in range(3):
            require(sum(m[i], F(0)) == 1, 'Choi partial trace')
    for w in words('ab', 5):
        require(channel_run(w, channels) == pfa_run(w, dyadic), 'CPTP embedding: '+repr(w))
        channel_count += 1

    bad = walsh(4)
    bad[0][0] = F(3,5)
    detected = False
    try:
        check_columns({'planted': bad})
    except AssertionError:
        detected = True
    require(detected, 'positive control failed to detect nonunitarity')
    print('Positive control: planted nonorthonormal column detected.')
    require(first_positive is not None, 'no positive-acceptance test')
    print('Positive acceptance witness:', first_positive)
    print('Orthonormal column inner products checked:', grams, '; failures: 0')
    print('Exact dyadic PFA/QFA-CL word comparisons:', exact_count, '; failures: 0')
    print('Rejection-sampling padded-code comparisons:', sampling_count, '; failures: 0')
    print('Exhaustive short syntax/partial-trial comparisons:', syntax_count,
          '; malformed cases:', malformed_count, '; failures: 0')
    print('Rational CPTP/PFA word comparisons:', channel_count, '; failures: 0')
    print('TOTAL acceptance comparisons:', exact_count + sampling_count + syntax_count + channel_count)
    print('PASS; positive controls detected: 2; no floating-point arithmetic used.')


if __name__ == '__main__':
    main()
