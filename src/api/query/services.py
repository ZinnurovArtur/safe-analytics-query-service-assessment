from schemas.query import QueryRequest, QueryResult
from utils.dataset import Dataset


def run_query(dataset: Dataset, request: QueryRequest, threshold: int) -> QueryResult:
    rows = dataset.rows

    # Apply exact-match filters before aggregation.
    if request.filter_query:
        filtered = []
        for row in rows:
            if all(
                row.get(column) == value
                for column, value in request.filter_query.items()
            ):
                filtered.append(row)

        rows = filtered

    # Count records for each value in the requested group_by column.
    counts = {}

    for row in rows:
        group_value = row[request.group_by]
        counts[group_value] = counts.get(group_value, 0) + 1

    # Hide counts below the suppression threshold.
    groups = {
        group: count if count >= threshold else "suppressed"
        for group, count in counts.items()
    }

    suppression_triggered = any(value == "suppressed" for value in groups.values())

    return QueryResult(
        groups=groups,
        suppression_triggered=suppression_triggered,
    )
