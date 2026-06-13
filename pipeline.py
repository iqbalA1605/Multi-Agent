from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
from rich import print

def run_research_pipeline(topic : str) -> dict:
    
    state = {}
    # search agent working
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, relaible and detailed information about: {topic}")]
    })
    
    # Safely extract content from the last message
    last_msg = search_result['messages'][-1]
    state["search_results"] = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
    print("\n search result", state['search_results'])

    print("\n"+" ="*50)
    print("step 2 - Reader agent is scrapping top resources ...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    
    last_reader_msg = reader_result['messages'][-1]
    state['scraped_content'] = last_reader_msg.content if hasattr(last_reader_msg, 'content') else str(last_reader_msg)
    print("\nscraped_content: \n", state['scraped_content'])

    print("\n"+" ="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS: \n {state['search_results']}\n\n"
        f"SCRAPED CONTENT: \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })
    print("\n Final Report\n", state['report'])

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ...")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report" : state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic: ")
    run_research_pipeline(topic)
