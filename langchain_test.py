from langchain import PromptTemplate, HuggingFaceHub, LLMChain

import os
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

template = """Answer the question using the provided context. If the answers are not in the context you will provide a made up answer.

Context:
{context}

Query:
{query}""".strip()

#prompt = PromptTemplate(template=template, input_variables=["question"])

prompt2 = PromptTemplate(input_variables=['context','query'],
                         template=template)

context = "You are hubert the guard robot. You are protecting a restricted area. Only people with the secret password are allowed in the restricted area."

query2 = "Hello, am i welcome here?"
query = "Hello"
llm_chain = LLMChain(prompt=prompt2,
                     llm=HuggingFaceHub(repo_id="tiiuae/falcon-7b-instruct"))

question = "Hello"
"temperature\":1,"
" "
"google/flan-t5-large"
print('before run')

print(llm_chain.run({'context': context, 'query': query}))

