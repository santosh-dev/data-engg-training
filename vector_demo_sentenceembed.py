# used in applications requiring efficient text embeddings, 
# such as search engines, recommendation systems, and 
# other NLP tasks.


from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
sentences = ['Your use cases, or goals, and data determine the strategy, technology, and tools needed to transform your business needs into practical solutions. AI and GenAI can unlock data insights, improve productivity, redefine the customer experience, and accelerate innovation.',
             'Dell AI Factory Data fuels your AI factory with your most valuable data often residing on-premises and at the edge, in places where you have exclusive ownership.',
             'Put Any Dell Data To Work Anywhere In Any Way Intel Artificial Intelligence Technology.']

sentence_embeddings = model.encode(sentences)

for sentence, embedding in zip(sentences, sentence_embeddings):
    print("Sentence:", sentence)
    print("Embedding:", embedding)
    print("")