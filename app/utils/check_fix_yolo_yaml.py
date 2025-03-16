import yaml
from pathlib import Path
from app.config.config import TEST_DIR, TRAIN_DIR, VAL_DIR, YOLO_CONFIG_DIR


def check_and_fix_yolo_yaml():
    """To edit."""
    if not YOLO_CONFIG_DIR.exists():
        print(f"❌ File {YOLO_CONFIG_DIR} does not exist!")
        return

    with open(YOLO_CONFIG_DIR, "r") as file:
        yolo_config = yaml.safe_load(file)

    updated = False
    if not Path(yolo_config.get("train", "")).exists():
        yolo_config["train"] = str(TRAIN_DIR)
        updated = True
    if not Path(yolo_config.get("val", "")).exists():
        yolo_config["val"] = str(VAL_DIR)
        updated = True
    if not Path(yolo_config.get("test", "")).exists():
        yolo_config["test"] = str(TEST_DIR)
        updated = True

    if updated:
        with open(YOLO_CONFIG_DIR, "w") as file:
            yaml.safe_dump(yolo_config, file, default_flow_style=False)
        print("✅ `data.yaml` corrected!")


if __name__ == "__main__":
    check_and_fix_yolo_yaml()
