import cv2
import pickle
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox

#  collect face data
def collect_faces():
    video = cv2.VideoCapture(0)
    facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    if not os.path.exists('data/'):
        os.makedirs('data/')

    faces_data = []
    labels = []

    # input window
    root = tk.Tk()
    root.title("Aadhar Number Entry")

    name_label = tk.Label(root, text="Enter Aadhar Number:")
    name_label.pack(pady=10)

    name_entry = tk.Entry(root, width=30)
    name_entry.pack(pady=10)

    def on_submit():
        nonlocal faces_data, labels

        name = name_entry.get()
        if name.strip() == "":
            messagebox.showwarning("Warning", "Please enter your Aadhar number.")
        else:
            name_entry.config(state=tk.DISABLED)
            submit_button.config(state=tk.DISABLED)
            name_label.config(text="Aadhar Number: " + name)
            i = 0
            while True:
                ret, frame = video.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = facedetect.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    crop_img = frame[y:y + h, x:x + w]
                    resized_img = cv2.resize(crop_img, (50, 50))

                    if len(faces_data) < 100 and i % 10 == 0:
                        faces_data.append(resized_img.flatten())
                        labels.append(name)

                        # Convert image to NumPy array
                        image_array = np.array(resized_img)
                       

                    i += 1
                    cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

                cv2.imshow('frame', frame)
                k = cv2.waitKey(1)
                if k == ord('q') or len(faces_data) >= 100:
                    break

            video.release()
            cv2.destroyAllWindows()

            faces_data = np.array(faces_data)
            labels = np.array(labels)

            # Save  data
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(labels, f)
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces_data, f)

            
            messagebox.showinfo("Success", "Data saved successfully.")

            root.destroy()

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    collect_faces()



