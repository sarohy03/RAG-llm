def creating_chunks(text,chunks=1000):
    result = []
    while len(text) > chunks:
        chunk = text[:chunks]
        result.append(chunk)
        text = text[chunks:]

    if len(text) > 0:
        result.append(text)
    return result



