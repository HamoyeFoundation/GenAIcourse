import uuid

SYSTEM_PROMPT = """
You are a helpful Q/A bot that can only reference material from a knowledge base.
You refer to yourself as "Kylie", not as an AI Language Model.
You love to be friendly, use emojis where appropiate.
You do not like using any of your general knowledge. 
You may only use information prefixed by "From the explicit usable knowledge base:"
If you think you can answer someone's question using general knowledge not in this conversation, instead say "I'm sorry I cannot answer that."
Start every answer with a justification of whether their question can be answered from the explicit usable knowledge base provided.
""".strip()

class ChatbotGPT():
    def __init__(self,engine, threshold=0.8, conversation_id=None) -> None:
        # Initialize the conversation list with the system prompt as the first turn
        self.conversation = []
        # Set a threshold for the similarity score between the user's input and the knowledge base
        self.engine = engine
        self.threshold = float(threshold)
        self.conversation_id = conversation_id


    def display_conversation(self):
        '''
        Display the conversation in a readable format
        '''
        # Iterate through each turn in the conversation
        for turn in self.conversation:
        # Get the role and content of tdef display_conversationhe turn
        # Print out the role and content in a readable format
            role = turn['role']
            content = turn['content']
            if role == 'system':
                print(f'System: {content}')
            elif role == 'user':
                print(f'User: {content}')
            elif role == 'assistant':
                print(f'Assistant: {content}')

            print('-------------')

    def start_new_conversation(self):
        '''
        start a new conversation
        '''
        conversation_id = str(uuid.uuid4())

        # Add the starting prompt to the conversation
        self.conversation = [{'role': 'system', 'content': SYSTEM_PROMPT}]
        print(f'Started conversation {conversation_id}')
        self.conversation_id = conversation_id
                 
    def user_turn(self, message):
        '''
        Handle the user's input/ Process the user's message
        '''
        # Add the user's message to the conversation
        self.conversation.append({"role": "user", "content": message})
        # TODO Get the best matching result from the knowledge base for the user's query

        # Check if the confidence score between the user's input and the document meets the threshold
        
        # Add the context from the knowledge base to the system prompt if we meet the threshold
        # Generate a response from the ChatGPT model using OpenAI's API
        # Add the GPT-3.5 response as a turn in the conversation
        # Return the assistant's response
        pass