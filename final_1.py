import pyautogui
import time
import csv

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
    
    return (next_x, next_y)

def main():
    csv_filename = "mouse_coordinates.csv"
    data = load_mouse_data(csv_filename)
    
    try:
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            while True:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
                x, y = pyautogui.position()

                print(f"\rMouse Position: X={x}, Y={y}", end="")

                prediction = predict_next_position(data, (x, y))
                if prediction:
                    print(f"\rPredicted Next Position: X={prediction[0]}, Y={prediction[1]}", end="")

                writer.writerow([timestamp, x, y])
                file.flush()
                
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()