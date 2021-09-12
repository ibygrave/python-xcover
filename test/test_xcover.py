import xcover

import pytest


@pytest.mark.parametrize(
    "target_set,subsets,expected_exact_covers",
    [
        (
            # https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
            {1, 2, 3, 4, 5, 6, 7},
            {
                "A": [1, 4, 7],
                "B": [1, 4],
                "C": [4, 5, 7],
                "D": [3, 5, 6],
                "E": [2, 3, 6, 7],
                "F": [2, 7],
            },
            [{"B", "D", "F"}],
        ),
        pytest.param(
            # https://en.wikipedia.org/wiki/Exact_cover_problem Basic example
            {1, 2, 3, 4},
            {
                "N": [],
                "O": [1, 3],
                "P": [2, 3],
                "E": [2, 4],
            },
            [{"O", "E"}, {"N", "O", "E"}],
            marks=pytest.mark.xfail(reason="Algorithm X never uses empty subsets"),
        ),
        (
            # https://en.wikipedia.org/wiki/Exact_cover_problem Basic example
            {1, 2, 3, 4},
            {
                "O": [1, 3],
                "P": [2, 3],
                "E": [2, 4],
            },
            [{"O", "E"}],
        ),
        (
            # https://en.wikipedia.org/wiki/Exact_cover_problem Basic example
            {1, 2, 3, 4, 5},
            {
                "N": [],
                "O": [1, 3],
                "P": [2, 3],
                "E": [2, 4],
            },
            [],  # No cover
        ),
        (
            # https://en.wikipedia.org/wiki/Exact_cover_problem Detailed example
            {1, 2, 3, 4, 5, 6, 7},
            {
                "A": [1, 4, 7],
                "B": [1, 4],
                "C": [4, 5, 7],
                "D": [3, 5, 6],
                "E": [2, 3, 6, 7],
                "F": [2, 7],
            },
            [{"B", "D", "F"}],
        ),
        (
            {1, 2, 3, 4},
            {
                "even": [2, 4],
                "odd": [1, 3],
                "small": [1, 2],
                "big": [3, 4],
                "unit": [1],
                "triple": [3],
                "non-unit": [2, 3, 4],
            },
            [{"even", "odd"}, {"small", "big"}, {"unit", "non-unit"}, {"even", "triple", "unit"}],
        ),
    ],
)
def test_xcover(target_set, subsets, expected_exact_covers):
    problem = xcover.Problem(target_set=target_set, subsets=subsets)
    found_exact_covers = list(problem.solve())
    for expected in expected_exact_covers:
        assert expected in found_exact_covers
    for found in found_exact_covers:
        assert found in expected_exact_covers
    assert len(found_exact_covers) == len(expected_exact_covers)
