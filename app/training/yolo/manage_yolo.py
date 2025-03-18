import argparse
from app.training.yolo.train_model import YoloTrainer
from app.config.config import YOLO_CONFIG_DIR, PREDICT_DIR


if __name__ == "__main__":
    # Create object parser
    parser = argparse.ArgumentParser(description="Automation")

    # Add argument for predicition and training
    parser.add_argument(
        "command",
        choices=["train", "predict"],
        help="""Select the operation mode:
                - train: Start YOLOv8 model training.
                - predict: Run inference on a given image.""",
    )

    # Add argument to pass model size
    parser.add_argument(
        "--model_size",
        choices=["n", "s", "m", "l", "x"],
        type=str,
        default="n",
        help="""Specify the YOLO model size:
                - n: nano
                - s: small
                - m: medium
                - l: large
                - x: extra large
                *** (default: nano) ***""",
    )

    # Add argument to pass number of epochs
    parser.add_argument(
        "--epochs",
        type=int,
        default=25,
        help="Number of training epochs. Higher values improve accuracy but increase training time. (default: 25)",
    )

    # Add argument to pass image-size
    parser.add_argument(
        "--img_size",
        type=int,
        default=640,
        help="Resolution of input images.\nHigher values improve detection accuracy but increase computational cost.",
    )

    # Add argument to pass batch-size
    parser.add_argument(
        "--batch_size",
        type=int,
        default=16,
        help="Number of images processed in one training step.\nHigher values speed up training but require more memory.",
    )

    # Add argument to pass kind of device
    parser.add_argument(
        "--device",
        choices=["cpu", "gpu"],
        type=str,
        default="cpu",
        help="""Select computing device:
                - cpu: Standard processing
                - gpu: Accelerated training and inference
                *** (default: cpu) ***""",
    )

    # Add argument to pass kind of device
    parser.add_argument(
        "--image",
        type=str,
        default=str(PREDICT_DIR),
        help="Path to the image for inference.\nThe model will detect objects in the specified image.",
    )

    # Parsing arguments
    args = parser.parse_args()

    # Initialization trainer
    model = YoloTrainer(
        model_size=f"yolov8{args.model_size}.pt",
        data_yaml=YOLO_CONFIG_DIR,
        epochs=args.epochs,
        img_size=args.img_size,
        batch_size=args.batch_size,
        device=args.device,
    )

    match args.command:
        case "train":
            model.train()
        case "predict":
            model.test(image_path=args.image)
