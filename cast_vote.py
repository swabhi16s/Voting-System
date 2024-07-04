import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import pickle
import os
import csv
import time
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
from win32com.client import Dispatch

def check_if_exists(value):
    try:
        with open("Votes.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0] == value:
                    return True
    except FileNotFoundError:
        print("File not found or unable to open the CSV file.")
    return False

def record_vote(voter_id, party, date, timestamp):
    COL_NAMES = ['NAME', 'VOTE', 'DATE', 'TIME']
    exist = os.path.isfile("Votes.csv")
    if exist:
        with open("Votes.csv", "+a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            attendance = [voter_id, party, date, timestamp]
            writer.writerow(attendance)
    else:
        with open("Votes.csv", "+a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(COL_NAMES)
            attendance = [voter_id, party, date, timestamp]
            writer.writerow(attendance)

# Function for speech synthesis
def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

def give_vote():
    video = cv2.VideoCapture(0)
    facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    if not os.path.exists('data/'):
        os.makedirs('data/')

    # Load existing data
    with open('data/names.pkl', 'rb') as f:
        LABELS = pickle.load(f)
    with open('data/faces_data.pkl', 'rb') as f:
        FACES = pickle.load(f)

    # Reshape FACES to match the number of labels
    FACES = np.reshape(FACES, (len(LABELS), -1))

    # Fit KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(FACES, LABELS)

    video.release()
    cv2.destroyAllWindows()

    # Voting system
    video = cv2.VideoCapture(0)

    def on_vote(party_name):
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        exist = os.path.isfile("Votes.csv")

        voter_id = output_label["text"]
        voter_exist = check_if_exists(voter_id)

        if voter_exist:
            speak("YOU HAVE ALREADY VOTED")
            root.destroy()
           
        else:
            speak("YOUR VOTE HAS BEEN RECORDED")
            record_vote(voter_id, party_name, date, timestamp)
            speak("THANK YOU FOR PARTICIPATING IN THE ELECTIONS")
            
            root.destroy()  

    def detect_face():
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            crop_img = frame[y:y + h, x:x + w]
            resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
            output = knn.predict(resized_img)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

            output_label.config(text=str(output[0]))

        
        img = cv2.resize(frame, (640, 480))
        img = tk.PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())
        panel.configure(image=img)
        panel.image = img

        root.after(10, detect_face)

    root = tk.Tk()
    root.title("Voting System")

    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack()

    panel = tk.Label(main_frame)
    panel.pack(padx=10, pady=10)

    output_label = tk.Label(main_frame, text="", font=("Helvetica", 24))
    output_label.pack(pady=20)

    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(pady=10)

    vote_btn1 = tk.Button(btn_frame, text="BJP", width=10, height=2, font=("Helvetica", 14), command=lambda: on_vote("BJP"))
    vote_btn1.pack()

    vote_btn2 = tk.Button(btn_frame, text="CONGRESS", width=10, height=2, font=("Helvetica", 14), command=lambda: on_vote("CONGRESS"))
    vote_btn2.pack()

    vote_btn3 = tk.Button(btn_frame, text="AAP", width=10, height=2, font=("Helvetica", 14), command=lambda: on_vote("AAP"))
    vote_btn3.pack()

    vote_btn4 = tk.Button(btn_frame, text="NOTA", width=10, height=2, font=("Helvetica", 14), command=lambda: on_vote("NOTA"))
    vote_btn4.pack()

    detect_face()
    root.mainloop()

if __name__ == "__main__":
    give_vote()





