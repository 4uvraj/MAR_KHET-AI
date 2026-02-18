from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv

load_dotenv()


def get_ai_explanation(
    predicted_price,
    commodity,
    state,
    month,
    year
):

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an agriculture market expert."),
        ("human", """
Predicted Price: ₹{price}
Commodity: {commodity}
State: {state}
Month: {month}
Year: {year}

Explain why price may be like this in simple farmer-friendly language.
""")
    ])

    llm = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        task="text-generation"
    )

    model = ChatHuggingFace(llm=llm)

    final_prompt = prompt.invoke({
        "price": predicted_price,
        "commodity": commodity,
        "state": state,
        "month": month,
        "year": year
    })

    response = model.invoke(final_prompt)

    return response.content
