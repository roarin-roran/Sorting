def list_of_words_dickens():
    """Return a list of words from the Bible"""
    with open('Inputs/dickens.txt', 'rb') as f:
        return f.read().split()


def list_of_words_bible():
    """Return a list of words from the Bible"""
    with open('Inputs/bible.txt', 'r') as f:
        return f.read().split()


if __name__ == '__main__':
    words = list_of_words_bible()
    print(words[:10])
    print(words[-10:])
    print(len(words))
    print(len(set(words)))
    print(sorted(words)[:10])
