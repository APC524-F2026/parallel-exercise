from pathlib import Path
import time
import subprocess

import matplotlib.pyplot as plt
import pytest

repo_root = Path(__file__).parent.parent


@pytest.fixture
def execute_serial():
    def execute(num_iters: int, divergence_threshold: float, samples_per_axis: int):
        result = subprocess.run(
            [
                "bash",
                "./run_serial.sh",
                f"{num_iters:d}",
                f"{divergence_threshold:.10f}",
                f"{samples_per_axis:d}",
            ],
            cwd=repo_root,
            capture_output=True,
            check=True,
        )
        try:
            return float(result.stdout.decode())
        except ValueError as e:
            e.add_note(
                "You may need to remove other echo/print statements from your code."
            )
            raise e

    return execute


@pytest.fixture
def execute_parallel():
    def execute(
        num_iters: int,
        divergence_threshold: float,
        samples_per_axis: int,
        num_workers: int,
    ):
        result = subprocess.run(
            [
                "bash",
                "./run_parallel.sh",
                f"{num_iters:d}",
                f"{divergence_threshold:.10f}",
                f"{samples_per_axis:d}",
                f"{num_workers:d}",
            ],
            cwd=repo_root,
            capture_output=True,
            check=True,
        )
        try:
            return float(result.stdout.decode())
        except ValueError as e:
            e.add_note(
                "You may need to remove other echo/print statements from your code."
            )
            raise e

    return execute


def test_grid_serial(execute_serial, mandelbrot_area):
    for n in [0, 1, 2, 5, 10, 50]:
        for L in [2, 3]:
            for N in [1, 5, 30, 100]:
                assert execute_serial(n, L, N) == pytest.approx(
                    mandelbrot_area(
                        num_iters=n, divergence_threshold=L, samples_per_axis=N
                    ),
                    abs=1e-6,
                    rel=1e-6,
                ), f'Disagreement for "./run_serial.sh {n} {L} {N}"'


def test_grid_parallel(execute_parallel, mandelbrot_area):
    for n in [0, 1, 2, 5, 10, 50]:
        for L in [2, 3]:
            for N in [1, 5, 30, 100]:
                py_sol = mandelbrot_area(
                    num_iters=n, divergence_threshold=L, samples_per_axis=N
                )
                for workers in [1, 2, 4, 8, 15, 16]:
                    assert execute_parallel(n, L, N, workers) == pytest.approx(
                        py_sol, abs=1e-6, rel=1e-6
                    ), f'Disagreement for "./run_parallel.sh {n} {L} {N} {workers}"'


artifact_fol = repo_root / "_test_artifacts"


def test_large_parallel(execute_parallel):
    n = 1000
    L = 2
    N = 1000

    # ran src/mandelbrot_area.py 1000 2 1000
    expected_value = 1.509975

    num_workers = [1, 2, 3, 4, 6, 8, 10, 12, 14, 16]
    execution_time = []

    for nworkers in num_workers:
        current_time = time.time()
        computed_value = execute_parallel(n, L, N, nworkers)
        time_elapsed = time.time() - current_time

        execution_time.append(time_elapsed)

        assert computed_value == pytest.approx(expected_value, abs=1e-6, rel=1e-6)

    artifact_fol.mkdir(parents=True, exist_ok=True)

    plt.plot(num_workers, execution_time, "-x")
    plt.xlabel("#workers")
    plt.ylabel("runtime (s)")
    plt.title("Execution time vs. Worker count")
    plt.ylim((0,None))
    plt.savefig(artifact_fol / "parallel_runtime.png")
