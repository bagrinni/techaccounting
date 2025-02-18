import re

def convert_sql_file(input_file, output_file):
    # Открываем исходный файл для чтения
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # Открываем файл для записи преобразованных запросов
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines:
            line = line.strip()

            # Пропускаем строки с заголовками и комментариями
            if line.startswith("INSERT INTO") and "VALUES" in line:
                # Попробуем извлечь данные из запроса INSERT INTO
                match = re.search(r"INSERT INTO\s+[^\s]+\s*\((.*)\)\s*VALUES\s*\((.*)\);", line)

                if match:
                    # Извлекаем список полей и значений
                    fields = match.group(1).split(',')
                    values = match.group(2).split(',')

                    # Убираем лишние пробелы и кавычки из значений
                    fields = [field.strip().strip('"').strip("'") for field in fields]
                    values = [value.strip().strip('"').strip("'") for value in values]

                    # Проверим, что количество полей и значений совпадает
                    if len(fields) == len(values):
                        # Преобразуем значения в соответствии с моделью
                        transformed_values = [
                            values[3],  # PHONE_LAST
                            values[3],  # PHONE_4 (если PHONE_LAST 4-значный, используем его)
                            f"92{values[3]}",  # PHONE_6 (формируем из PHONE_4 с префиксом 92)
                            "NULL",  # department_id (если нет данных)
                            values[6] if len(values) > 6 else "NULL",  # port_asl
                            values[7] if len(values) > 7 else "NULL",  # stan
                            values[8] if len(values) > 8 else "NULL",  # lin
                            "NULL",  # address
                            "NULL",  # status_id
                        ]

                        # Формируем новый SQL-запрос
                        new_query = f"INSERT INTO records_phonerecord (phone_last, phone_4, phone_6, department_id, port_asl, stan, lin, address, status_id)\n"
                        new_query += f"VALUES ({', '.join(transformed_values)});\n"

                        # Записываем преобразованный запрос в новый файл
                        outfile.write(new_query)
                    else:
                        print(f"Не совпадает количество полей и значений в запросе: {line}")
                else:
                    print(f"Не удалось найти значения для обработки в строке: {line}")
            elif line.startswith("/") or not line:  # Игнорируем пустые строки и комментарии
                continue
            else:
                print(f"Пропускаем строку, не являющуюся запросом INSERT INTO: {line}")

# Пример использования
convert_sql_file('dep_phone1_cleaned.sql', 'converted_phone_records.sql')
