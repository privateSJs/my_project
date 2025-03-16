from pathlib import PosixPath
from ultralytics import YOLO
from app.utils.logger import logger
from app.config.config import MODEL_TRAINED_PATH
from app.utils.decorators.validator import validate_args

class YoloTrainerConfig:
    _device_list = ["cpu", "gpu"]
    _model_list = ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt"]

    @validate_args()
    def __init__(
        self,
        model_size: str,
        data_yaml: PosixPath,
        epochs: int = 50,
        img_size: int = 640,
        batch_size: int = 16,
        device: str = "cpu",
    ) -> None:
        """Initialization Yolov8 Model."""

        match device:
            case "cpu":
                logger.info("ℹ️ Info: Model will work on the CPU.")
            case "gpu":
                logger.info("ℹ️ Info: Model will work on the GPU.")
            case _:
                logger.warning("⚠️ Warning: Unrecognized device. Using default 'cpu'.")

        # ✅ Jeśli wszystko OK, przypisz wartości
        try:
            self.model = YOLO(model_size)
            self.data_yaml = data_yaml
            self.epochs = epochs
            self.img_size = img_size
            self.batch_size = batch_size
            self.device = device
            self.model_trained_path = MODEL_TRAINED_PATH
        except (TypeError, ValueError) as e:
            logger.error(f"❌ Error: Variable initialization failed!", exc_info=True)
            raise
        else:
            logger.info(f"✅ Model '{model_size}' initialized successfully!")
            logger.info(
                f"✅ Initialization variables in class initialized successfully!"
            )
            print(f"✅ Model '{model_size}' initialized successfully!", end="\n\n")


class YoloTrainer(YoloTrainerConfig):
    def __init__(
        self,
        model_size: str,
        data_yaml: PosixPath,
        epochs: int,
        img_size: int,
        batch_size: int,
        device: str,
    ) -> None:
        """
        Inherits the entire constructor from the configuration class.
        """
        super().__init__(model_size, data_yaml, epochs, img_size, batch_size, device)

    def train(self) -> dict:
        """Training model with delivered datas."""
        print("Starting a training model.")
        train_results = self.model.train(
            data=self.data_yaml,
            epochs=self.epochs,
            imgsz=self.img_size,
            batch=self.batch_size,
            device=self.device,
            project=str(self.model_trained_path),
        )
        return train_results

    def test(
        self,
        image_path: str,
        confidence: float = 0.5,
        save: bool = True,
        show: bool = True,
    ) -> list:
        if not isinstance(image_path, str) or not image_path:
            logger.error("❌ Error: Parameter data_yaml must be provided.")
            raise ValueError(f"Invalid image_path '{image_path}'.")

        __model = YOLO(self.model_trained_path)

        test_results = __model(image_path, conf=confidence, save=save, show=show)
        return test_results
