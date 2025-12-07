# agents/conflict_detector_agent.py

import json
from typing import Any, Dict
from google.adk.agents import Agent, LlmAgent

# --- Local Session Implementation ---
class Session:
    """A simple state-management class to pass data between agents."""
    def __init__(self, initial_state: Dict[str, Any] = None):
        self.state = initial_state if initial_state is not None else {}


class ConflictDetectionAgent(Agent):
    llm_agent: LlmAgent

    def __init__(self, name: str, description: str, llm_agent: LlmAgent):
        super().__init__(
            name=name, description=description, llm_agent=llm_agent
        )

    def __call__(self, session: Session) -> Session:
        """Analyzes mapped data for medication, dosage, or diagnosis conflicts."""
        standardized_data = session.state.get('mapped_timeline', [])
        
        if not standardized_data:
            session.state['conflict_report'] = "Error: Missing data for conflict detection."
            return session
            
        print("\n[Conflict Detector Agent] Identifying potential medical conflicts...")
        
        # Prepare the input for the LLM agent
        llm_input_prompt = f"Records to analyze:\n{json.dumps(standardized_data, indent=2)}"

        # Simulate the output from the LLM run
        simulated_conflict_output = """
            **CONFLICT REPORT:**
            1. **Potential Dosage Conflict:** The same medication, Atenolol, appears as 
               25mg daily in one note, but another record (hypothetical) suggests 50mg. 
               Needs clarification.
            2. **Lab/Diagnosis Discrepancy:** High Cholesterol (210 mg/dL) is present, 
               but no Hyperlipidemia diagnosis is recorded. This should be flagged.
        """
        
        # Set output state
        session.state['conflict_report'] = simulated_conflict_output
        
        print("[Conflict Detector Agent] Conflicts identified and reported.")
        return session

def create_conflict_detector_agent() -> ConflictDetectionAgent:
    """Factory function to create the Conflict Detection Agent with its LLM component."""
    
    llm_agent = LlmAgent(
        name="ConflictLlm",
        instruction="You are a medical conflict resolution specialist. Analyze records for conflicts and list them explicitly.",
        model="gemini-2.5-flash",
    )
    
    return ConflictDetectionAgent(
        name="ConflictDetectionAgent",
        description="Identifies conflicts across medications, dosages, and diagnoses.",
        llm_agent=llm_agent
    )