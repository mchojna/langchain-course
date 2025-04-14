import os
from typing import Tuple

from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from output_prasers import Summary

from third_parties.linkedin_scraper import scrape_linkedin_profile
from third_parties.twitter_scraper import scrape_user_tweets
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from tools.tools import get_profile_url_tavily

from output_prasers import summary_parser

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def summarise_profile(name: str) -> Tuple[Summary, str]:
    template = """
            Given the information about a person from linkedin {linkedin_information} 
            and latest twitter posts {twitter_information} I want to create:
            1. a short summary of the person,
            2. two interesting facts about the person.
            
            Use both information from Twitter and LinkedIn to create a concise and informative summary.
            \n{format_instructions}
        """

    linkedin_profile_url = linkedin_lookup_agent(name, get_profile_url_tavily)
    linkedin_information = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url,
    )

    twitter_username = twitter_lookup_agent(name, scrape_user_tweets)
    twitter_information = scrape_user_tweets(mock=True)

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
    )

    # chain = prompt_template | llm | StrOutputParser()

    chain = summary_prompt_template | llm | summary_parser

    result: Summary = chain.invoke(
        input={
            "linkedin_information": linkedin_information,
            "twitter_information": twitter_information
        }
    )

    return result, linkedin_information.get("avatar")


if __name__ == "__main__":
    summary = summarise_profile("Andrew Ng")
    print(summary)
