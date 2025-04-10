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
        model="o3-mini",
    )
    template = """
        Given the full name {name} I want you to get it me a link of their Linkedin profile page URL.
        Your answer should contain only a URL.
    """
    prompt_template = PromptTemplate(
        template=template,
        input_variables=[name],
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Linkedin Profile URL",
            func=func,
            description="Useful for when you need to get the Linkedin profile page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url
