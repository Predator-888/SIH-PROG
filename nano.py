import json

def retrieve_relevant_content(user_question, file_path="quiz.json"):
    """
    Finds the most relevant content blocks from the JSON file based on keywords in the user's question.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    
    keywords = set(user_question.lower().split())
    
    scored_content = []
    
    for module in data.get("modules", []):
        module_text = json.dumps(module).lower()
        score = sum(1 for keyword in keywords if keyword in module_text)
        
        if score > 0:
            # We will retrieve the whole module as context for better AI performance
            scored_content.append({"score": score, "content": module})

    scored_content.sort(key=lambda x: x["score"], reverse=True)
    
    # Combine the content of the top 2 modules for rich context
    top_results_text = ""
    for item in scored_content[:2]:
        top_results_text += json.dumps(item["content"], indent=2) + "\n\n"

    return top_results_text if top_results_text else "No relevant content found."

def main_app_flow():
    """Simulates the entire application workflow."""
    while True:
        # 1. Get User Input
        user_question = input("Hello! What topic would you like to learn about? (or type 'exit' to quit)\n> ")
        if user_question.lower() == 'exit':
            break

        # 2. Retrieve Relevant Knowledge
        print("\nSearching my knowledge base...")
        context = retrieve_relevant_content(user_question)
        
        if "Error:" in context or "No relevant content found" in context:
            print(context)
            continue
        
        print("I've found relevant information!")

        # 3. Offer a Choice
        while True:
            print("\nWhat would you like to do?")
            print("  1. Explain this topic to me.")
            print("  2. Give me a quiz on this topic.")
            print("  3. Choose a different topic.")
            
            try:
                choice = int(input("> "))
                if choice not in [1, 2, 3]:
                    print("Invalid choice, please enter 1, 2, or 3.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # 4. Execute the Choice
        if choice == 1:
            # Prepare the explanation prompt for the AI model
            explanation_prompt = f"""
You are a helpful assistant explaining the concepts of Jeevan Vidya. Based ONLY on the following context, please answer the user's question in a clear and simple way.

--- CONTEXT ---
{context}
--- END CONTEXT ---

USER'S QUESTION: {user_question}

ANSWER:
"""
            print("\n--- PROMPT TO SEND TO AI FOR EXPLANATION ---")
            print(explanation_prompt)

        elif choice == 2:
            # Prepare the quiz generation prompt for the AI model
            quiz_prompt = f"""
You are an expert quiz creator. Based ONLY on the following context, create a multiple-choice quiz with 3 questions to test a user's understanding. For each question, provide 4 options and clearly indicate the correct answer.

--- CONTEXT ---
{context}
--- END CONTEXT ---

quiz:
"""
            print("\n--- PROMPT TO SEND TO AI FOR quiz GENERATION ---")
            print(quiz_prompt)
            
        elif choice == 3:
            continue

if __name__ == "__main__":
    main_app_flow()