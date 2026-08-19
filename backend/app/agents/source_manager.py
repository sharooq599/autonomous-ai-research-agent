from app.schemas.source import Source


def deduplicate_sources(
    sources: list[dict]
) -> list[dict]:

    unique_sources = []

    seen_urls = set()

    source_id = 1

    for source in sources:

        title = source.get(
            "title",
            ""
        ).strip()

        url = source.get(
            "url",
            ""
        ).strip()

        if not url:
            continue

        # Normalize URL
        normalized_url = url.rstrip("/")

        # Skip duplicate URLs
        if normalized_url in seen_urls:
            continue

        seen_urls.add(
            normalized_url
        )

        unique_sources.append(
            Source(
                id=source_id,
                title=title,
                url=normalized_url
            ).model_dump()
        )

        source_id += 1

    return unique_sources