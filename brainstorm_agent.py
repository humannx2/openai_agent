"""
Brainstorming Assistant Agent

This script creates an AI agent that helps with brainstorming by asking relevant questions
and maintaining context throughout the conversation. It uses the OpenAI Agents Python framework.

Usage:
    python brainstorm_agent.py
"""

from dotenv import load_dotenv
import os
import asyncio
from agents import Agent, Runner
from agents import function_tool
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in your .env file.")

# Define tools for the agent
@function_tool
def summarize_ideas(ideas: List[str]) -> str:
    """
    Summarize a list of ideas discussed in the brainstorming session.
    
    Args:
        ideas: A list of ideas to summarize
        
    Returns:
        A concise summary of the ideas
    """
    return f"Here's a summary of the {len(ideas)} ideas we've discussed so far."

@function_tool
def suggest_brainstorming_technique(current_topic: str, stuck_level: int) -> str:
    """
    Suggest a brainstorming technique based on the current topic and how stuck the user feels.
    
    Args:
        current_topic: The topic being brainstormed
        stuck_level: How stuck the user feels (1-5, where 5 is completely stuck)
        
    Returns:
        A suggestion for a brainstorming technique
    """
    techniques = {
        1: "Mind Mapping: Start with your central idea and branch out with related concepts.",
        2: "SCAMPER: Consider how you can Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, or Reverse aspects of your idea.",
        3: "Six Thinking Hats: Look at the problem from different perspectives (facts, emotions, caution, benefits, creativity, process).",
        4: "Random Word Association: Pick a random word and force connections between it and your problem.",
        5: "Reverse Brainstorming: Instead of solving the problem, think about how to cause it or make it worse, then reverse your solutions."
    }
    
    return f"For your topic '{current_topic}', you might try: {techniques.get(stuck_level, techniques[3])}"

# Define the brainstorming agent
brainstorm_agent = Agent(
    name="Brainstorming Assistant",
    instructions="""
    You are a helpful brainstorming assistant that asks thought-provoking questions to help users develop their ideas.
    
    Your primary goals are to:
    1. Understand the user's brainstorming topic or problem
    2. Ask relevant, open-ended questions that help the user explore different angles
    3. Maintain context throughout the conversation
    4. Suggest connections between ideas when appropriate
    5. Summarize and organize thoughts when helpful
    6. Suggest specific brainstorming techniques when the user seems stuck
    
    Follow these guidelines:
    - Start by understanding the user's topic or problem thoroughly
    - Ask one question at a time to avoid overwhelming the user
    - Focus on "why," "how," and "what if" questions to encourage deeper thinking
    - Validate ideas before suggesting alternatives or expansions
    - Remember all context from the current session
    - When appropriate, summarize the ideas discussed so far
    - If the user seems stuck, suggest a specific brainstorming technique
    
    Avoid:
    - Dominating the conversation with too many suggestions
    - Criticizing or judging ideas prematurely
    - Shifting topics too quickly before fully exploring an idea
    - Asking closed-ended (yes/no) questions
    """,
    model="gpt-4o-mini",
    tools=[summarize_ideas, suggest_brainstorming_technique],
)

async def interactive_brainstorming_session():
    """
    Run an interactive brainstorming session in the terminal.
    """
    print("\n\n==== Brainstorming Assistant ====")
    print("Type 'exit' or 'quit' to end the session.")
    print("Let's start brainstorming! What topic would you like to explore today?\n")
    
    conversation_history = []
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("\nThank you for brainstorming with me! Goodbye!")
            break
        
        # Add user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})
        
        # Run the agent with the current user input
        result = await Runner.run(
            brainstorm_agent, 
            input=user_input,
            context={"conversation_history": conversation_history}
        )
        
        # Display agent's response
        print(f"\nBrainstorming Assistant: {result.final_output}")
        
        # Add agent's response to conversation history
        conversation_history.append({"role": "assistant", "content": result.final_output})

def main():
    """
    Main function to run the brainstorming agent.
    """
    try:
        asyncio.run(interactive_brainstorming_session())
    except KeyboardInterrupt:
        print("\n\nSession terminated by user. Goodbye!")
    except Exception as e:
        print(f"\n\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main() 