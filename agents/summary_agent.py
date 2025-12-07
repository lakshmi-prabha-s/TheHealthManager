# agents/summary_agent.py

from typing import Any, Dict
from google.adk.agents import Agent, LlmAgent

# --- Local Session Implementation ---
class Session:
    """A simple state-management class to pass data between agents."""
    def __init__(self, initial_state: Dict[str, Any] = None):
        self.state = initial_state if initial_state is not None else {}


class HarmonizedSummaryAgent(Agent):
    llm_agent: LlmAgent

    def __init__(self, name: str, description: str, llm_agent: LlmAgent):
        super().__init__(
            name=name, description=description, llm_agent=llm_agent
        )

    def __call__(self, session: Session) -> Session:
        """Aggregates all results and creates the final, user-facing report."""
        timeline_summary = session.state.get('relational_summary', 'N/A')
        conflict_report = session.state.get('conflict_report', 'N/A')
        
        print("\n[Harmonized Summary Agent] Compiling final patient report...")
        
        # Prepare the comprehensive input for the LLM agent
        llm_input_prompt = (
            f"Relational Summary:\n{timeline_summary}\n\n"
            f"Conflict Report:\n{conflict_report}"
        )

        # Simulate FINAL OUTPUT
        final_report = f"""
            # 🌟 Harmonized Medical Summary Report 🌟
            
            ---
            ## 1. Combined Non-Conflicting Elements
            * **Diagnosis:** Hypertension (Consistent across all records).
            * **Medication:** Atenolol 25mg, taken Daily (Pending dosage conflict resolution).
            
            ---
            ## 2. Key Lab Results Comparison
            | Test | Value | Date | Doctor |
            | :--- | :--- | :--- | :--- |
            | Cholesterol | 210 mg/dL (High) | 2024-05-10 | Dr. Smith |
            | Glucose | 115 mg/dL | 2024-05-10 | Dr. Smith |

            ---
            ## 3. ⚠️ Critical Conflict Notes
            {conflict_report}
            **ACTION REQUIRED:** Please review these conflicts with your physician immediately.
            
            ---
            ## 4. Questions for Your Doctors
            1.  Can you confirm the correct dosage for my Atenolol (25mg or 50mg)?
            2.  My Cholesterol is high (210 mg/dL). Should I be diagnosed or treated for Hyperlipidemia?
        """
        
        # Final Output State
        session.state['final_report'] = final_report
        
        print("[Harmonized Summary Agent] Final report generated.")
        return session

def create_summary_agent() -> HarmonizedSummaryAgent:
    """Factory function to create the Harmonized Summary Agent with its LLM component."""
    
    llm_agent = LlmAgent(
        name="SummaryLlm",
        instruction="You are a patient advocate. Combine the timeline and conflict report into a safe, actionable summary.",
        model="gemini-2.5-flash",
    )
    
    return HarmonizedSummaryAgent(
        name="HarmonizedSummaryAgent",
        description="Creates the final, actionable report for the user.",
        llm_agent=llm_agent
    )
