import os
import cv2


def preprocess_images(input_folder_path, output_folder_path, target_size=(640, 384)):
    # Tworzymy katalog wyjściowy, jeśli nie istnieje
    os.makedirs(output_folder_path, exist_ok=True)

    # Pobieramy listę plików w katalogu wejściowym
    images = os.listdir(input_folder_path)

    for image_name in images:
        # Pełna ścieżka do obrazu wejściowego
        input_image_path = os.path.join(input_folder_path, image_name)

        # Wczytanie obrazu
        image = cv2.imread(input_image_path)
        if image is None:
            print(f"❌ Błąd: Nie udało się wczytać {input_image_path}")
            continue  # Pominięcie błędnego pliku

        # Skalowanie obrazu
        resized_image = cv2.resize(image, target_size)

        # Pełna ścieżka do zapisu obrazu wyjściowego
        output_image_path = os.path.join(output_folder_path, image_name)

        # Zapisujemy przetworzony obraz
        cv2.imwrite(output_image_path, resized_image)
        print(f"✅ Przetworzono: {input_image_path} -> {output_image_path}")

    print("🎉 Wszystkie obrazy zostały przeskalowane!")


preprocess_images(
    input_folder_path="/home/jarek9917/Dokumenty/MasterDegree/my_project/app/assets/preprocessed",
    output_folder_path="/home/jarek9917/Dokumenty/MasterDegree/my_project/app/assets/resized",
)
