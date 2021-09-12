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
        (
            # https://en.wikipedia.org/wiki/Exact_cover_problem Basic example
            {1, 2, 3, 4},
            {
                "N": [],
                "O": [1, 3],
                "P": [2, 3],
                "E": [2, 4],
            },
            [{"O", "E"}, {"N", "O", "E"}],
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
    ],
)
def test_xcover(target_set, subsets, expected_exact_covers):
    problem = xcover.Problem(target_set=target_set, subsets=subsets)
    found_exact_covers = list(problem.solve())
    print(found_exact_covers)
    for expected in expected_exact_covers:
        assert expected in found_exact_covers
    for found in found_exact_covers:
        assert found in expected_exact_covers
    assert len(found_exact_covers) == len(expected_exact_covers)
