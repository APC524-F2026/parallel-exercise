import pytest


def test_known(mandelbrot_area):
    for n in range(10):
        for L in range(1, 10):
            assert mandelbrot_area(
                num_iters=n, divergence_threshold=L, samples_per_axis=1
            ) == pytest.approx(9), (
                "single cell, point at -0.5 will max out at 0.5 magnitude"
            )

    # from figure
    for n, L, N, area in [
        (1, 2, 3, 9),
        (6, 2, 3, 2),
        (10, 2, 3, 2),
        (1,2,5,8.28),
        (6,2,5,2.88),
        (10,2,5,2.88),
        (100,2,5,2.88),
    ]:
        assert mandelbrot_area(
            num_iters=n, divergence_threshold=L, samples_per_axis=N
        ) == pytest.approx(area, abs=1e-10, rel=1e-10)
