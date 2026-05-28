from collections import Counter

from schemas.query import QueryRequest, QueryResult
from utils.dataset import Dataset


def run_query(dataset: Dataset, request: QueryRequest, threshold: int) -> QueryResult:
    rows = dataset.rows

    if request.filter:
        rows = tuple(
            row for row in rows
            if all(row.get(k) == v for k, v in request.filter.items())
        )

    counts = Counter(row[request.group_by] for row in rows)

    groups = {
        group: count if count >= threshold else "suppressed"
        for group, count in counts.items()
    }

    return QueryResult(
        groups=groups,
        suppression_triggered=any(v == "suppressed" for v in groups.values()),
    )
