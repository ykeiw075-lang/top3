import csv
import sys


def read_participants(path):
    """Читает участников из CSV-файла с разделителем ';'."""
    rows = []

    try:
        with open(path, "r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file, delimiter=";")

            for line_no, row in enumerate(reader, start=1):
                if not row or all(not cell.strip() for cell in row):
                    continue

                if len(row) != 2:
                    raise ValueError(
                        f"строка {line_no}: ожидается 2 поля — имя и вес"
                    )

                rows.append((line_no, row[0].strip(), row[1].strip()))

    except FileNotFoundError:
        raise ValueError(f"файл не найден: {path}")

    return rows


def validate_participants(rows):
    """Проверяет имена и веса участников."""
    if not rows:
        raise ValueError("файл не содержит участников")

    participants = []
    names = set()

    for line_no, name, weight_text in rows:
        if not name:
            raise ValueError(f"строка {line_no}: имя участника не может быть пустым")

        if name in names:
            raise ValueError(f"строка {line_no}: повторяющееся имя — {name}")

        if not weight_text.isdigit():
            raise ValueError(
                f"строка {line_no}: вес должен быть целым положительным числом"
            )

        weight = int(weight_text)

        if weight <= 0:
            raise ValueError(f"строка {line_no}: вес должен быть больше 0")

        names.add(name)
        participants.append((name, weight))

    return participants


def split_bill(total_kopecks, participants):
    """Распределяет сумму между участниками без потери копеек."""
    if total_kopecks < 0:
        raise ValueError("общая сумма не может быть отрицательной")

    if not participants:
        raise ValueError("нет участников для распределения")

    total_weight = sum(weight for _, weight in participants)

    if total_weight <= 0:
        raise ValueError("суммарный вес участников должен быть больше 0")

    base_amounts = {
        name: total_kopecks * weight // total_weight
        for name, weight in participants
    }

    distributed = sum(base_amounts.values())
    remainder = total_kopecks - distributed

    fractional_parts = [
        (
            -(total_kopecks * weight / total_weight),
            name,
            weight
        )
        for name, weight in participants
    ]

    fractional_parts.sort()

    for _, name, _ in fractional_parts[:remainder]:
        base_amounts[name] += 1

    return base_amounts


def save_result(path, amounts):
    """Сохраняет результат в CSV-файл."""
    try:
        with open(path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["участник", "сумма_копеек"])

            for name, amount in amounts.items():
                writer.writerow([name, amount])

    except OSError as e:
        raise ValueError(f"не удалось сохранить результат: {e}")


def main():
    if len(sys.argv) != 4:
        print("Использование:")
        print("python src/main.py <входной_csv> <сумма_в_копейках> <выходной_csv>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[3]

    try:
        total_kopecks = int(sys.argv[2])
    except ValueError:
        print("Ошибка: сумма должна быть целым числом копеек.")
        sys.exit(1)

    try:
        rows = read_participants(input_path)
        participants = validate_participants(rows)
        amounts = split_bill(total_kopecks, participants)

        print("Результат распределения:")
        for name, amount in amounts.items():
            print(f"{name}: {amount} коп.")

        print(f"Общая сумма: {sum(amounts.values())} коп.")

        save_result(output_path, amounts)
        print(f"Результат сохранён в файл: {output_path}")

    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
