# Codsoft Artificial Intelligence Internship

Welcome to my portfolio repository for the Codsoft Artificial Intelligence Internship! This repository showcases the projects I built, demonstrating my skills in Python, fundamental AI concepts, and interactive application development with Streamlit.

Each task assigned during the internship is organized into its own dedicated folder. Below is a summary of each project.

---

## Projects Overview

### 📝 [Task 1: Rule-Based Chatbot](./Task1-Chatbot%20with%20rule%20based%20responses/)

A sophisticated chatbot named "Intellibot," built from scratch using Python. This project demonstrates a classic AI approach, using **regular expressions** and **state management** to create dynamic, context-aware conversations without relying on a large language model.

**Key Features:**
- **Stateful Conversations:** Remembers context like the user's name and to-do list items within a single session.
- **Interactive To-Do List:** Allows users to add, remove, view, and clear items.
- **Fun & Games:** Can play a "Guess the Number" game, tell jokes, and flip a coin.
- **Practical Utilities:** Includes a secure password generator and a basic calculator.

**Technology Stack:** Python, Streamlit, Regular Expressions (`re`).

### 🤖 [Task 2: Unbeatable Tic-Tac-Toe AI](./Task2-Tic-Tac-Toe-Ai/)

An interactive, web-based Tic-Tac-Toe game where a human can play against an unbeatable AI opponent. The AI's logic is powered by the **Minimax algorithm**, a foundational concept in game theory and artificial intelligence.

**Key Features:**
- **Unbeatable AI:** Implements the Minimax algorithm to recursively find the optimal move, making it impossible for the human player to win.
- **Interactive Game Board:** A clean and intuitive UI built with Streamlit buttons.
- **Stateful Gameplay:** Tracks the board state, player turns, and game outcomes.
- **Educational Component:** Includes an in-app explainer on how the Minimax algorithm works to make decisions.

**Technology Stack:** Python, Streamlit.

### 🍽️ [Task 3: Restaurant Recommendation System](./Task3-Recommendation_System-Restaurent%20Recommendation/)

A rule-based AI recommendation system that helps users find restaurants based on their specific preferences. This project uses the Pandas library to efficiently filter and rank a large dataset according to a clear set of user-defined rules.

**Key Features:**
- **Rule-Based Filtering:** The core AI filters thousands of restaurants based on user-selected rules for cuisine, location, and price.
- **Intelligent Ranking:** Ranks the filtered results using a `quality_score` (`rating` * `votes`) to surface the most popular and highly-regarded options first.
- **Dynamic User Interface:** Allows users to choose any combination of filters to apply.
- **Efficient Data Handling:** Uses Streamlit's caching to load and process the large dataset only once, ensuring a fast and responsive user experience.

**Technology Stack:** Python, Streamlit, Pandas.

---

## 🔧 How to Run a Project

To run any of the projects on your local machine, please follow these general steps:

1.  **Clone this Repository**
    ```bash
    git clone https://github.com/jai07032005-byte/Codsoft-Internship.git
    ```

2.  **Navigate to a Project Directory**
    ```bash
    # Example for Task 3
    cd Codsoft-Internship/Task3-Recommendation_System-Restaurent\ Recommendation/
    ```

3.  **Install Required Libraries**
    Each project folder contains its own `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
    *(It's highly recommended to use a Python virtual environment.)*

4.  **Run the Streamlit Application**
    Execute the following command. The Python script name may vary per project.
    ```bash
    streamlit run Restaurent.py
    ```
