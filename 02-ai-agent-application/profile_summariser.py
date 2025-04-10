import os
import pprint

from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from linkedin_scraper import screpe_linkedin_profile

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def summarise_profile(template: str, information: dict) -> None:
    prompt_template = PromptTemplate(
        input_variables=["information"],
        template=template,
    )

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="o3-mini")

    chain = prompt_template | llm | StrOutputParser()

    result = chain.invoke(input={"information": information})

    print(result)


if __name__ == "__main__":
    template = """
        Given the information {information} about a person from I want to create:
        1. a short summary of the person,
        2. two interesting facts about the person.
    """
    information = screpe_linkedin_profile(mock=True)

    summarise_profile(template, information)
