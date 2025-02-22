import cv2
from ultralytics import YOLO
from src.loop.utils.process import get_frame_iterator, generate_output_name, create_output_writer, process_frame


def run_tracking(
    model: YOLO,
    video: str = None,
    frames_dir: str = None,
    output_dir: str = None,
    visualize=False,
    classes=None
):
    """
    Tracks objects in the input video or frames and visualizes predictions.

    Args:
        model (YOLO): YOLO model instance for object detection.
        video (str, optional): Path to the video file. Defaults to None.
        frames_dir (str, optional): Path to the directory containing image frames. Defaults to None.
        output_dir (str, optional): Directory to save the processed video. Defaults to None.
        visualize (bool, optional): Whether to visualize the predictions in real-time. Defaults to False.
        classes (dict, optional): Dictionary containing class information (tags and colors). Defaults to None.
    """
    if visualize:
        cv2.namedWindow("cam", cv2.WINDOW_NORMAL)

    try:
        frame_iterator, total_frames, cap = get_frame_iterator(video=video, frames_dir=frames_dir)

        vid_writer = None
        output_name = generate_output_name(video=video, frames_dir=frames_dir)

        for frame_id, frame in enumerate(frame_iterator):
            if vid_writer is None and output_dir:
                height, width, _ = frame.shape
                vid_writer = create_output_writer(output_dir, output_name, width, height)

            if not process_frame(frame, model, classes, vid_writer, visualize):
                break

        if cap:
            cap.release()

        if visualize:
            cv2.destroyAllWindows()
        if vid_writer:
            vid_writer.release()
            print(f"Processed video saved as {output_name} in {output_dir}")

    except ValueError as e:
        print(e)
