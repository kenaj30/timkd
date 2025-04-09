from collections import Counter, OrderedDict
import random

def create_random_text(n, probabilities):
    return ''.join(random.choices(tuple(probabilities.keys()), weights=probabilities.values(), k=n))

def average_word_length(text):
    words = text.split()
    return sum(map(len, words)) / len(words) if words else 0

def create_ngrams(text, n=1):
    ngrams = Counter(text[i:i + n] for i in range(len(text) - n + 1))
    return OrderedDict(sorted(normalize_probabilities(ngrams).items()))

def normalize_probabilities(probabilities):
    total = sum(probabilities.values())
    return {key: value / total for key, value in probabilities.items()} if total > 0 else probabilities

def get_conditional_probabilities(text, n):
    ngrams = create_ngrams(text, n)
    next_ngrams = create_ngrams(text, n + 1)
    conditional_probabilities = {}

    for ngram in ngrams:
        conditional_probabilities[ngram] = {}
        for letter in letters:
            new_key = ngram + letter
            if new_key in next_ngrams:
                conditional_probabilities[ngram][letter] = next_ngrams[new_key] / ngrams[ngram]
        conditional_probabilities[ngram] = normalize_probabilities(conditional_probabilities[ngram])

    return conditional_probabilities

def create_markov(n, degree, start, probabilities):
    result = start
    while len(result) < n:
        ngram = result[-degree:]
        if ngram not in probabilities or not probabilities[ngram]:
            result += random.choice(list(letters.keys()))
        else:
            result += random.choices(list(probabilities[ngram].keys()), weights=probabilities[ngram].values())[0]
    return result

with open("hamlet.txt") as file:
    text= file.read()

letters = Counter(text)

for degree in [1, 3, 5]:
    print(f"Źródło {degree} rzędu Markova")
    probabilities = get_conditional_probabilities(text, degree)
    generated_text = create_markov(1000, degree, "probability", probabilities)
    print("Wytworzony tekst:", generated_text)
    print("Średnia długość ciągu:", average_word_length(generated_text))
    print()
