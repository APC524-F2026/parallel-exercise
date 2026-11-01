from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def mandelbrot_area_vectorized(
    num_iters: int, divergence_threshold: float, samples_per_axis: int
):
    dx = 3 / samples_per_axis

    x_sample = -2 + (np.arange(samples_per_axis) + 0.5) * dx
    y_sample = -1.5 + (np.arange(samples_per_axis) + 0.5) * dx

    c = x_sample[:, np.newaxis] + 1.0j * y_sample[np.newaxis, :]

    z = np.zeros(c.shape, dtype=np.complex128)

    inside = np.abs(z) < divergence_threshold
    for _ in range(num_iters):
        z = (z**2 + c) * inside
        inside &= np.abs(z) < divergence_threshold

    return inside


if __name__ == "__main__":
    fig, axs = plt.subplots(nrows=3, ncols=5, figsize=(10, 6))

    resolutions = [3, 5, 10]
    inter_counts = [1, 6, 10, 100, 1000]

    for irow, axrow in enumerate(axs):
        for icol, ax in enumerate(axrow):
            plt.sca(ax)

            samples_per_axis = resolutions[irow]
            num_iters = inter_counts[icol]
            divergence_threshold = 2

            mandelbrot = mandelbrot_area_vectorized(
                num_iters, divergence_threshold, 100
            )

            plt.imshow(
                mandelbrot.T,
                cmap="Reds",
                extent=(-2, 1, -1.5, 1.5),
                vmin=0,
                vmax=1,
                alpha=0.75,
            )

            mandelbrot_discrete = mandelbrot_area_vectorized(
                num_iters, divergence_threshold, samples_per_axis
            ).T
            plt.imshow(
                mandelbrot_discrete,
                cmap="Blues",
                extent=(-2, 1, -1.5, 1.5),
                vmin=0,
                vmax=1,
                alpha=0.5,
            )

            pts_grid = np.zeros((2, 2 * (samples_per_axis - 1), 2))
            pts_grid[:, : samples_per_axis - 1, 0] = np.linspace(
                -2, 1, samples_per_axis + 1
            )[1:-1]
            pts_grid[:, samples_per_axis - 1 :, 1] = np.linspace(
                -1.5, 1.5, samples_per_axis + 1
            )[1:-1]
            pts_grid[:, : samples_per_axis - 1, 1] = np.array([-1.5, 1.5])[:, None]
            pts_grid[:, samples_per_axis - 1 :, 0] = np.array([-2, 1])[:, None]
            plt.plot(pts_grid[..., 0], pts_grid[..., 1], "k")

            dx = 3 / samples_per_axis
            x_sample = -2 + (np.arange(samples_per_axis) + 0.5) * dx
            y_sample = -1.5 + (np.arange(samples_per_axis) + 0.5) * dx
            X, Y = np.meshgrid(x_sample, y_sample)
            plt.scatter(X[~mandelbrot_discrete], Y[~mandelbrot_discrete], 5, color="k")
            plt.scatter(X[mandelbrot_discrete], Y[mandelbrot_discrete], 5, color="b")

            plt.title(
                "$M_{%d}^{%.0f}$ (N = %d)\nArea = %.4f"
                % (
                    num_iters,
                    divergence_threshold,
                    samples_per_axis,
                    np.count_nonzero(mandelbrot_discrete) * dx**2,
                )
            )

    fig.tight_layout()
    plt.savefig(Path(__file__).parent / "area_demo.png")
