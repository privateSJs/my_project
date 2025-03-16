# 🔥 Training parameters
VENV_PATH=$(PWD)/.venv/bin/python
TRAIN_SCRIPT=app.training.yolo.start_train_yolo
FIX_YOLO_SCRIPT = app.utils.check_fix_yolo_yaml
PREDICT_IMAGE?=assets

# ✅ Uruchomienie treningu YOLO
train:
	$(VENV_PATH) -m $(FIX_YOLO_SCRIPT)
	$(VENV_PATH) -m $(TRAIN_SCRIPT) train $(ARGS)

# ✅ Predykcja na nowym obrazie
predict:
	$(VENV_PATH) -m $(TRAIN_SCRIPT) predict --image=$(TEST_IMAGE) $(ARGS)

# ✅ Szczegółowa pomoc z argparse
help-args:
	$(VENV_PATH) -m $(TRAIN_SCRIPT) --help

# ✅ Czyszczenie wyników treningu
clean:
	@echo "🧹 Cleaning all runs/ and detect/ directories..."
	@find . -type d \( -name "runs" -o -name "detect" \) -exec rm -rf {} +
	@echo "✅ Cleanup complete."

# ✅ Pomoc - podstawowa dokumentacja
help:
	@echo "🔥 Available Commands:"
	@echo ""
	@echo "  🚀 Training YOLO:"
	@echo "    make train ARGS='--model_size=s --epochs=50 --batch_size=32 --device=gpu'"
	@echo "      → Train YOLOv8 with specified parameters."
	@echo ""
	@echo "    ⚙️ **Default values (if not specified in ARGS):**"
	@echo "      --model_size=n            (nano model)"
	@echo "      --epochs=25               (default: 25 epochs)"
	@echo "      --img_size=640            (image resolution: 640px)"
	@echo "      --batch_size=16           (batch size: 16)"
	@echo "      --device=cpu              (uses CPU by default)"
	@echo "      --data_yaml=YOLO_CONFIG_DIR (dataset configuration, default set in config file)"
	@echo ""
	@echo "    📌 **Note:**"
	@echo "      The 'data_yaml' file is set **only** in the configuration file: `config/config.py`"
	@echo "      → The dataset configuration **cannot** be passed as an argument in 'make train'."
	@echo ""
	@echo "  🔎 **Run inference:**"
	@echo "    make predict TEST_IMAGE=path/to/image.jpg"
	@echo "      → Run object detection on a specified image."
	@echo ""
	@echo "  🧹 **Clean previous runs:**"
	@echo "    make clean"
	@echo "      → Automatically removes all 'runs/' and 'detect/' directories in the project."
	@echo ""
	@echo "📌 **To see available arguments for training and prediction, run:**"
	@echo "    make help-args"
