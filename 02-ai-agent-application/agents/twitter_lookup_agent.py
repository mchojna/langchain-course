import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub


load_dotenv()

def lookup(name: str, func) -> str:
    llm = ChatOpenAI(
        api_key=os.getenv("CHAT_OPENAI_API_KEY"),
        model="gpt-4o-mini",
    )
    template = """
        Give the name {name} I want you to find their Twitter profile page URL and extract from it only the username.
        Your answer should contain only a person's username.
    """
    prompt_template = PromptTemplate(
        input_variables=[name],
        template=template,
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Twitter Profile Username",
            func=func,
            description="Useful for when you need to get the Twitter profile username",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
    )
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name=name)}
    )

    twitter_username = result["output"]
    return twitter_username
