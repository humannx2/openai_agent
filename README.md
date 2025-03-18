# Brainstorming Assistant

An AI-powered brainstorming assistant that helps users develop ideas by asking relevant questions and maintaining context throughout the conversation.

## Features

- Asks thought-provoking, open-ended questions to explore different angles of a topic
- Maintains conversation context throughout the brainstorming session
- Suggests connections between ideas
- Summarizes and organizes thoughts when needed
- Suggests brainstorming techniques when the user seems stuck
- Interactive command-line interface for easy conversation

## Requirements

- Python 3.8+
- OpenAI API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/brainstorming-assistant.git
   cd brainstorming-assistant
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the brainstorming assistant:

```
python brainstorm_agent.py
```

Follow the prompts to start your brainstorming session. Type 'exit' or 'quit' to end the session.

## How It Works

The brainstorming assistant is built using the OpenAI Agents Python framework. It uses:

1. A main agent with carefully crafted instructions for effective brainstorming
2. Custom tools for summarizing ideas and suggesting brainstorming techniques
3. Conversation history tracking to maintain context
4. GPT-4o-mini as the underlying language model

The assistant follows these guidelines:
- Asks one question at a time to avoid overwhelming the user
- Focuses on "why," "how," and "what if" questions to encourage deeper thinking
- Validates ideas before suggesting alternatives or expansions
- Remembers all context from the current session
- Avoids criticizing or judging ideas prematurely

## Example Conversation

```
==== Brainstorming Assistant ====
Type 'exit' or 'quit' to end the session.
Let's start brainstorming! What topic would you like to explore today?

You: I'm trying to come up with a new app idea for students

Brainstorming Assistant: That's a great area to explore! Students have many needs and pain points that could be addressed with a well-designed app. To get started, could you tell me what specific problem or challenge for students you're most interested in solving?

You: I'm thinking about helping them manage their time better

Brainstorming Assistant: Time management is definitely a common challenge for students! Let's explore this further. What do you think are the biggest time management hurdles that students face in their daily lives?
```

## Customization

You can customize the brainstorming agent by modifying:

1. The agent instructions in `brainstorm_agent.py`
2. The available tools and their functionality
3. The model configuration (e.g., switching to a different OpenAI model)

## License

MIT 