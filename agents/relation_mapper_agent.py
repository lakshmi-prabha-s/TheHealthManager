# agents/relation_mapper_agent.py

import json
from typing import Any, Dict
from google.adk.agents import Agent, LlmAgent

# --- Local Session Implementation ---
class Session:
    """A simple state-management class to pass data between agents."""
    def __init__(self, initial_state: Dict[str, Any] = None):
        self.state = initial_state if initial_state is not None else {}


class RelationMapperAgent(Agent):
    llm_agent: LlmAgent

    def __init__(self, name: str, description: str, llm_agent: LlmAgent):
        super().__init__(
            name=name, description=description, llm_agent=llm_agent
        )
    def __call__(self, session: Session) -> Session:
        """Retrieves standardized data and generates a relational summary."""
        standardized_data = session.state.get('standardized_records', [])
        
        if not standardized_data:
            session.state['mapped_timeline'] = "Error: No standardized data found."
            return session
            
        print("\n[Relation Mapper Agent] Generating timeline and relational summary...")
        
        # Prepare the input for the LLM agent
        llm_input_prompt = f"Standardized Records:\n{json.dumps(standardized_data, indent=2)}"

        # Simulate the output from the LLM run
        simulated_output = """
            **Timeline Summary:**
            On 2024-05-10, Dr. Smith recorded a diagnosis of Hypertension. This diagnosis 
            is linked to a high Cholesterol (210 mg/dL) lab result from the same day. 
            The same doctor prescribed Atenolol (25mg, Daily) to treat the Hypertension.
        """
        
        # Set output state
        session.state['mapped_timeline'] = standardized_data 
        session.state['relational_summary'] = simulated_output
        
        print("[Relation Mapper Agent] Timeline mapped and summary generated.")
        return session

def create_relation_mapper_agent() -> RelationMapperAgent:
    """Factory function to create the Relation Mapper Agent with its LLM component."""
    
    llm_agent = LlmAgent(
        name="MapperLlm",
        instruction="You are a medical data integrator. Map relationships between records to create a patient timeline.",
        model="gemini-2.5-flash",
    )
    
    return RelationMapperAgent(
        name="MedicalRelationMapperAgent",
        description="Connects standardized records into a coherent timeline/graph.",
        llm_agent=llm_agent
    )