import logging
import sys
import os
import math
import traceback

# --- Логирование ---
os.makedirs("Logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | [%(levelname)-7s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("Logs/triangle.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


EPS = 1e-9


def process_triangle(s1, s2, s3):
    # --- Парсинг ---
    try:
        a, b, c = float(s1), float(s2), float(s3)
    except ValueError:
        logger.error(f"Нечисловые данные: {s1}, {s2}, {s3}")
        return "", [(-2, -2)] * 3

    # --- Проверка чисел ---
    if a <= 0 or b <= 0 or c <= 0 or not all(map(math.isfinite, (a, b, c))):
        logger.error(f"Некорректные числа: {a}, {b}, {c}")
        return "", [(-1, -1)] * 3

    # --- Вид треугольника (с эпсилон) ---
    if a + b - c < EPS or a + c - b < EPS or b + c - a < EPS:
        kind = "не треугольник"
        vertices = [(-1, -1)] * 3
    elif abs(a - b) < EPS and abs(b - c) < EPS:
        kind = "равносторонний"
    elif abs(a - b) < EPS or abs(b - c) < EPS or abs(a - c) < EPS:
        kind = "равнобедренный"
    else:
        kind = "разносторонний"

    # --- Координаты ---
    if kind != "не треугольник":
        cx = (b * b + c * c - a * a) / (2 * c)
        cy = math.sqrt(max(b * b - cx * cx, 0))
        pts = [(0, 0), (c, 0), (cx, cy)]

        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        w = max(max(xs) - min(xs), 1)
        h = max(max(ys) - min(ys), 1)
        scale = min(90 / w, 90 / h)
        ox = (100 - w * scale) / 2
        oy = (100 - h * scale) / 2

        vertices = [
            (int((x - min(xs)) * scale + ox), int((y - min(ys)) * scale + oy))
            for x, y in pts
        ]

    logger.info(f"A={a}, B={b}, C={c} → {kind}, {vertices}")
    return kind, vertices


def main():
    logger.info("Приложение запущено")

    while True:
        try:
            s1 = input("Сторона A (или 'q' для выхода): ")
            if s1.strip().lower() in ("q", "quit", "exit", "выход"):
                break

            s2 = input("Сторона B: ")
            s3 = input("Сторона C: ")
        except EOFError:
            logger.error("Не удалось прочитать входные данные (EOF)")
            break

        kind, vertices = process_triangle(s1, s2, s3)

        print(f"Тип треугольника: {kind}")
        print(f"Координаты вершин: {vertices}")
        print()  # пустая строка для читаемости

    logger.info("Приложение завершено")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.critical(traceback.format_exc())
        sys.exit(1)