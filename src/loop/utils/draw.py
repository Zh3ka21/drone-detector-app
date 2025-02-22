import cv2
import numpy as np


def draw_boxes(frame, boxes, class_ids, scores, classes):
    """
    Displays rectangles, class names, probabilities, and colors on the frame
    with improved visualization (transparent labels and thicker boxes).

    Args:
        frame (np.ndarray): An image or frame from a video.
        boxes (list): List of bounding box coordinates [x_min, y_min, x_max, y_max].
        class_ids (list): List of class indices.
        scores (list): List of probabilities for each detection.
        classes (dict): Dictionary containing class information (colors and tags).

    Returns:
        np.ndarray: Frame with bounding boxes and labels drawn.
    """
    overlay = frame.copy()
    for box, class_id, score in zip(boxes, class_ids, scores):
        x_min, y_min, x_max, y_max = map(int, box)

        # Get class information
        class_info = classes.get(class_id, {"color": (0, 255, 0), "tag": f"Class {class_id}"})
        color = class_info["color"]
        tag = class_info["tag"]

        # Draw bounding box with thicker line
        cv2.rectangle(overlay, (x_min, y_min), (x_max, y_max), color, thickness=3)

        # Label with background
        label = f"{tag}: {score:.2f}"
        (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        label_bg_x_min = x_min
        label_bg_y_min = y_min - text_height - 10
        label_bg_x_max = x_min + text_width + 10
        label_bg_y_max = y_min

        # Ensure label background is within the frame bounds
        label_bg_y_min = max(label_bg_y_min, 0)

        # Draw label background rectangle
        cv2.rectangle(overlay, (label_bg_x_min, label_bg_y_min), (label_bg_x_max, label_bg_y_max), color, thickness=-1)

        # Draw label text
        cv2.putText(
            overlay,
            label,
            (x_min + 5, y_min - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            thickness=2,
            lineType=cv2.LINE_AA,
        )

    # Add transparency effect
    alpha = 0.7
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    return frame
