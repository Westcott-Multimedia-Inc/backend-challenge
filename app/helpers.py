"""Define helper functions."""
import itertools
import time
from functools import wraps
from typing import List


def timer(func: object, iterations: int = 1) -> object:
    """Print runtime of decorated function.

    Args:
        func: decorated function
        iterations: times a function will be executed to determine its average run time
    Returns:
        Decorator function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            times = []
            for _ in range(iterations):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                times.append(time.perf_counter() - start_time)
            average_run_time = sum(times) / len(times)
            print(
                f"Finished {func.__name__} in {average_run_time:.4f} seconds on average"
            )
            return result

        return wrapper

    return decorator


def get_previous_current_pair(iterable):
    """Make an iterator that yields an (previous, current) tuple per element.

    Returns None if the value does not make sense (i.e. previous before
    first and next after last).
    """
    iterable = iter(iterable)
    prv = None
    cur = next(iterable)
    try:
        while True:
            nxt = next(iterable)
            yield prv, cur
            prv = cur
            cur = nxt
    except StopIteration:
        yield prv, cur


def get_crossed_dates_per_artist(requested_value: int) -> List[dict]:
    """
    Returns all days when any existing artist 'crossed' requested metric value
    and its metric_value on the previous day is lower than the requested
    parameter value.

    :param requested_value: requested metric value to compare with
    :return: List of objects with "artist_id" and "crossings" which passed
            condition
    """
    from app.models import Metric  # avoid circular import

    metric_values = Metric.query.order_by(Metric.artist_id).all()

    result_per_artist = {}

    metric_values = itertools.groupby(
        metric_values, lambda metric: metric.artist_id
    )

    for artist_id, artist_metrics in metric_values:
        for prev, curr in get_previous_current_pair(artist_metrics):
            # Note: assuming previous date means previous Metric item,
            # not the previous calendar day
            if prev and prev.value < requested_value <= curr.value:
                crossed_value_date = curr.date.strftime("%Y-%m-%d")
                try:
                    result_per_artist[artist_id].append(crossed_value_date)
                except KeyError:
                    result_per_artist[artist_id] = [crossed_value_date]
            else:
                try:
                    if result_per_artist[artist_id]: continue
                except KeyError:
                    result_per_artist[artist_id] = []

    return [{'artist_id': key, 'crossings': value}
            for key, value in result_per_artist.items()]
