import csv
import json
import math
import random

def ran_binaire(longeur):
    binary_number = ""
    for _ in range(longeur):
        bit = str(random.randint(0, 1))
        binary_number += bit
    return binary_number

def ran_langage():
    longeur_langage = random.randint(2, 10)
    langages = []
    for _ in range(longeur_langage):
        lang = ran_binaire(random.randint(2, 7))
        langages.append(lang)
    return langages

def bit_frequency(langage):
    frequency = {'0': 0, '1': 0}
    for bit_string in langage:
        for bit in bit_string:
            frequency[bit] += 1
    return frequency

def information_complexity(langage):
    unique_bits = set(bit for bit_string in langage for bit in bit_string)
    bit_frequencies = bit_frequency(langage)
    complexity = 0
    for bit in unique_bits:
        p_x = bit_frequencies.get(bit, 0) / len(langage)
        complexity += p_x * math.log2(p_x)
    return complexity

def bit_density(binary_data):
    total_bits = sum(len(bit_string) for bit_string in binary_data)
    total_mots = len(binary_data)
    return total_bits / total_mots


def verification_code(table):
    results = []
    stats = {'e': 0, 'vide': 0, 'duplicate': 0}
    for i in range(len(table)):
        prefix = table[i]
        element_results = []
        for j in range(i + 1, len(table)):
            if table[j] == prefix:
                result = "e"
                stats['e'] += 1
            elif table[j].startswith(prefix):
                result = table[j][1:]
                if result == prefix:
                    stats['duplicate'] += 1
            else:
                result = "vide"
                stats['vide'] += 1
            element_results.append((table[j], result))
        results.append((table[i], element_results))
    return results, stats



def retire_result(results):
    all_empty = True
    duplicate = False
    for result in results:
        for sub_result in result[1]:
            if 'e' in sub_result[1] and sub_result[1] != 'e' and sub_result[1] != 'vide':
                return "pas code"
            elif sub_result[1] != 'vide':
                all_empty = False
            if result[0] == sub_result[1]:
                duplicate = True
    if all_empty:
        return "code"
    elif duplicate:
        return "code"
    else:
        return "pas code"

def calculate_r(L, word):
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

def v_code(L):
    Ln = set(L)
    i = 0
    all_residuals = []
    stats_total = {'ok': 0, 'vide': 0}

    while True:
        residuals = set()
        stats_word = {'ok': 0, 'vide': 0}
        for word in Ln:
            word_residuals, stats_word_local = calculate_r(L, word)
            stats_total['ok'] += stats_word_local['ok']
            stats_total['vide'] += stats_word_local['ok']
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

def final_result(source):
    is_valid, stats = v_code(source)
    return is_valid, stats

def esemble_donnee(data):
    datas = []
    nombre_de_mots = len(data)
    bit_freq = bit_frequency(data)
    info_complexity = information_complexity(data)
    bit_density_value = bit_density(data)
    results, stats = final_result(data)
    datas.append([
        nombre_de_mots,
        bit_freq,
        info_complexity,
        bit_density_value,
        stats,
        results
    ])
    return datas

def get_donnee_verif(data):
    datas = []
    nombre_de_mots = len(data)
    bit_freq = bit_frequency(data)
    info_complexity = information_complexity(data)
    bit_density_value = bit_density(data)
    results, stats = final_result(data)
    datas.append([
        nombre_de_mots,
        bit_freq,
        info_complexity,
        bit_density_value,
        stats
    ])
    return datas

def main():
    all_results = []
    for _ in range(5000):
        resultat = ran_langage()
        data = [rest for rest in resultat]
        result = esemble_donnee(data)
        all_results.extend(result)
    with open('stock_donnee.txt', 'w') as file:
        json.dump(all_results, file)
    with open('stock_donnee.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["mots", "moyenne frequence", "variation mots", "moyenne mots", "stats", "resultat"])
        for row in all_results:
            writer.writerow(row)
        print("creation des donnees terminer")

if __name__ == "__main__":
    main()