import os
import shutil
import pandas as pd
import re

# --- НАСТРОЙКИ ---
data_file = 'NAME.csv' 
source_folder = r'W:\Concentrator\KALConcentrator 2\002 - Maintenance'
target_base_path = r'C:\Users\Kuanysh.Kalken\Documents\Искатель\папка'

def final_collect():
    print("Проверка файлов...")
    if not os.path.exists(data_file):
        print(f"ОШИБКА: Файл {data_file} не найден!")
        return

    # --- СУПЕР-БЛОК ЧТЕНИЯ ---
    df = None
    # Список кодировок для проверки
    encodings = ['utf-8', 'windows-1251', 'cp1251', 'utf-8-sig']
    # Список возможных разделителей
    delimiters = [',', ';', '\t']

    for enc in encodings:
        for sep in delimiters:
            try:
                df = pd.read_csv(data_file, encoding=enc, sep=sep)
                # Проверяем, правильно ли прочитались колонки
                if 'Номер оборудования' in df.columns:
                    print(f"Успех! Кодировка: {enc}, Разделитель: '{sep}'")
                    break
            except:
                continue
        if df is not None and 'Номер оборудования' in df.columns:
            break

    if df is None or 'Номер оборудования' not in df.columns:
        print("ОШИБКА: Не удалось распознать структуру файла.")
        print("Убедись, что в первой строке есть заголовок 'Номер оборудования'.")
        if df is not None:
            print(f"Сейчас я вижу колонки: {list(df.columns)}")
        return
    # -------------------------------

    print(f"Начинаю поиск на диске W. Это займет время...")

    for root, dirs, files in os.walk(source_folder):
        try:
            for file_name in files:
                for index, row in df.iterrows():
                    # Используем названия колонок из твоего файла
                    asset_folder = str(row['Номер оборудования']).strip()
                    tag_no = str(row['Тег номер']).strip()
                    doc_no = str(row['Номер документа']).strip()
                    
                    # Извлекаем GN-111
                    short_tag_match = re.search(r'[A-Z]{2}-\d{3}', tag_no)
                    short_tag = short_tag_match.group() if short_tag_match else "___NONE___"
                    
                    # Извлекаем V0233
                    v_code_match = re.search(r'V\d{4}', doc_no)
                    v_code = v_code_match.group() if v_code_match else "___NONE___"

                    if (tag_no in file_name) or (short_tag in file_name) or (v_code in file_name):
                        dest_dir = os.path.join(target_base_path, asset_folder)
                        
                        if os.path.exists(dest_dir):
                            source_path = os.path.join(root, file_name)
                            dest_path = os.path.join(dest_dir, file_name)
                            
                            if not os.path.exists(dest_path):
                                try:
                                    shutil.copy2(source_path, dest_path)
                                    print(f"[OK] Найдено: {file_name} -> {asset_folder}")
                                except:
                                    pass
        except PermissionError:
            continue
        except Exception:
            continue

    print("\n--- ГОТОВО! Проверяй папки на рабочем столе. ---")

if __name__ == "__main__":
    final_collect()
    input("Нажми Enter, чтобы закрыть...")