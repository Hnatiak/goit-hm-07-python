import os
import shutil

# Функція для перейменування файлів та папок
def normalize(name):
    # Транслітерація кирилічних символів
    name = name.replace('а', 'a').replace('б', 'b').replace('в', 'v').replace('г', 'h').replace('д', 'd')
    # Інші заміни
    for char in name:
        if not char.isalnum():
            name = name.replace(char, '_')
    return name

# Функція для обробки папки
def process_folder(folder_path, target_path):
    try:
        items = os.listdir(folder_path)
        for item in items:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                # Якщо це папка, рекурсивно обробляємо її
                process_folder(item_path, target_path)
            else:
                # Якщо це файл, отримуємо розширення
                file_extension = item.split('.')[-1].lower()
                if file_extension in ('jpg', 'jpeg', 'png', 'svg'):
                    shutil.move(item_path, os.path.join(target_path, 'images', normalize(item)))
                elif file_extension in ('avi', 'mp4', 'mov', 'mkv'):
                    shutil.move(item_path, os.path.join(target_path, 'video', normalize(item)))
                elif file_extension in ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'):
                    shutil.move(item_path, os.path.join(target_path, 'documents', normalize(item)))
                elif file_extension in ('mp3', 'ogg', 'wav', 'amr'):
                    shutil.move(item_path, os.path.join(target_path, 'audio', normalize(item)))
                elif file_extension in ('zip', 'gz', 'tar'):
                    archive_name = item.split('.')[0]
                    shutil.unpack_archive(item_path, os.path.join(target_path, 'archives', normalize(archive_name)))
                else:
                    shutil.move(item_path, os.path.join(target_path, 'unknown', normalize(item)))
        # Видаляємо порожні папки
        for item in items:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path) and not os.listdir(item_path):
                os.rmdir(item_path)
    except Exception as e:
        print(f"Виникла помилка при обробці папки {folder_path}: {str(e)}")

# Основна функція для сортування папки
def sort_folder(source_folder):
    try:
        # Створюємо цільову папку та підпапки
        target_folder = os.path.join(source_folder, 'sorted')
        os.makedirs(target_folder, exist_ok=True)
        subfolders = ['images', 'video', 'documents', 'audio', 'archives', 'unknown']
        for subfolder in subfolders:
            os.makedirs(os.path.join(target_folder, subfolder), exist_ok=True)
        # Обробляємо папку
        process_folder(source_folder, target_folder)
        print("Сортування завершено.")
    except Exception as e:
        print(f"Виникла помилка при сортуванні папки: {str(e)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Потрібно вказати лише шлях до папки для сортування.")
    else:
        source_folder = sys.argv[1]
        sort_folder(source_folder)
