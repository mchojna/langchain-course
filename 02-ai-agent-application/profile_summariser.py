import os

from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from third_parties.linkedin_scraper import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from tools.tools import get_profile_url_tavily

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def summarise_profile(name: str):
    template = """
            Given the information {information} about a person from I want to create:
            1. a short summary of the person,
            2. two interesting facts about the person.
        """

    linkedin_profile_url = linkedin_lookup_agent(name, get_profile_url_tavily)

    information = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url,
    )

    prompt_template = PromptTemplate(
        input_variables=["information"],
        template=template,
    )

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="o3-mini",
    )

    chain = prompt_template | llm | StrOutputParser()

    result = chain.invoke(input={"information": information})

    return result


if __name__ == "__main__":
    summary = summarise_profile("Andrew Ng")
    print(summary)
