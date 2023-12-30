from django_filters import rest_framework as filters

from health.models import WeightRecord


class WeightRecordFilterSet(filters.FilterSet):
    """
    Filter set for querying WeightRecord instances based on specific criteria.

    Filters:
    - `cow`: A filter for the cow associated with the weight record (case-insensitive contains search).
    - `day_of_weighing`: An exact match filter for the day of the weighing date.
    - `month_of_weighing`: An exact match filter for the month of the weighing date.
    - `year_of_weighing`: An exact match filter for the year of the weighing date.

    Meta:
    - `model`: The WeightRecord model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'cow', 'day_of_weighing', 'month_of_weighing', and 'year_of_weighing'.

    Usage:
        Use this filter set to apply filters when querying the list of WeightRecord instances.
        For example, to retrieve all weight records for a specific cow.

    Example:
        ```
        /api/weight_records/?cow=123
        ```
    """

    cow = filters.CharFilter(field_name="cow", lookup_expr="icontains")
    day_of_weighing = filters.NumberFilter(
        field_name="date_taken__day", lookup_expr="exact"
    )
    month_of_weighing = filters.NumberFilter(
        field_name="date_taken__month", lookup_expr="exact"
    )
    year_of_weighing = filters.NumberFilter(
        field_name="date_taken__year", lookup_expr="exact"
    )

    class Meta:
        model = WeightRecord
        fields = [
            "cow",
            "day_of_weighing",
            "month_of_weighing",
            "year_of_weighing",
        ]

