
def calculate_residuals(L, word):
    residuals = set()
    stats = {'ok': 0, 'vide': 0}
    for w in L:
        if w.startswith(word):
            residual = w[len(word):]
            if residual == '':
                stats['ok'] += 1
            else:
                stats['vide'] += 1
            residuals.add(residual)
    return residuals, stats


def is_prefix_code(L):
    Ln = set(L)
    i = 0
    all_residuals = []
    stats_total = {'ok': 0, 'vide': 0}
    while True:
        residuals = set()
        stats_word = {'ok': 0, 'vide': 0}

        for word in Ln:
            word_residuals, stats_word_local = calculate_residuals(L, word)
            stats_total['ok'] += stats_word_local['ok']
            stats_total['vide'] += stats_word_local['vide']
            residuals.update(word_residuals)

        if i < 1:
            non_empty_residuals = set()
            for res in residuals:
                if res!= '':
                    non_empty_residuals.add(res)
            residuals = non_empty_residuals

        if '' in residuals:
            return False, stats_total

        all_residuals_present = True
        for res in residuals:
            if res not in all_residuals:
                all_residuals_present = False
                break

        if all_residuals_present:
            return True, stats_total

        for res in residuals:
            all_residuals.append(res)
        Ln = residuals
        i += 1

    return stats_total

# def find(L):
#     if is_prefix_code(L):
#         return True
#     return False

def find(L):
    is_valid, _ = is_prefix_code(L)
    return is_valid

def main():
    source = ["000", "010", "011", "01001"]
    stat = is_prefix_code(source)
    print(stat)
    result = find(source)
    print("resultat ", result)


if __name__ == "__main__":
    main()