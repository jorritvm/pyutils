import numpy as np

__all__ = [
    "detect_vector_interpolation",
]

def detect_vector_interpolation(vector: np.ndarray, sequence_length: int=5, tolerance=1e-5) -> (bool, np.ndarray):
    """
    Detects if a vector contains at least one segment of linear interpolation of at least sequence_length.
    A segment is considered linearly interpolated if the difference between consecutive elements
    is constant within a given tolerance.
    Args:
        vector (np.ndarray): The input vector to analyze.
        sequence_length (int): The minimum length of a linear interpolation segment to detect.
        tolerance (float): The tolerance within which differences are considered equal.
    Returns:
        tuple: A tuple containing:
            - bool: True if at least one interpolated segment of at least sequence_length is found
            - np.ndarray: A mask array of the same length as vector, with 1s indicating positions
                          that are part of an interpolated segment and 0s otherwise.
    """

    # short circuit for short vectors
    if vector is None:
        raise ValueError("vector is None")
    if sequence_length <= 2:
        raise ValueError('sequence_length must be greater than 2')
    if len(vector) < sequence_length:
        return False, np.zeros(len(vector), dtype=int)

    has_interpolated_segment = False
    mask = np.zeros(len(vector), dtype=int)
    current_sequence_length = 2
    for i, value in enumerate(vector):
        if i == 0:
            continue

        current_step = value - vector[i - 1]

        # skip ahead for first value, no previous step to compare to
        if i == 1:
            previous_step = current_step
            continue

        if abs(current_step - previous_step) < tolerance:
            # if the step is the same as the previous step within tolerance, we are potentially in linear interpollation
            current_sequence_length += 1

            # if the last value of the vector is still part of a sequence, we need to wrap it up here
            if i == len(vector) - 1:
                if current_sequence_length >= sequence_length:
                    has_interpolated_segment = True
                    mask[i - current_sequence_length + 1 : i + 1] = 1
        else:
            # if the step is different, wrap up the previous sequence
            if current_sequence_length >= sequence_length:
                has_interpolated_segment = True
                mask[i - current_sequence_length : i] = 1

            # start a new sequence
            current_sequence_length = 2  # reset to 2 because we have a new step
            previous_step = current_step

    return has_interpolated_segment, mask