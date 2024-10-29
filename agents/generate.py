from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT="""

Generate working Python code for the task highlighted.
The output should only be code. No introduction or complementary text.

Specifically, please consider the following aspects:

1. Functionality:
   - Ensure that the code fully addresses and accomplishes the highlighted task.
   - Include any necessary imports and dependencies.

2. Code Readability:
   - Use clear and descriptive variable names.
   - Structure the code logically, with well-defined functions or classes.
   - Add comments to explain non-obvious parts of the code.

3. Error Handling:
   - Implement appropriate error handling to manage potential issues or edge cases.
   - Include try-except blocks where necessary.

4. Efficiency:
   - Optimize the code for performance where applicable.
   - Avoid unnecessary computations or redundant code.

5. Best Practices:
   - Follow industry best practices for Python coding.
   - Adhere to a recognized style guide, such as PEP 8.

Please only provide working Python code that meets these criteria. Thank you!
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{query}"),
    ]
)

generate_chain = prompt | ChatOpenAI(model="gpt-4o", temperature= 0.7)
