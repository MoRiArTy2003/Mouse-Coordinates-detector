import pyautogui
import time
import csv

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Define the safe zone (example: a rectangle in the center of the screen)
SAFE_ZONE = {
    "left": 100,
    "right": SCREEN_WIDTH - 100,
    "top": 100,
    "bottom": SCREEN_HEIGHT - 100
}

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
    
    next_x = max(0, min(SCREEN_WIDTH - 1, next_x))
    next_y = max(0, min(SCREEN_HEIGHT - 1, next_y))
    
    return (next_x, next_y)

def is_within_safe_zone(x, y):
    return SAFE_ZONE["left"] <= x <= SAFE_ZONE["right"] and SAFE_ZONE["top"] <= y <= SAFE_ZONE["bottom"]

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
                        if not is_within_safe_zone(next_x, next_y):
                            print("\nPredicted position out of safe zone. Terminating.")
                            break
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
