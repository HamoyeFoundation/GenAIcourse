from fastapi import APIRouter
from models.conversation import ConversationRequest, ConversationResponse
# from utils.conversation_utils import ChatbotGPT
from utils import embed, prompt
from utils.convo import ChatbotGPT

conversation_router = APIRouter()

@conversation_router.post("/", response_model=ConversationResponse)
async def conversation(request: ConversationRequest):
    message = request.message
    max_tokens = request.max_tokens
    temperature = request.temperature
    top_p = request.top_p
    frequency_penalty = request.frequency_penalty
    presence_penalty = request.presence_penalty
    stop = request.stop
    threshold = request.threshold

    conversation_id = request.conversation_id
    embedding_engine = embed.get_embedding_engine()

    print("connecting to vector storage")
    vector_index = embed.connect_to_vector_index(
        embed.INDEX_NAME, embedding_engine
    )
    print("connected to vector storage")

    sources_and_scores = vector_index.similarity_search_with_score(message, k=5)
    sources, scores = zip(*sources_and_scores)

    print("running query against Q&A chain")

    c = ChatbotGPT("gpt-3.5-turbo-1106", prompt=prompt.main, temperature=temperature, max_tokens=max_tokens)
    response = c.question_answer(sources, message)
    print(response)

    return ConversationResponse(text=response)
