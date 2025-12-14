import numpy as np
import pytest
from pyutils.vectors import detect_vector_interpolation


def test_single_interpolated_section():
    v = np.array([1, 9, 1, 2, 3, 4, 5, 1, 9])
    has_segment, mask = detect_vector_interpolation(v, 3)
    assert has_segment is True
    # The interpolated segment is [1,2,3,4,5] (indices 2-6)
    expected_mask = np.array([0, 0, 1, 1, 1, 1, 1, 0, 0])
    assert np.array_equal(mask, expected_mask)


def test_no_interpolated_section_due_to_length():
    v = np.array([1, 9, 1, 2, 3, 4, 5, 1, 9])
    has_segment, mask = detect_vector_interpolation(v, 6)
    assert has_segment is False
    assert np.all(mask == 0)


def test_two_distinct_interpolated_sections():
    v = np.array([5, 5, 5, 9, 1, 2, 3, 4, 5, 0, 5, 5, 5])
    has_segment, mask = detect_vector_interpolation(v, 3)
    # There are three segments: [5,5,5] (0-2), [1,2,3,4,5] (4-8), [5,5,5] (10-12)
    expected_mask = np.array([1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1])
    assert has_segment is True
    assert np.array_equal(mask, expected_mask)


def test_with_random_noise():
    import random
    v = np.array([1, 2, 3, 4, 5, 9, 1, 2, 3, 8], dtype=float)
    v_noisy = np.array([x + random.uniform(-0.00001, 0.00001) for x in v])
    has_segment, mask = detect_vector_interpolation(v_noisy, 3, tolerance=1e-4)
    # The first five values are nearly linear, and [1,2,3] (indices 6-8) is also linear
    expected_mask = np.array([1, 1, 1, 1, 1, 0, 1, 1, 1, 0])
    assert has_segment is True
    assert np.array_equal(mask, expected_mask)


def test_empty_vector():
    v = np.array([])
    has_segment, mask = detect_vector_interpolation(v, 3)
    assert has_segment is False
    assert mask.size == 0


def test_single_element_vector():
    v = np.array([1])
    has_segment, mask = detect_vector_interpolation(v, 3)
    assert has_segment is False
    assert np.all(mask == 0)


def test_two_element_vector():
    v = np.array([1, 1])
    has_segment, mask = detect_vector_interpolation(v, 3)
    assert has_segment is False
    assert np.all(mask == 0)
