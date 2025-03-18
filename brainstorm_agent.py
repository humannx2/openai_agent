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
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from agents import Agent, Runner, RunContextWrapper, function_tool

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in your .env file.")

# Define a context class to store conversation history
@dataclass
class BrainstormingContext:
    """Context class to store conversation history and brainstorming session data."""
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    topic: Optional[str] = None
    ideas_discussed: List[str] = field(default_factory=list)
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})
    
    def add_idea(self, idea: str) -> None:
        """Add an idea to the list of ideas discussed."""
        self.ideas_discussed.append(idea)
    
    def get_conversation_summary(self) -> str:
        """Get a string summary of the conversation history."""
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])

# Define tools for the agent
@function_tool
def summarize_ideas(wrapper: RunContextWrapper[BrainstormingContext]) -> str:
    """
    Summarize the ideas discussed in the brainstorming session so far.
    
    Returns:
        A concise summary of the ideas
    """
    context = wrapper.context
    if not context.ideas_discussed:
        return "We haven't recorded any specific ideas yet. Let's continue brainstorming!"
    
    return f"Here's a summary of the {len(context.ideas_discussed)} ideas we've discussed so far:\n" + \
           "\n".join([f"- {idea}" for idea in context.ideas_discussed])

@function_tool
def save_idea(wrapper: RunContextWrapper[BrainstormingContext], idea: str) -> str:
    """
    Save an important idea from the conversation.
    
    Args:
        idea: The idea to save
        
    Returns:
        Confirmation that the idea was saved
    """
    wrapper.context.add_idea(idea)
    return f"I've saved the idea: '{idea}'"

@function_tool
def suggest_brainstorming_technique(
    wrapper: RunContextWrapper[BrainstormingContext], 
    stuck_level: int
) -> str:
    """
    Suggest a brainstorming technique based on how stuck the user feels.
    
    Args:
        stuck_level: How stuck the user feels (1-5, where 5 is completely stuck)
        
    Returns:
        A suggestion for a brainstorming technique
    """
    current_topic = wrapper.context.topic or "your current topic"
    
    techniques = {
        1: "Mind Mapping: Start with your central idea and branch out with related concepts.",
        2: "SCAMPER: Consider how you can Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, or Reverse aspects of your idea.",
        3: "Six Thinking Hats: Look at the problem from different perspectives (facts, emotions, caution, benefits, creativity, process).",
        4: "Random Word Association: Pick a random word and force connections between it and your problem.",
        5: "Reverse Brainstorming: Instead of solving the problem, think about how to cause it or make it worse, then reverse your solutions."
    }
    
    return f"For your topic '{current_topic}', you might try: {techniques.get(stuck_level, techniques[3])}"

@function_tool
def set_brainstorming_topic(
    wrapper: RunContextWrapper[BrainstormingContext], 
    topic: str
) -> str:
    """
    Set or update the brainstorming topic.
    
    Args:
        topic: The topic to brainstorm about
        
    Returns:
        Confirmation that the topic was set
    """
    wrapper.context.topic = topic
    return f"I've set our brainstorming topic to: '{topic}'"

# Create a dynamic instructions function that includes context
def dynamic_instructions(agent: Agent[BrainstormingContext], wrapper: RunContextWrapper[BrainstormingContext]) -> str:
    """
    Generate dynamic instructions that include the current conversation context.
    """
    instructions = """
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
    - Use the save_idea tool when the user shares a notable idea
    - Use the set_brainstorming_topic tool when you identify the main topic
    
    Avoid:
    - Dominating the conversation with too many suggestions
    - Criticizing or judging ideas prematurely
    - Shifting topics too quickly before fully exploring an idea
    - Asking closed-ended (yes/no) questions
    """
    
    # Add topic if set
    if wrapper.context.topic:
        instructions += f"\n\nCURRENT BRAINSTORMING TOPIC: {wrapper.context.topic}"
    
    # Add ideas if any have been recorded
    if wrapper.context.ideas_discussed:
        instructions += "\n\nIDEAS DISCUSSED SO FAR:\n"
        instructions += "\n".join([f"- {idea}" for idea in wrapper.context.ideas_discussed])
    
    return instructions

# Define the brainstorming agent
brainstorm_agent = Agent[BrainstormingContext](
    name="Brainstorming Assistant",
    instructions=dynamic_instructions,
    model="gpt-4o-mini",
    tools=[
        summarize_ideas,
        save_idea,
        suggest_brainstorming_technique,
        set_brainstorming_topic
    ],
)

async def interactive_brainstorming_session():
    """
    Run an interactive brainstorming session in the terminal.
    """
    print("\n\n==== Brainstorming Assistant ====")
    print("Type 'exit' or 'quit' to end the session.")
    print("Let's start brainstorming! What topic would you like to explore today?\n")
    
    # Initialize context
    context = BrainstormingContext()
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("\nThank you for brainstorming with me! Goodbye!")
            break
        
        # Add user input to conversation history
        context.add_message("user", user_input)
        
        # Run the agent with the current context
        result = await Runner.run(
            brainstorm_agent,
            input=user_input,
            context=context
        )
        
        # Display agent's response
        print(f"\nBrainstorming Assistant: {result.final_output}")
        
        # Add agent's response to conversation history
        context.add_message("assistant", result.final_output)

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