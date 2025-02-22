import os
import cv2
from src.loop.utils.draw import draw_boxes


def get_frame_iterator(video=None, frames_dir=None):
    """
    Returns a frame iterator from either a video file or a directory of images.

    Args:
        video (str, optional): Path to the video file.
        frames_dir (str, optional): Path to the directory containing image frames.

    Returns:
        tuple:
            - generator: An iterator yielding frames.
            - int: The total number of frames.
            - cv2.VideoCapture or None: The video capture object if the input is a video, otherwise None.

    Raises:
        ValueError: If neither `video` nor `frames_dir` is provided or if no valid frames are found.
    """
    if frames_dir:
        valid_extensions = ('.png', '.jpg', '.jpeg')
        frame_files = [
            os.path.join(frames_dir, f)
            for f in sorted(os.listdir(frames_dir))
            if f.lower().endswith(valid_extensions)
        ]
        if not frame_files:
            raise ValueError(f"No valid frames found in folder: {frames_dir}")

        def frame_generator():
            for frame_path in frame_files:
                frame = cv2.imread(frame_path)
                if frame is None:
                    print(f"Could not read frame: {frame_path}")
                    continue
                yield frame

        return frame_generator(), len(frame_files), None

    elif video:
        cap = cv2.VideoCapture(video)
        if not cap.isOpened():
            raise ValueError(f"Unable to open video: {video}")

        def frame_generator():
            while True:
                ret_val, frame = cap.read()
                if not ret_val:
                    break
                yield frame

        return frame_generator(), int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)), cap

    else:
        raise ValueError("Either 'video' or 'frames_dir' must be provided.")


def generate_output_name(video=None, frames_dir=None):
    """
    Generates the output file name based on the input source.

    Args:
        video (str, optional): Path to the video file.
        frames_dir (str, optional): Path to the directory containing image frames.

    Returns:
        str: The generated output file name.

    Raises:
        ValueError: If neither `video` nor `frames_dir` is provided.
    """
    if video:
        base_name = os.path.splitext(os.path.basename(video))[0]
    elif frames_dir:
        base_name = os.path.basename(os.path.dirname(os.path.normpath(frames_dir)))
    else:
        raise ValueError("Either 'video' or 'frames_dir' must be provided.")

    return f"{base_name}_result.avi"


def create_output_writer(output_dir, output_name, width, height):
    """
    Creates a video writer object to save the processed output.

    Args:
        output_dir (str): Directory where the output file will be saved.
        output_name (str): Name of the output video file.
        width (int): Width of the video frames.
        height (int): Height of the video frames.

    Returns:
        cv2.VideoWriter: Video writer object, or None if no `output_dir` is provided.
    """
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_name)
        return cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"XVID"), 30, (width, height))
    return None


def process_frame(frame, model, classes, vid_writer=None, visualize=False):
    """
    Processes a single frame: detects objects, draws bounding boxes, and optionally saves/visualizes the frame.

    Args:
        frame (np.ndarray): The input frame to be processed.
        model (YOLO): YOLO model instance for object detection.
        classes (dict): Dictionary containing class information (tags and colors).
        vid_writer (cv2.VideoWriter, optional): Video writer to save the processed frame. Defaults to None.
        visualize (bool, optional): Whether to display the processed frame in a window. Defaults to False.

    Returns:
        bool: False if the ESC key is pressed during visualization, True otherwise.
    """
    results = model.predict(frame)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
    scores = results[0].boxes.conf.cpu().numpy()
    print(f"Box {boxes}, Class {class_ids}, Score {scores}")
    online_im = draw_boxes(frame.copy(), boxes, class_ids, scores, classes)

    if vid_writer:
        vid_writer.write(online_im)
    if visualize:
        online_im = cv2.resize(online_im, (640, 640))
        cv2.imshow("cam", online_im)
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            return False
    return True
