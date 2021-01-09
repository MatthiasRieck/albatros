import albatros as alba
from albatros.solvers.ipopt import IpoptWrapper
import numpy as np
import matplotlib.pyplot as plt
import time


states = [
    alba.State('x', lower_bound=0),
    alba.State('y', lower_bound=0),
    alba.State('v', lower_bound=0),
]

controls = [
    alba.Control('u', lower_bound=0, upper_bound=np.pi),
]

t_final = alba.Parameter('t_final', 5, lower_bound=0)


def model_dynamics(states, controls):
    v = states[2]
    u = controls[0]

    g = 9.81

    x_dot = v * np.sin(u)
    y_dot = v * np.cos(u)
    v_dot = g * np.cos(u)

    states_dot = [x_dot, y_dot, v_dot]
    j_states_dot = [
        [0, 0, np.sin(u), v * np.cos(u)],
        [0, 0, np.cos(u), -v * np.sin(u)],
        [0, 0, 0, -g * np.sin(u)],
    ]

    return states_dot, j_states_dot


problem = alba.Problem('brachistrochone')
tau = np.linspace(0, 1, 1001)

model = alba.Model(model_dynamics, states, jac_sparsity=[[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1]])
phase = problem.add_phase(model, tau)
control_grid = phase.add_controls(controls)
phase.start_time = alba.Parameter('start_time', 0, is_fixed=True)
phase.final_time = t_final
phase.state_grid.set_start_bound(np.array([0, 0, 0]))
phase.state_grid.set_final_bound([5, 0, 0], [5, 4, np.inf])

problem.build()
ipopt = IpoptWrapper(problem)

start = time.time()

res, info = ipopt.solve()
print("hello")
end = time.time()
print(end - start)

x_opt = problem.phases[0].state_grid.values

plt.figure()
plt.plot(x_opt[:, 0], -x_opt[:, 1], '-x')
plt.title('example_brachistochrone')
plt.grid(True)

print(problem.phases[0].final_time.value)
plt.show()
