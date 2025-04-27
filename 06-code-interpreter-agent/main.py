from typing import Any

from dotenv import load_dotenv
from langchain import hub
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.agents import create_csv_agent

load_dotenv()

def main():
    print("Start...")

    instructions = """
    You are an agent designed to write and execute python code to answer questions.
    You have access to a python REPL, which you can use to execute python code.
    If you get an error, debug your code and try again.
    Only use the output of your code to answer the question.
    You might know the answer without running any code, but you should still run the code to get the answer.
    If it does not seem like you can write code to answer the question, just return "I don't know." as the answer.
    """
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    tools = [PythonREPLTool()]
    python_agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
        tools=tools,
    )

    python_agent_executor: AgentExecutor = AgentExecutor(
        agent=python_agent,
        tools=tools,
        verbose=True,
    )

    csv_agent_executor: AgentExecutor = create_csv_agent(
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
        path="episode_info.csv",
        verbose=True,
        allow_dangerous_code=True,
    )

    def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        return python_agent_executor.invoke({"input": original_prompt})

    def python_csv_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        return csv_agent_executor.invoke({"input": "Using tool python_repl_ast answer this question: " + original_prompt})

    tools = [
        Tool(
            name="Python Agent",
            func=python_agent_executor_wrapper,
            description="""
            Useful when you need to transform natural language to python code and execute python code.
            Returning the results of the code execution.
            Not accept code as input.
            """,
        ),
        Tool(
            name="CSV Agent",
            func=python_csv_executor_wrapper,
            description="""
            Useful when you need to answer question over episode_info.csv file.
            Takes as input the entire question and returns the answer after running pandas calculations.
            Needs to use python_repl_ast 
            """
        )
    ]

    prompt = base_prompt.partial(instructions="")
    grand_agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
        tools=tools,
    )

    grand_agent_executor: AgentExecutor = AgentExecutor(
        agent=grand_agent,
        tools=tools,
        verbose=True,
    )

    print(
        grand_agent_executor.invoke(
            input = {"input": "Which season has the most episodes?"}
        )
    )

if __name__ == "__main__":
    main()
