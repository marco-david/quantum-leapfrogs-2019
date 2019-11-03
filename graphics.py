import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from qutip import *

from train import integrate_model
from serialize import load_t_array, load_simulated_data


def clear():
    plt.clf()
    plt.cla()


def plot_trajectory(t, y_vec, params=None,save=None, show=False):
    clear()

    labels = ['x', 'y', 'z']
    for i in range(3):
        y_component = np.array(y_vec)[:, i]
        plt.plot(t, y_component, label=labels[i])

    plt.legend()
    plt.xlabel("Time $t$")
    plt.ylabel(r"Expectation values $\langle\sigma_\alpha\rangle$")
    if params:
        plt.title(f"$|B| = 1$, $\langle\eta^2\\rangle = {params[0]}$, $\\tau_c = {params[1]}$")

    if save:
        plt.savefig(save)
    if show:
        plt.show()


def plot_simulated_data(data_id, traj_id=0, params=None, save=True, show=False):
    t, traj, _ = load_simulated_data(data_id, traj_id=traj_id)
    save = f'simulation-results/simulation-{data_id}-traj{traj_id}.pdf' if save else None
    plot_trajectory(t, traj, params=params, save=save, show=show)


def integrate_and_plot(models, data_id, params=None):
    t = load_t_array(data_id)

    # Integrate Model
    yi = np.asarray([0.0, 0.0, 1.0])
    kwargs = {'rtol': 1e-10, 'method': 'RK45'}
    # 't_eval': np.linspace(t_span[0], t_span[1], 1000)

    ys = []
    for i, model in enumerate(models):
        ys.append(yi)
        if i is len(models) - 1: break

        hnn_ivp = integrate_model(model, [t[i], t[i + 1]], yi, **kwargs)
        yi = hnn_ivp['y'][:, -1]  # all 3 dimensions, last value

    plot_trajectory(t, ys, params=params,
                    save=f'network-results/model-{data_id}-output-{datetime.now().strftime("%Y-%m-%d-%H:%M")}.pdf')


# === ANIMATION ===


def sphere_plot(data_id):
    # Fix Mayavi Issue from StackOverflow
    #from tvtk.common import configure_input
    #configure_input(m, cs)  # <== will work

    # bola.add_points(pnts,meth='l') # to plot lines

    sphere = Bloch3d()
    sphere.point_color = ['b']
    sphere.vector_color = ['r']
    sphere.point_size = 0.05
    sphere.vector_width = 1

    t, traj, _ = load_simulated_data(data_id=data_id)

    for frame in range(len(t)):
        sphere.clear()
        for i in range(frame):
            point = traj[i]
            sphere.add_points(point, meth='l')
        sphere.add_vectors(traj[frame])
        sphere.save(dirc='temp')

    #sphere.save("tmp.pdf")
    #sphere.show()

if __name__ == '__main__':
    sphere_plot(20)