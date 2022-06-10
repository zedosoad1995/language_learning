from collections import deque

word_list = [
    {
        'original': 'Auto',
        'translations': 'carro',
        'revelvance': 5,
        'knowledge': 5,
    },
    {
        'original': 'Rechner',
        'translations': 'computador/calculadora',
        'revelvance': 4,
        'knowledge': 1
    },
    {
        'original': 'Geige',
        'translations': 'violino',
        'revelvance': 2,
        'knowledge': 1
    },
    {
        'original': 'Katze',
        'translations': 'cat',
        'revelvance': 3,
        'knowledge': 2
    },
    {
        'original': 'Ohrhoerer',
        'translations': 'fones',
        'revelvance': 4,
        'knowledge': 1
    },
    {
        'original': 'Meerjungfrau',
        'translations': 'sereia',
        'revelvance': 1,
        'knowledge': 2
    },
    {
        'original': 'Kater',
        'translations': 'ressaca',
        'revelvance': 2,
        'knowledge': 1
    },
    {
        'original': 'Schwanz',
        'translations': 'cauda',
        'revelvance': 3,
        'knowledge': 1
    },
]


def calculate_new_scores(word_list):
    for word in word_list:
        word['score'] = word.get('score', 0) + word['revelvance'] + (6 - word['knowledge'])

    word_list.sort(key=lambda word: word['score'], reverse=True)

    return word_list


word_list = calculate_new_scores(word_list)
i = 0
while True:
    """ cmd = input('Next day? (y/n):')

    if cmd == 'y':
        word_list = calculate_new_scores(word_list)
    elif cmd != 'n':
        continue """

    i += 1

    print(f"Word: {word_list[0]['original']}: {word_list[0]['translations']}")
    #print({word['original']: word['score'] for word in word_list})
    word_list[0]['score'] = 0
    word_list = deque(word_list)
    word_list.rotate(-1)
    word_list = list(word_list)

    if i%3 == 0:
        input('next day')
        word_list = calculate_new_scores(word_list)
        continue