# Medical Harmonizer Agent Workflow

This project demonstrates a multi-agent system designed to ingest, harmonize, and analyze unstructured medical data from various sources. It uses a sequential workflow of specialized agents to transform raw data (like PDFs and images of lab reports or doctor's notes) into a single, actionable summary for a patient.

The core of the system is built using a conceptual framework similar to the Google Agent Development Kit (ADK), where a `SequentialAgent` orchestrates a series of sub-agents, each performing a specific task.

## 🎯 Core Problem

Patient medical data is often fragmented across different formats and systems:
- Unstructured text in PDFs (lab results).
- Images of handwritten notes.
- Disparate EMR (Electronic Medical Record) entries.

This fragmentation makes it difficult to get a holistic view of a patient's health, identify trends, or spot potentially dangerous conflicts (e.g., medication contraindications). This project simulates a solution to this problem by harmonizing this data.

## 🤖 The Agent-Based Workflow

The system is orchestrated by `main.py`, which sets up a `SequentialAgent`. This orchestrator ensures that the output of one agent becomes the input for the next, creating a data processing pipeline.

The workflow consists of four specialized agents:

### 1. Standardization Agent
*   **File:** `agents/standardization_agent.py`
*   **Purpose:** To ingest raw files and convert them into a structured, standardized JSON format.
*   **Process:**
    1.  **Ingestion:** Takes a list of file paths as input.
    2.  **OCR (Simulated):** A placeholder function (`run_ocr_on_file`) simulates extracting raw text from each file.
    3.  **Structuring (Simulated LLM Call):** A placeholder function (`_simulate_llm_structuring`) mimics an LLM call that takes the raw text and converts it into a predefined JSON schema, extracting entities like diagnoses, medications, and lab results.
*   **Output:** A list of structured JSON objects, which is stored in the `session.state['standardized_records']`.

### 2. Relation Mapper Agent
*   **File:** `agents/relation_mapper_agent.py`
*   **Purpose:** To analyze the standardized records and establish connections and a timeline.
*   **Process:**
    1.  **Input:** Reads the `standardized_records` from the session.
    2.  **Mapping (Simulated LLM Call):** It simulates sending all the structured data to an LLM to generate a narrative summary that connects the dots (e.g., "This medication was prescribed to treat that diagnosis, which is supported by this lab result.").
*   **Output:** A human-readable timeline summary, stored in `session.state['relational_summary']`.

### 3. Conflict Detector Agent
*   **File:** `agents/conflict_detector_agent.py`
*   **Purpose:** To identify medical inconsistencies or potential risks across the combined dataset.
*   **Process:**
    1.  **Input:** Reads the mapped data from the session.
    2.  **Analysis (Simulated LLM Call):** It simulates an LLM call designed to find conflicts, such as:
        - Dosage discrepancies for the same medication.
        - Abnormal lab results without a corresponding diagnosis.
        - Contradictory diagnoses.
*   **Output:** A formatted conflict report, stored in `session.state['conflict_report']`.

### 4. Harmonized Summary Agent
*   **File:** `agents/summary_agent.py`
*   **Purpose:** To create the final, user-facing report that is easy to understand and act upon.
*   **Process:**
    1.  **Input:** Reads the `relational_summary` and `conflict_report` from the session.
    2.  **Aggregation (Simulated LLM Call):** It simulates a final LLM call to synthesize all the information into a clean, well-structured report that includes:
        - A summary of non-conflicting information.
        - A clear presentation of the identified conflicts.
        - A list of actionable questions for the patient to ask their doctor.
*   **Output:** The final report string, stored in `session.state['final_report']`.

## ⚙️ Project Structure

```
/medical_harmonizer
├── agents/
│   ├── __init__.py
│   ├── standardization_agent.py
│   ├── relation_mapper_agent.py
│   ├── conflict_detector_agent.py
│   └── summary_agent.py
├── main.py
└── README.md
```

- **`main.py`**: The entry point of the application. It defines the agents, constructs the `SequentialAgent` orchestrator, initializes the session, and runs the workflow.
- **`agents/`**: A directory containing each specialized agent in its own module. This promotes modularity and separation of concerns.

## 🚀 How to Run

1.  **Prerequisites**: Ensure you have Python installed. This demo uses a conceptual `google.adk` library, but the logic is self-contained and does not require external installation as-is.

2.  **Configure Input**: Open `main.py` and modify the `user_uploaded_files` list to point to your desired (simulated) file paths.

    ```python
    # main.py
    user_uploaded_files = [
        "C:/data/lab_results_may_10.pdf",
        "C:/data/doctors_note_may_10.jpg",
    ]
    ```

3.  **Execute the Workflow**: Run the main script from your terminal.

    ```bash
    python main.py
    ```

4.  **View Output**: The script will print the status of each agent as it runs and will display the final, harmonized report in the console.
