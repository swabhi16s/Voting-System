# Voting-System

## Overview

This project implements an Aadhar-based voting system using face recognition technology. It allows voters to securely cast their votes using their Aadhar number for identification.

## Features

- **Face Recognition**: Voters are identified using facial recognition technology.
- **Aadhar Verification**: Each voter's identity is verified using their Aadhar number.
- **Secure Voting**: Ensures each voter can cast only one vote.
- **User-Friendly Interface**: Simple GUI for voters to cast their votes securely.

## Algorithm Used

The face recognition in this project is implemented using the **K-Nearest Neighbors (KNN)** algorithm. Here's a brief overview of how it works:

1. **Data Collection**: Face images are collected and stored along with corresponding Aadhar numbers during registration.

2. **Training**: The collected face data is used to train a KNN classifier. Each face image is converted into a feature vector (flattened and resized) and labeled with the corresponding Aadhar number.

3. **Prediction**: During the voting process, the face detector captures a live image, detects faces, and extracts features. The trained KNN classifier predicts the Aadhar number associated with the detected face.

4. **Verification**: The predicted Aadhar number is checked against the database to verify the voter's identity. If verified and eligible to vote (hasn't voted before), the voter can proceed to cast their vote.

## Requirements

- Python 3.x
- OpenCV
- tkinter (for GUI)
- numpy
- scikit-learn

## Installation

1. Clone the repository:
git clone https://github.com/swabhi16s/Voting-System.git
cd Voting-System

2. Install dependencies:
-pip install opencv-python
-pip install scikit-learn
-pip install pywin32
-pip install tkinter


## Usage

1. **Data Collection**:
- Run `python capture_faces.py` to collect and store face data along with Aadhar numbers.

2. **Voting Process**:
- Run `python caste_vote.py` to start the Aadhar-based voting system. Follow the instructions on the GUI to cast votes securely.
