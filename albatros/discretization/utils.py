from albatros.core.core import AlbatrosError, assert_that

import numpy as np


def assert_valid_normalized_time(tau, tau_one_required=False):
    """Checks that the normalized time is valid"""

    assert_that(
        tau[0] == 0,
        AlbatrosError(f'Normalized time must start with 0.0 but starts with "{tau[0]}"!'),
    )
    assert_that(
        all(np.diff(tau) > 0),
        AlbatrosError('Normalized must be monotonically increasing strictly!'),
    )

    if tau_one_required:
        assert_that(
            tau[-1] == 1,
            AlbatrosError(f'Normalized time must end with 1.0 but ends with "{tau[-1]}"!'),
        )


def interpolation_indices(root_tau, sub_tau):
    """Calculates the indices of `sub_tau` in `root_tau`"""

    assert_that(
        isinstance(root_tau, np.ndarray),
        AlbatrosError(f'root_tau must be of type numpy.ndarray but is of type "{type(root_tau).__name__}"!'),
    )
    assert_that(
        isinstance(sub_tau, np.ndarray),
        AlbatrosError(f'sub_tau must be of type numpy.ndarray but is of type "{type(sub_tau).__name__}"!'),
    )
    assert_that(
        all(map(lambda x: x in root_tau, sub_tau)),
        AlbatrosError(f'Not all elements of sub_tau "{sub_tau}" are found in "{root_tau}"!'),
    )

    if len(sub_tau) == len(root_tau):
        return np.array(range(0, len(root_tau)))

    # match sub_tau in root_tau
    s_ind = np.searchsorted(root_tau, sub_tau, side='left')
    indices = np.full(root_tau.shape, np.nan)
    indices[s_ind] = s_ind

    # fill gaps
    last_index = 0
    for i in range(0, len(indices)):
        if np.isnan(indices[i]):
            indices[i] = last_index
        else:
            last_index = indices[i]

    return indices
