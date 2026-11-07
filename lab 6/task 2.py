import re
import json


def word_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]


def create_windows(text, size=40, overlap=10, offset=0):
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("Invalid chunk size or overlap")

    spans = word_spans(text)
    chunks = []

    for i in range(0, len(spans), size - overlap):
        end_index = min(i + size, len(spans))
        start = offset + spans[i][0]
        end = offset + spans[end_index - 1][1]

        chunks.append((start, end))

        if end_index == len(spans):
            break

    return chunks


def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("Chunk size must be positive")

    boundaries = [0]
    boundaries += [
        match.end()
        for match in re.finditer(r"[.!?]\s+", text)
    ]
    boundaries.append(len(text))

    result = []
    current_start = None
    current_end = None
    current_words = 0

    for start, end in zip(boundaries, boundaries[1:]):
        sentence = text[start:end]
        word_count = len(sentence.split())

        if word_count == 0:
            continue

        if word_count > size:
            if current_start is not None:
                result.append((current_start, current_end))

            result.extend(create_windows(sentence, size, 0, start))
            current_start = None
            current_end = None
            current_words = 0

        elif current_start is None:
            current_start = start
            current_end = end
            current_words = word_count

        elif current_words + word_count <= size:
            current_end = end
            current_words += word_count

        else:
            result.append((current_start, current_end))
            current_start = start
            current_end = end
            current_words = word_count

    if current_start is not None:
        result.append((current_start, current_end))

    return result


def make_chunks(documents, strategy):
    all_chunks = []

    for doc_id, text in documents.items():

        if strategy == "sentence":
            positions = sentence_chunks(text)

        elif strategy == "0":
            positions = create_windows(text, 40, 0)

        elif strategy == "10":
            positions = create_windows(text, 40, 10)

        else:
            raise ValueError("Strategy must be 0, 10 or sentence")

        for number, (start, end) in enumerate(positions):
            all_chunks.append({
                "id": f"{doc_id}_{strategy}_{number}",
                "doc": doc_id,
                "start": start,
                "end": end,
                "text": text[start:end]
            })

    return all_chunks


def main():
    with open("corpus.json", encoding="utf-8") as file:
        documents = json.load(file)

    print("=" * 60)
    print("TASK 2: TEXT CHUNKING")
    print("=" * 60)

    for strategy in ["0", "10", "sentence"]:
        chunks = make_chunks(documents, strategy)

        word_counts = [len(c["text"].split()) for c in chunks]

        print("\nStrategy:", strategy)
        print("Total chunks:", len(chunks))
        print("Average words:", round(sum(word_counts) / len(word_counts), 2))
        print("Minimum words:", min(word_counts))
        print("Maximum words:", max(word_counts))

        for chunk in chunks[:3]:
            print(
                chunk["id"],
                "Characters:", chunk["start"], "-", chunk["end"]
            )

    assert create_windows("") == []
    assert create_windows("This is a short text") == [(0, 21)]

    try:
        create_windows("one two three", 10, 10)
    except ValueError:
        print("\nInvalid overlap test passed.")

    long_text = " ".join(["example"] * 95) + "."
    long_chunks = sentence_chunks(long_text)

    assert all(len(long_text[a:b].split()) <= 40
               for a, b in long_chunks)

    print("Empty, short, invalid overlap and long sentence tests passed.")


if __name__ == "__main__":
    main()