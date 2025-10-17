# Agentic-Fitness-Coach
An intelligent, conversational AI fitness assistant designed to provide personalized workout, nutrition, and motivation plans. Built with Streamlit and powered by the high-speed Groq API.


---

## ✨ Features

- **Conversational AI Coach:** Get instant, human-like responses for your fitness queries.
- **Multi-Intent Understanding:** The AI can differentiate between requests for **workouts**, **nutrition**, and **motivation**, providing contextually appropriate answers.
- **Personalized Profile:** Input your name, age, sex, and primary fitness goal (e.g., Weight Loss) to get more tailored advice.
- **Safety First:** Includes a built-in safety guardrail to detect questions related to medical issues or pain and provides a responsible disclaimer instead of unsafe advice.
- **Sleek & Responsive UI:** A clean and modern user interface built with Streamlit, perfect for both desktop and mobile.

---

## 🛠️ Tech Stack

- **Framework:** [Streamlit](https://streamlit.io/)
- **Language:** [Python](https://www.python.org/)
- **LLM API:** [Groq](https://groq.com/)
- **Model:** Llama 3
- **Libraries:** Pandas

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python 3.9 or higher
- A Groq API Key

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/Agentic-Fitness-Coach.git](https://github.com/YourUsername/Agentic-Fitness-Coach.git)
    cd Agentic-Fitness-Coach
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**
    - Create a new folder in the root of the project called `.streamlit`.
    - Inside the `.streamlit` folder, create a new file named `secrets.toml`.
    - Add your Groq API key to the `secrets.toml` file like this:
      ```toml
      GROQ_API_KEY = "gsk_YourActualApiKeyGoesHere"
      ```

5.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

The application should now be running in your web browser!

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
