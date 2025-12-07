# main.py
from typing import Any, Dict
from google.adk.agents import SequentialAgent

# --- Local Session Implementation ---
class Session:
    """A simple state-management class to pass data between agents."""
    def __init__(self, initial_state: Dict[str, Any] = None, session_id: str = None):
        self.state = initial_state if initial_state is not None else {}
        self.session_id = session_id
# Import the agent creation functions
from agents.standardization_agent import create_standardization_agent
from agents.relation_mapper_agent import create_relation_mapper_agent
from agents.conflict_detector_agent import create_conflict_detector_agent
from agents.summary_agent import create_summary_agent


def run_medical_harmonizer_workflow(file_paths: list):
    """
    Sets up the sequential multi-agent workflow using ADK's SequentialAgent 
    and runs the session.
    """
    print("--- 🩺 Starting Multi-Agent Medical Harmonizer ---")
    
    # 1. Define the Agents
    standardization_agent = create_standardization_agent()
    mapper_agent = create_relation_mapper_agent()
    detector_agent = create_conflict_detector_agent()
    summary_agent = create_summary_agent()
    
    # 2. Define the Workflow Orchestrator (SequentialAgent)
    # The SequentialAgent ensures the data flow is correct: Output of 1 -> Input of 2
    workflow_orchestrator = SequentialAgent(
        name="MedicalHarmonizerWorkflow",
        sub_agents=[
            standardization_agent,
            mapper_agent,
            detector_agent,
            summary_agent
        ]
    )
    
    # 3. Initialize Session with Input Data
    session = Session(session_id="user_medical_analysis_123", initial_state={})
    session.state['input_file_paths'] = file_paths
    session.state['user_profile'] = {"name": "Jane Doe", "age": 55}
    
    print(f"Input: {len(file_paths)} files loaded for analysis.")
    print("-" * 40)
    
    # 4. Execute the Workflow (Run the main SequentialAgent)
    # The orchestration is performed by iterating through the sub_agents
    # defined in the SequentialAgent and calling each one in order.
    current_session = session
    for agent in workflow_orchestrator.sub_agents:
        current_session = agent(current_session)
    final_session = current_session
    
    print("-" * 40)
    print("--- ✅ Workflow Completed ---")
    
    # 5. Final Output to User (Minimal UI)
    print("\n\n" + "="*50)
    print("      FINAL HARMONIZED REPORT (Minimal UI)      ")
    print("="*50)
    
    final_report = final_session.state.get('final_report', 'An error occurred during report generation.')
    print(final_report)


if __name__ == "__main__":
    # Simulate user input files
    user_uploaded_files = [
        "C:/data/lab_results_may_10.pdf",
        "C:/data/doctors_note_may_10.jpg",
    ]
    
    # Run the entire system
    run_medical_harmonizer_workflow(user_uploaded_files)