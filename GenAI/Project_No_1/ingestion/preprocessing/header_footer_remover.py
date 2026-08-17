from collections import Counter


def _get_lines(text: str) -> list[str]:
    """
    Convert page text into normalized non-empty lines.

    Input:
        text (str):
            Text extracted from one PDF page.

    Output:
        list[str]:
            Normalized lines from the page.
    """

    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return lines


def detect_headers_and_footers(
    documents: list[dict],
    min_page_ratio: float = 0.5,
    lines_to_check: int = 3
) -> tuple[set[str], set[str]]:
    """
    Detect repeated headers and footers across PDF pages.

    Input:
        documents:
            List of page-level PDF documents.

        min_page_ratio:
            Minimum percentage of pages where a line must appear
            to be considered a header/footer.

        lines_to_check:
            Number of lines from the top and bottom of each page
            to inspect.

    Output:
        tuple:
            (
                detected_headers,
                detected_footers
            )
    """

    page_count = len(documents)

    if page_count == 0:
        return set(), set()

    header_counter = Counter()
    footer_counter = Counter()

    for document in documents:

        lines = _get_lines(document["text"])

        if not lines:
            continue

        # Check first few lines for possible headers
        header_lines = lines[:lines_to_check]

        # Check last few lines for possible footers
        footer_lines = lines[-lines_to_check:]

        for line in header_lines:
            header_counter[line] += 1

        for line in footer_lines:
            footer_counter[line] += 1

    minimum_occurrences = max(
        2,
        int(page_count * min_page_ratio)
    )

    headers = {
        line
        for line, count in header_counter.items()
        if count >= minimum_occurrences
    }

    footers = {
        line
        for line, count in footer_counter.items()
        if count >= minimum_occurrences
    }

    return headers, footers


def remove_headers_and_footers(
    documents: list[dict],
    headers: set[str],
    footers: set[str]
) -> list[dict]:
    """
    Remove detected headers and footers from PDF pages.

    Input:
        documents:
            Page-level PDF documents.

        headers:
            Detected repeated header lines.

        footers:
            Detected repeated footer lines.

    Output:
        list[dict]:
            Documents with headers and footers removed.
    """

    cleaned_documents = []

    for document in documents:

        lines = _get_lines(document["text"])

        filtered_lines = [
            line
            for line in lines
            if line not in headers and line not in footers
        ]

        document["text"] = "\n".join(filtered_lines)

        cleaned_documents.append(document)

    return cleaned_documents