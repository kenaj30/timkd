import random
from collections import Counter

def generate_random_words(probabilities):
    return random.choices(tuple(probabilities), weights=probabilities.values())

def create_ngrams(text, n):
    words = text.split()
    if n == 0:
        return normalize_probabilities(Counter(words))
    ngrams = Counter(tuple(words[i:i + n]) for i in range(len(words) - n + 1))
    return normalize_probabilities(ngrams)

def normalize_probabilities(probabilities):
    total = sum(probabilities.values())
    return {key: value / total for key, value in probabilities.items()}

def get_conditional_probabilities(text, n):
    ngrams = create_ngrams(text, n)
    next_ngrams = create_ngrams(text, n + 1)
    conditional_probabilities = {}

    for ngram, prob in next_ngrams.items():
        prefix, last_word = tuple(ngram[:-1]), ngram[-1]
        if prefix not in conditional_probabilities:
            conditional_probabilities[prefix] = {}
        conditional_probabilities[prefix][last_word] = prob / ngrams[prefix]

    return {key: normalize_probabilities(Counter(value)) for key, value in conditional_probabilities.items()}

def create_markov(text, n, k, start=None):
    ngram = start or generate_random_words(create_ngrams(text, 0))
    for degree in range(1, n):
        ngram.extend(generate_random_words(get_conditional_probabilities(text, degree)[tuple(ngram)]))

    probabilities = get_conditional_probabilities(text, n)
    result = ngram.copy()

    for _ in range(k - n):
        if tuple(ngram) in probabilities:
            next_word = generate_random_words(probabilities[tuple(ngram)])[0]
            result.append(next_word)
            ngram = (*ngram[1:], next_word)
        else:
            break

    return ' '.join(result)

with open("norm_wiki_sample.txt") as f:
    text = f.read()
print("Źródło 1 rzędu Markova")
print(create_markov(text, 1, 100))
print()
print("Źródło 2 rzędu Markova")
print(create_markov(text, 2, 100))
print()
print("Źródło 2 rzędu Markova z \"probability\":")
print(create_markov(text, 2, 100, ["probability"]))
