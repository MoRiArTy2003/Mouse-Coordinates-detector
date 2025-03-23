# import pyautogui
# import time

# def main():
#     try:
#         while True:
#             # Get the current mouse position
#             x, y = pyautogui.position()

#             # Clear the previous output and print the current coordinates
#             print(f"\rMouse Position: X={x}, Y={y}", end="")

#             # Wait for a short interval before getting the next position
#             time.sleep(0.1)

#     except KeyboardInterrupt:
#         print("\nProgram terminated by user.")

# if __name__ == "__main__":
#     main()


# sample 2

# import pyautogui
# import time
# import csv

# def main():
#     csv_filename = "mouse_coordinates.csv"
#     try:
#         with open(csv_filename, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(["Timestamp", "X", "Y"])
            
#             while True:
#                 # Get the current timestamp
#                 timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
#                 # Get the current mouse position
#                 x, y = pyautogui.position()

#                 # Print the current coordinates to the console
#                 print(f"\rMouse Position: X={x}, Y={y}", end="")

#                 # Write the coordinates to the CSV file
#                 writer.writerow([timestamp, x, y])
                
#                 # Wait for a short interval before getting the next position
#                 time.sleep(0.1)

#     except KeyboardInterrupt:
#         print("\nProgram terminated by user.")

# if __name__ == "__main__":
#     main()

# sample 3

# import pyautogui
# import time
# import csv

# def main():
#     csv_filename = "mouse_coordinates.csv"
#     try:
#         with open(csv_filename, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(["Timestamp", "X", "Y"])
            
#             while True:
#                 # Get the current timestamp
#                 timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
#                 # Get the current mouse position
#                 x, y = pyautogui.position()

#                 # Print the current coordinates to the console
#                 print(f"\rMouse Position: X={x}, Y={y}", end="")

#                 # Write the coordinates to the CSV file
#                 writer.writerow([timestamp, x, y])
                
#                 # Flush the file to ensure data is written immediately
#                 file.flush()
                
#                 # Wait for a short interval before getting the next position
#                 time.sleep(0.1)

#     except KeyboardInterrupt:
#         print("\nProgram terminated by user.")

# if __name__ == "__main__":
#     main()

# sample 4
# import pyautogui
# import time
# import csv

# def load_mouse_data(csv_filename):
#     data = []
#     with open(csv_filename, mode='r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the header row
#         for row in reader:
#             data.append((int(row[1]), int(row[2])))  # Extract X, Y coordinates
#     return data

# def predict_next_position(data, current_position):
#     if len(data) < 2:
#         return None
    
#     # Calculate the difference between the current and previous positions
#     prev_x, prev_y = data[-2]
#     dx = current_position[0] - prev_x
#     dy = current_position[1] - prev_y
    
#     # Predict the next position based on the average change
#     next_x = current_position[0] + dx
#     next_y = current_position[1] + dy
    
#     return (next_x, next_y)

# def main():
#     csv_filename = "mouse_coordinates.csv"
#     data = load_mouse_data(csv_filename)
    
#     try:
#         with open(csv_filename, mode='a', newline='') as file:
#             writer = csv.writer(file)
#             while True:
#                 # Get the current timestamp
#                 timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
#                 # Get the current mouse position
#                 x, y = pyautogui.position()

#                 # Print the current coordinates to the console
#                 print(f"\rMouse Position: X={x}, Y={y}", end="")

#                 # Predict the next position
#                 prediction = predict_next_position(data, (x, y))
#                 if prediction:
#                     print(f"\rPredicted Next Position: X={prediction[0]}, Y={prediction[1]}", end="")

#                 # Write the current coordinates to the CSV file
#                 writer.writerow([timestamp, x, y])
#                 file.flush()
                
#                 # Wait for a short interval before getting the next position
#                 time.sleep(0.5)

#     except KeyboardInterrupt:
#         print("\nProgram terminated by user.")

# if __name__ == "__main__":
#     main()

#sample 5
import pyautogui
import time
import csv

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

def load_mouse_data(csv_filename):
    data = []
    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            data.append((int(row[1]), int(row[2])))  # Extract X, Y coordinates
    return data

def predict_next_position(data, current_position):
    if len(data) < 2:
        return None
    
    # Calculate the difference between the current and previous positions
    prev_x, prev_y = data[-2]
    dx = current_position[0] - prev_x
    dy = current_position[1] - prev_y
    
    # Predict the next position based on the average change
    next_x = current_position[0] + dx
    next_y = current_position[1] + dy
    
    # Clamp the next position within the screen boundaries
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
                    # Get the current timestamp
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Get the current mouse position
                    x, y = pyautogui.position()

                    # Print the current coordinates to the console
                    print(f"\rMouse Position: X={x}, Y={y}", end="")

                    # Predict the next position
                    prediction = predict_next_position(data, (x, y))
                    if prediction:
                        next_x, next_y = prediction
                        print(f"\rPredicted Next Position: X={next_x}, Y={next_y}", end="")
                        
                        # Move the mouse to the predicted next position
                        pyautogui.moveTo(next_x, next_y, duration=1)  # Add a slight duration for smooth movement

                    # Write the current coordinates to the CSV file
                    writer.writerow([timestamp, x, y])
                    file.flush()
                    
                    # Append the current position to the data for the next prediction
                    data.append((x, y))
                    
                    # Wait for a short interval before getting the next position
                    time.sleep(0.5)
                
                except pyautogui.FailSafeException:
                    print("\nFail-safe triggered! Moving the mouse to the corner of the screen. Exiting.")
                    break

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()


