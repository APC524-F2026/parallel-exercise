def mandelbrot_area(num_iters: int, divergence_threshold: float, samples_per_axis: int):
    dx = 3.0 / samples_per_axis

    num_cells_inside = 0
    for ix in range(samples_per_axis):
        x = -2 + (0.5 + ix) * dx
        for iy in range(samples_per_axis):
            y = -1.5 + (0.5 + iy) * dx
            c = complex(x, y)

            z = 0
            broke_free = abs(z) > divergence_threshold
            for _ in range(num_iters):
                z = z**2 + c
                if abs(z) > divergence_threshold:
                    broke_free = True
                    break

            if not broke_free:
                num_cells_inside += 1

    return num_cells_inside * dx**2


if __name__ == "__main__":
    import sys

    num_iters = int(sys.argv[1])
    divergence_threshold = float(sys.argv[2])
    samples_per_axis = int(sys.argv[3])

    print(f"{mandelbrot_area(num_iters, divergence_threshold, samples_per_axis):.15f}")
