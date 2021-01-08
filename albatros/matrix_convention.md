# Matrix Convention
It has to be explained how matrices are stored internally. Thus, the structure of multi time evaluations is better understood.

## General Convention
Number of time steps is the first dimension that is indexed
```python
# Scalar case
np.array([x_0, x_1, x_2, x_3, x_4, ...])

# Vector case
np.array([
    [x_0, y_0],
    [x_1, y_1],
    [x_2, y_2],
    ...
])
```

## Matrices
Since matrices need to be multipliable `np.matmul(m1, m2)` they need to be stored in a readable format.

Thus the jacobian looks as the following
```python
np.array([
    [dxdot_dx, dxdot_dy],
    [dydot_dx, dydot_dy],
])
```
and with mutliple time steps
```python
np.array([
    [
        [dxdot_dx_0, dxdot_dy_0],
        [dydot_dx_0, dydot_dy_0],
    ],
    [
        [dxdot_dx_1, dxdot_dy_1],
        [dydot_dx_1, dydot_dy_1],
    ],
    ...
])
```