

# AI Technical Interview Question Generator

This is an AI-powered Streamlit application that generates customized technical interview questions based on a given topic. It supports multiple question formats including essay questions, short answers, multiple choice questions (MCQs), and coding challenges. The tool is designed for students, educators, and job seekers preparing for technical interviews or assessments.

## Features

- **Topic-Based Generation**: Generate relevant technical questions by entering a specific topic (e.g., "Operating Systems", "Data Structures", "Machine Learning").
- **Question Types**: Supports essay, short answer, MCQs, and coding problems with sample input/output and solutions.
- **Balanced Mode**: Automatically creates a mix of question types if none are specified.
- **PDF Export**: Export the generated questions and answers as a well-formatted PDF.
- **Educational Level Classification**: Each question includes a Bloom's Taxonomy level (e.g., Remember, Understand, Apply, Analyze).
- **Multilingual Support**: Automatically adjusts the output language based on user preferences (e.g., Python, Java, C++) for coding problems.

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/Habiba480/interview-question-generator.git
   cd interview-question-generator

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_key_here
   ```

4. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

## File Structure

```
.
├── app.py                 # Main Streamlit application
├── requirements.txt       # Required Python packages                 # API keys and environment variables
└── README.md              # Project overview
```

## Technologies Used

* **Python 3.11+**
* **Streamlit** – UI framework
* **LangChain** – Prompt engineering and message history
* **OpenAI GPT** – Question generation engine
* **FPDF** – PDF generation
* **dotenv** – Environment variable management

## Example Output

### Short Answer Questions

**1. What is a thread in operating systems?**
**Answer:** A thread is the smallest unit of processing that can be scheduled by an operating system.

**Level:** Understand

### Coding Problem

**1. Write a function in Python to reverse a string.**

**Example Input:** "hello"
**Example Output:** "olleh"

**Solution:**

```python
def reverse_string(s):
    return s[::-1]
```

**Level:** Apply

## License

This project is licensed under the MIT License.

