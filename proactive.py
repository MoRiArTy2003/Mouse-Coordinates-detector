import pyautogui
import time
import csv

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

def load_mouse_data(csv_filename):
    data = []
    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data.append((int(row[1]), int(row[2])))
    return data

def predict_next_position(data, current_position):
    if len(data) < 2:
        return None

    prev_x, prev_y = data[-2]
    dx = current_position[0] - prev_x
    dy = current_position[1] - prev_y

    next_x = current_position[0] + dx
    next_y = current_position[1] + dy

    # Check if the next position is out of screen bounds
    if next_x < 0 or next_x >= SCREEN_WIDTH:
        dx = -dx  # Reverse direction in x-axis
        next_x = current_position[0] + dx

    if next_y < 0 or next_y >= SCREEN_HEIGHT:
        dy = -dy  # Reverse direction in y-axis
        next_y = current_position[1] + dy

    # Ensure next position is within bounds
    next_x = max(0, min(SCREEN_WIDTH - 1, next_x))
    next_y = max(0, min(SCREEN_HEIGHT - 1, next_y))

    return (next_x, next_y)

def main():
    csv_filename = "mouse_coordinates.csv"
    data = load_mouse_data(csv_filename)

    try:
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            while True:
                try:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    x, y = pyautogui.position()
                    print(f"\rMouse Position: X={x}, Y={y}", end="")
                    prediction = predict_next_position(data, (x, y))
                    if prediction:
                        next_x, next_y = prediction
                        print(f"\rPredicted Next Position: X={next_x}, Y={next_y}", end="")
                        pyautogui.moveTo(next_x, next_y, duration=1)
                    writer.writerow([timestamp, x, y])
                    file.flush()
                    data.append((x, y))
                    time.sleep(0.5)
                except pyautogui.FailSafeException:
                    print("\nFail-safe triggered! Moving the mouse to the corner of the screen. Exiting.")
                    break
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()
