# Web Chat App

## Overview

The **Web Chat App** is a real-time messaging application designed to facilitate seamless communication between users and increase focus on productivity by eliminating spam and ditracting messages. Built with modern web technologies, this project demonstrates the use of WebSockets for real-time chat functionality and includes a user-friendly interface for engaging conversations.

## Features

- **Real-Time Messaging**: Engage in real-time chat with other users using WebSockets.
- **User Authentication**: Secure user registration and login.
- **Chat Rooms**: Join and create chat rooms for group conversations.
- **Responsive Design**: Optimized for both desktop and mobile devices.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Node.js, Express
- **WebSocket Library**: `socket.io`
- **Database**: MongoDB (for user and message storage)
- **Authentication**: JWT (JSON Web Tokens)
- **Python**: Flask (for additional features, if any)

## Installation

Install the following on your local machine:

- **Node.js**
- **MongoDB**
- **Python**

# Project Setup and Execution

## Environment Setup

To get started with this project, follow these steps to set up your local environment:

1. **Install the following on your local machine:**
   - Node.js
   - MongoDB
   - Python

2. **Install Python libraries:**
   - Navigate to `Project Source Code/ML`
   - Open a command prompt and run:
     ```bash
     pip install -r req.txt
     ```

3. **Install web npm libraries:**
   - Navigate to `Project Source Code/Web`
   - Open a command prompt and run:
     ```bash
     npm install
     ```

Your environment is now ready to execute the project.

## Execution

Follow these steps to run the project locally:

1. **Start the MongoDB server:**
   - Open a command prompt from the Start menu and run:
     ```bash
     mongod
     ```
   - MongoDB server will now be live.

2. **Start the Flask server:**
   - Navigate to `Project Source Code/ML`
   - Open a command prompt and run:
     ```bash
     python app.py
     ```
   - The Flask server will now be live.

3. **Start the web server:**
   - Navigate to `Project Source Code/Web`
   - Open a command prompt and run:
     ```bash
     node app.js
     ```
   - The web server will now be live.

## Access the Project

To access the project, open your web browser and go to:

[http://localhost:5000/user/signup](http://localhost:5000/user/signup)
