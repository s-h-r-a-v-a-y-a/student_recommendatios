
# Student Performance Analysis Dashboard 📊

This project analyzes students' quiz performance and generates personalized insights and recommendations. It includes tools to assess performance trends, identify strengths and weaknesses, and suggest improvement strategies using a clean, interactive Streamlit dashboard.

---

## 🚀 Features

- **Persona Generation**: Creates a student persona based on learning style, consistency, strengths, and areas for improvement.
- **Recommendations**: Provides actionable improvement plans and study strategies.
- **Performance Trends**: Tracks performance over time and identifies weak areas.
- **Interactive Dashboard**: Upload files to get instant analysis in a user-friendly interface.
- **Downloadable Reports**: Export analysis results as JSON.

---

## 📂 Project Structure

- **`app.py`**: The Streamlit app providing the user interface for data analysis.
- **`student_recommendations.py`**: Core logic for analyzing student performance and generating recommendations.

---

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip for installing dependencies

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/student-performance-analysis.git

2. Navigate to the project directory:
   ```bash
   cd student-performance-analysis

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Run the Streamlit app:
   ```bash
   streamlit run app.py

5. Open your browser at http://localhost:8501 to access the dashboard.

---

## 📝 How to Use
1. Prepare the following JSON files:
   -**Historical Data**: Contains details of past quiz performances.
   -**Current Quiz Data**: Information about the most recent quiz.
   -**Quiz Submission Data**: Student answers for the current quiz.
   Sample Format:
   ```bash
   {
    "quiz": {"topic": "Mathematics", "difficulty": "Medium"},
    "score": 75,
    "accuracy": "80 %",
    "correct_answers": 8,
    "total_questions": 10
   }
2. Upload the files through the app's sidebar.

3. Click "Analyze Data" to view the results.

4. Download the analysis report for further review.

---

## 💡 Approach Description

### Core Functionalities
- **Data Loading**: JSON files are uploaded via the app and processed using Pandas.
- **Performance Analysis**:
        Tracks trends across quizzes (accuracy, scores).
        Identifies weak areas based on accuracy thresholds.
- **Persona Generation**:
        Determines learning style based on speed and accuracy.
        Classifies performance level into "High Achiever," "Average Performer," or "Needs Improvement."
- **Recommendations**:
        Creates personalized practice plans.
        Suggests strategies tailored to learning style and performance trends.

### Implementation Flow
- **Data Pipeline**:
        Load JSON files.
        Preprocess and analyze historical and current quiz data.
- **Analysis Module**:
        Calculate trends and weak areas.
        Generate persona based on consistency, strengths, and style.
- **Dashboard**:
        Visualizes analysis results.
        Provides download options for reports.

