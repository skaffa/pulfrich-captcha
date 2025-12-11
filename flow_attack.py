import cv2
import numpy as np
from pathlib import Path
import imageio.v3 as iio

def load_video_frames(path):
    frames = []
    for frame in iio.imiter(path):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frames.append(gray.astype(np.uint8))
    return frames  # list of (H,W)


def compute_flow_stack(frames):
    flows = []
    for i in range(len(frames) - 1):
        f1 = frames[i]
        f2 = frames[i + 1]

        flow = cv2.calcOpticalFlowFarneback(
            f1, f2,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=13,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0
        )
        flows.append(flow)
    return np.stack(flows)  # (T-1, H, W, 2)


def flow_magnitude_map(flow_stack):
    mag = np.sqrt(flow_stack[..., 0]**2 + flow_stack[..., 1]**2)
    return np.mean(mag, axis=0)  # average magnitude over time


def save_map(img, out):
    img_norm = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    img8 = img_norm.astype(np.uint8)
    cv2.imwrite(out, img8)
    print("[+] Saved:", out)


if __name__ == "__main__":
    video_path = Path("./captcha.avi")  # change to your file
    frames = load_video_frames(video_path)

    print("[*] Computing optical flow...")
    flows = compute_flow_stack(frames)

    print("[*] Computing magnitude map...")
    mag_map = flow_magnitude_map(flows)

    save_map(mag_map, "flow_result.png")
    print("[+] Done.")
