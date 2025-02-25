import os
import shutil
from PIL import Image
import imagehash
from tqdm import tqdm

# Dataset dirs path
DATASET_PATH = r""
OUTPUT_PATH = r""

def get_image_hash(image_path):
    """Вычислить перцептивный хэш изображения."""
    try:
        image = Image.open(image_path)
        return imagehash.phash(image)
    except Exception as e:
        print(f"Ошибка обработки {image_path}: {e}")
        return None

def find_duplicates(dataset_path):
    """Поиск дубликатов изображений."""
    hash_dict = {}
    duplicates = []

    for task_folder in os.listdir(dataset_path):
        task_path = os.path.join(dataset_path, task_folder, "images")
        if not os.path.exists(task_path):
            continue

        for img_file in tqdm(os.listdir(task_path), desc=f"Обработка {task_folder}"):
            img_path = os.path.join(task_path, img_file)
            img_hash = get_image_hash(img_path)

            if img_hash is not None:
                if img_hash in hash_dict:
                    duplicates.append((img_path, hash_dict[img_hash]))
                else:
                    hash_dict[img_hash] = img_path

    return duplicates

def remove_duplicates(duplicates, dataset_path, output_path):
    """Удалить дубликаты и их аннотации."""
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for task_folder in os.listdir(dataset_path):
        src_images = os.path.join(dataset_path, task_folder, "images")
        src_labels = os.path.join(dataset_path, task_folder, "labels")
        dst_images = os.path.join(output_path, task_folder, "images")
        dst_labels = os.path.join(output_path, task_folder, "labels")

        # Создаем папки в выходной директории
        os.makedirs(dst_images, exist_ok=True)
        os.makedirs(dst_labels, exist_ok=True)

        # Копируем файлы, исключая дубликаты
        for img_file in os.listdir(src_images):
            img_path = os.path.join(src_images, img_file)
            # Имя текстового файла аннотации (без учета расширения)
            file_base_name = os.path.splitext(img_file)[0]  # Извлекаем имя файла без расширения
            label_path = os.path.join(src_labels, file_base_name + ".txt")

            # Пропускаем дубликаты
            if any(dup[0] == img_path for dup in duplicates):
                continue

            # Копируем изображения и аннотации
            shutil.copy(img_path, dst_images)
            if os.path.exists(label_path):
                shutil.copy(label_path, dst_labels)

# Шаг 1: Найти дубликаты
print("Ищем дубликаты...")
duplicates = find_duplicates(DATASET_PATH)
print(f"Найдено дубликатов: {len(duplicates)}")

# Шаг 2: Удалить дубликаты
print("Удаляем дубликаты...")
remove_duplicates(duplicates, DATASET_PATH, OUTPUT_PATH)
print(f"Фильтрация завершена. Новый датасет сохранен в {OUTPUT_PATH}.")
