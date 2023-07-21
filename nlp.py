
import openai

# Set your OpenAI API key
openai.api_key = "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"

def perform_query_analysis(query):
    # Construct the prompt with the query for analysis
    prompt = f"Query Analysis: {query}"

    # Send the prompt as an API request to GPT-3
    response = openai.Completion.create(
        engine="text-davinci-002",  # Use "text-davinci-002" for GPT-3.5-turbo
        prompt=prompt,
        max_tokens=100,  # Control the length of the generated response
    )

    # Access the generated response from the API
    generated_text = response.choices[0].text

    return generated_text

# Example usage:
query_to_analyze = "What are the symptoms of COVID-19?"
result = perform_query_analysis(query_to_analyze)

print("Query:", query_to_analyze)
print("Analysis Result:", result)
