import inspect

import theano
import numpy as np
from scipy.sparse import issparse


__all__ = ('format_data', 'does_layer_accept_1d_feature', 'asfloat',
           'AttributeKeyDict', 'is_list_of_integers', 'preformat_value',
           'as_array2d', 'NotTrainedException')


class NotTrainedException(Exception):
    """ Exception needs for cases when algorithm is not trained
    and can not be applied.
    """


def format_data(data, is_feature1d=True, copy=False):
    """ Transform data in a standardized format.

    Notes
    -----
    It should be applied to the input data prior to use in
    learning algorithms.

    Parameters
    ----------
    data : array-like
        Data that should be formated. That could be, matrix, vector or
        Pandas DataFrame instance.
    is_feature1d : bool
        Should be equal to ``True`` if input data if a vector that
        contains n samples with 1 feature each. Defaults to ``True``.
    copy : bool
        Defaults to ``False``.

    Returns
    -------
    ndarray
        The same input data but transformed to a standardized format
        for further use.
    """
    if data is None or issparse(data):
        return data

    data = np.array(asfloat(data), copy=copy)

    # Valid number of features for one or two dimentions
    n_features = data.shape[-1]

    if data.ndim == 1:
        data_shape = (n_features, 1) if is_feature1d else (1, n_features)
        data = data.reshape(data_shape)

    return data


def does_layer_accept_1d_feature(layer):
    """ Check if 1D feature values are valid for the layer.

    Parameters
    ----------
    layer : object

    Returns
    -------
    bool
    """
    return (layer.size == 1)


def asfloat(value):
    """ Convert variable to float type configured by theano
    floatX variable.

    Parameters
    ----------
    value : matrix, ndarray or scalar
        Value that could be converted to float type.

    Returns
    -------
    matrix, ndarray or scalar
        Output would be input value converted to float type
        configured by theano floatX variable.
    """

    if isinstance(value, (np.matrix, np.ndarray)):
        return value.astype(theano.config.floatX)

    elif issparse(value):
        return value

    float_x_type = np.cast[theano.config.floatX]
    return float_x_type(value)


class AttributeKeyDict(dict):
    """ Modified built-in Python ``dict`` class. That modification
    helps get and set values like attributes.

    Examples
    --------
    >>> attrdict = AttributeKeyDict()
    >>> attrdict
    {}
    >>> attrdict.test_key = 'test_value'
    >>> attrdict
    {'test_key': 'test_value'}
    >>> attrdict.test_key
    'test_value'
    """

    def __getattr__(self, attrname):
        return self[attrname]

    def __setattr__(self, attrname, value):
        self[attrname] = value

    def __delattr__(self, attrname):
        del self[attrname]


def is_list_of_integers(sequence):
    """ Check that sequence contains only integer numbers.

    Parameters
    ----------
    sequence : list, tuple
        Array that should be validated.

    Returns
    -------
    bool
        Result would be ``True`` only if each element in a sequence contains
        is an integer. ``False`` otherwise.
    """
    return all(isinstance(element, int) for element in sequence)


def preformat_value(value):
    """ Function pre-format input value depence on it's type.

    Parameters
    ----------
    value : object

    Returns
    -------
    object
    """
    if inspect.isfunction(value) or inspect.isclass(value):
        return value.__name__

    elif isinstance(value, (list, tuple, set)):
        return [preformat_value(v) for v in value]

    elif isinstance(value, (np.ndarray, np.matrix)):
        return value.shape

    return value


def as_array2d(array):
    """ Transform any array to 2D.

    Parameters
    ----------
    array : array-like

    Returns
    -------
    array-like
        The same array transformed to 2D.
    """
    if array.ndim == 1:
        return array.reshape((1, -1))

    n_samples, feature_shape = array.shape[0], array.shape[1:]
    return array.reshape((n_samples, np.prod(feature_shape)))
