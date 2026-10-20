from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    CorrectnessEvaluator,
    SemanticSimilarityEvaluator,
    EvaluationResult,
)
from unifiedquery_documents import query_chatbot  # Your actual chatbot function

# Wrapper to simulate a response object
class ChatbotResponse:
    def __init__(self, response_text: str):
        self.response = response_text
        self.source_nodes = []

# Custom LLM-based scoring for additional metrics
def llm_judgment(question, answer, reference, category):
    if not isinstance(answer, str):
        answer = str(answer.response if hasattr(answer, "response") else answer)

    if category == "answer_relevancy":
        return 1.0 if any(word in answer.lower() for word in question.lower().split()) else 0.0
    elif category == "guideline_adherence":
        return 1.0  # Placeholder logic
    return 0.0

# Questions and ground truths
examples = [
    "What is the total credit for cybersecurity",
    "What is the maximum acceptable absense per course",
    "What is the total credit for computer science",
    "what is the total credit for network engineering",
    "What are the prerequisites for taking the internship course ITCY 482 in cybersecurity program",
    "How many business electives do I need to take in cybersecurity program"
]

ground_truths = [
    "The total credits required for the Cybersecurity program are 132.",
    "The maximum acceptable absence per course is 25% of the total number of classes.",
    "The total credits required for the Computer Science program are 130.",
    "the total credits required fro the Network engineering program are 135",
    "The prerequisite for taking ITCY 482 Internship in Cybersecurity is passing 85 credits.",
    "According to the program components, students must select two Business courses as part of their General Studies Elective requirements"
]


# Initialize evaluators
faithfulness_eval = FaithfulnessEvaluator()
relevancy_eval = RelevancyEvaluator()
correctness_eval = CorrectnessEvaluator()
semantic_eval = SemanticSimilarityEvaluator()

# Score trackers
faithfulness_scores = []
relevancy_scores = []
correctness_scores = []
semantic_scores = []
answer_relevancy_scores = []
guideline_adherence_scores = []

print("🚀 Starting Evaluation...\n")

for i, question in enumerate(examples):
    print(f"\n=== Test ===")
    print(f"❓ Question: {question}")

    try:
        response_text = query_chatbot(question)
        print(f"🧠 Response: {response_text}")

        response_obj = ChatbotResponse(response_text)
        reference = ground_truths[i]

        # Run evaluations
        faithfulness_result = faithfulness_eval.evaluate_response(
            query=question,
            response=response_obj.response,
            context=reference,
            reference=reference,
        )
        relevancy_result = relevancy_eval.evaluate_response(
            query=question,
            response=response_obj.response,
            reference=reference,
        )
        correctness_result = correctness_eval.evaluate_response(
            query=question,
            response=response_obj.response,
            reference=reference,
        )
        semantic_result = semantic_eval.evaluate_response(
            query=question,
            response=response_obj.response,
            reference=reference,
        )

        # Custom scores
        answer_score = llm_judgment(question, response_obj.response, reference, "answer_relevancy")
        guideline_score = llm_judgment(question, response_obj.response, reference, "guideline_adherence")

        # Boolean results (pass/fail)
        answer_relevancy_pass = answer_score >= 0.5
        guideline_adherence_pass = guideline_score >= 0.5

        # Store scores
        faithfulness_scores.append(faithfulness_result.score or 0.0)
        relevancy_scores.append(relevancy_result.score or 0.0)
        correctness_score = min(correctness_result.score, 4.0) if correctness_result.score else 0.0
        correctness_scores.append(correctness_score)
        semantic_scores.append(semantic_result.score or 0.0)
        answer_relevancy_scores.append(answer_score)
        guideline_adherence_scores.append(guideline_score)

        # Display results
        print(f"✅ Faithfulness        : {faithfulness_result.passing} - {faithfulness_result.score:.2f}/1.00")
        print(f"✅ Relevancy           : {relevancy_result.passing} - {relevancy_result.score:.2f}/1.00")
        print(f"✅ Correctness         : {correctness_result.passing} - {correctness_score:.2f}/4.00")
        print(f"✅ Semantic Similarity : {semantic_result.passing} - {semantic_result.score:.2f}/1.00")
        print(f"✅ Answer Relevancy    : {answer_relevancy_pass} - {answer_score:.2f}/1.00")
        print(f"✅ Guideline Adherence : {guideline_adherence_pass} - {guideline_score:.2f}/1.00")

    except Exception as e:
        print("⚠️ Error:", str(e))
        faithfulness_scores.append(0.0)
        relevancy_scores.append(0.0)
        correctness_scores.append(0.0)
        semantic_scores.append(0.0)
        answer_relevancy_scores.append(0.0)
        guideline_adherence_scores.append(0.0)

# Summary
print("\n📊 Evaluation Summary:")
print(f"Avg. Faithfulness Score       : {sum(faithfulness_scores)/len(faithfulness_scores):.2f}/1.00")
print(f"Avg. Relevancy Score          : {sum(relevancy_scores)/len(relevancy_scores):.2f}/1.00")
print(f"Avg. Correctness Score        : {sum(correctness_scores)/len(correctness_scores):.2f}/4.00")
print(f"Avg. Semantic Similarity Score: {sum(semantic_scores)/len(semantic_scores):.2f}/1.00")
print(f"Avg. Answer Relevancy Score   : {sum(answer_relevancy_scores)/len(answer_relevancy_scores):.2f}/1.00")
print(f"Avg. Guideline Adherence Score: {sum(guideline_adherence_scores)/len(guideline_adherence_scores):.2f}/1.00")

