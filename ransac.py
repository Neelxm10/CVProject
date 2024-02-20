import cv2 as cv
import numpy as np

def ransac(img, threshold, max_iterations, min_inline):
    num_points = np.column_stack(np.where(img > 0))

    if len(num_points) == 0:
        print("No edge points found in the binary image.")
        return None

    accumulator = np.zeros_like(img, dtype=int)
    best_circle = None
    max_inliers = 0

    for i in range(max_iterations):
        sample_index = np.random.choice(len(num_points), size=3)
        sample_points = num_points[sample_index]
        xi, yi = sample_points[:, 1], sample_points[:, 0]

        c = np.array([np.mean(xi), np.mean(yi)])
        r = np.mean(np.sqrt((xi - c[0]) ** 2 + (yi - c[1]) ** 2))

        if 0 <= c[0] < img.shape[1] and 0 <= c[1] < img.shape[0] and 0 < r < min(img.shape[0], img.shape[1]) / 2:
            th = np.arange(0, 2 * np.pi, 0.01)
            a = c[0] + (r * np.cos(th))
            b = c[1] + (r * np.sin(th))

            margin = 5  # Adjust this margin as needed
            a_idx = np.clip(a.astype(int), 0 + margin, img.shape[1] - 1 - margin)
            b_idx = np.clip(b.astype(int), 0 + margin, img.shape[0] - 1 - margin)

            accumulator[b_idx, a_idx] += 1

            # Non-maximal suppression
            accumulator = cv.convertScaleAbs(accumulator)
            local_max = cv.dilate(accumulator, np.ones((3, 3)), iterations=1)
            lmax_mask = (local_max == accumulator)
            accumulator *= lmax_mask

    for max_coords in np.argwhere(accumulator > 0):
        radius = np.mean(np.sqrt((xi - max_coords[1]) ** 2 + (yi - max_coords[0]) ** 2))
        center = (max_coords[1], max_coords[0])

        th = np.arange(0, 2 * np.pi, 0.01)
        x_circle = (center[0] + radius * np.cos(th)).astype(int)
        y_circle = (center[1] + radius * np.sin(th)).astype(int)

        x_circle = np.clip(x_circle, 0, img.shape[1] - 1)
        y_circle = np.clip(y_circle, 0, img.shape[0] - 1)

        inliers = np.sum(img[y_circle, x_circle] > 0)

        if inliers >= min_inline and radius <= threshold and inliers > max_inliers:
            print(f"Found Circle with radius {radius} px and center {center}")
            best_circle = (center, radius)
            max_inliers = inliers

    if best_circle is not None:
        # Visualize the best circle
        circ = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        cv.circle(circ, best_circle[0], int(best_circle[1]), [0, 255, 0], 2)
        cv.circle(circ, best_circle[0], 5, [0, 0, 255], -1)
        cv.putText(circ, f'Center: ({best_circle[0][0]}, {best_circle[0][1]})', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1,
                   (0, 255, 255), 2)

        cv.imshow('Best Circle', circ)
        cv.imwrite("Best_Circle_Detected.png", circ)
        cv.waitKey(20)
        cv.destroyAllWindows()
    else:
        print("No circles found")

    return best_circle