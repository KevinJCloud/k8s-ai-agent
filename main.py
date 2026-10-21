
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools import TOOLS
import os


# 1. Configure the local LLM
llm = ChatOllama(
    model="llama3.2",
    base_url= os.getenv("OLLAMA_BASE_URL","http://localhost:11434"),
    temperature=0,
)


# 2. Define the agent's instructions
SYSTEM_PROMPT = """
You are a Kubernetes troubleshooting assistant.

Your job is to investigate Kubernetes problems using the available tools.

Instructions:
1. Understand the user's question.
2. Use the appropriate tools to collect actual cluster information.
3. For general cluster health, inspect nodes and pods.
4. For pod failures, inspect pod status and Kubernetes events.
5. Use pod logs when you have enough information to identify
   the affected pod and namespace.
6. Base your conclusions on the tool results.
7. If information is unavailable, explain what is missing.
8. Explain the likely cause and recommend safe troubleshooting steps.
9. Never claim you fixed an issue when you only diagnosed it.
10. Do not invent logs, events, pod names, or cluster conditions.
11. The tools are read-only. Never claim to modify the cluster.
"""


# 3. Create the AI agent and attach the tools
agent = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
)


# 4. Chat with the agent
def main():
    print("Kubernetes AI Troubleshooting Agent")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ("exit", "quit"):
            print("Agent stopped.")
            break

        if not question:
            continue

        try:
            response = agent.invoke({
                "messages": [
                    {"role": "user", "content": question}
                ]
            })

            # Display the final assistant response
            for message in reversed(response["messages"]):
                if (
                    getattr(message, "type", "") == "ai"
                    and message.content
                ):
                    print("\nAI:", message.content, "\n")
                    break

        except Exception as exc:
            print(f"\nAgent error: {exc}\n")


if __name__ == "__main__":
    main()
