"""Exact Cover"""
from contextlib import contextmanager


class Solution:
    """Partial solution to an exact cover problem"""

    def __init__(self, problem):
        self.problem = problem
        self.to_cover = self.problem.get_element_covers()
        self.cover = []

    def add_subset(self, subset_name):
        """Start solution with a named subset,
        so that only solutions containing that subset are found."""
        assert subset_name in self.problem.subsets
        self.cover.append(subset_name)

    def is_complete(self):
        """Check if the partial solution covers all elements."""
        return not self.to_cover

    def least_covered_element(self):
        """Find the uncovered element with
        the fewest subsets that can cover it."""

        def covering_subsets(element):
            return len(self.to_cover[element])

        return min(self.to_cover, key=covering_subsets)

    @contextmanager
    def subset_covered(self, subset_name):
        """Context manager for temporarily covering one named subset."""
        self.cover.append(subset_name)
        covered_elements = []
        for element in self.problem.subsets[subset_name]:
            for other_subset_name in self.to_cover[element]:
                for other_element in self.problem.subsets[other_subset_name]:
                    if other_element != element:
                        self.to_cover[other_element].remove(other_subset_name)
            covered_elements.append(self.to_cover.pop(element))
        yield
        for element in reversed(self.problem.subsets[subset_name]):
            self.to_cover[element] = covered_elements.pop()
            for other_subset_name in self.to_cover[element]:
                for other_element in self.problem.subsets[other_subset_name]:
                    if other_element != element:
                        self.to_cover[other_element].add(other_subset_name)
        self.cover.pop()

    def __str__(self):
        return f"{self.cover} {self.to_cover}"


class Problem:
    """One exact cover problem"""

    def __init__(self, target_set, subsets):
        self.target_set = target_set
        self.subsets = subsets

    def get_element_covers(self):
        """Transform the subset->[element] map to element->[subset]"""
        element_covers = {element: set() for element in self.target_set}
        for subset_name, subset in self.subsets.items():
            for element in subset:
                element_covers[element].add(subset_name)
        return element_covers

    def solve(self, solution=None):
        """Generate all solutions of the problem,
        given an optional partial solution."""
        if solution is None:
            solution = Solution(self)

        if solution.is_complete():
            yield set(solution.cover)  # clone
            return

        element = solution.least_covered_element()

        for subset_name in list(solution.to_cover[element]):
            with solution.subset_covered(subset_name):
                yield from self.solve(solution)

    def __str__(self):
        return f"{self.target_set} {self.subsets}"
