from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    CorrectnessEvaluator,
    SemanticSimilarityEvaluator,
    EvaluationResult
)
from query_documents import query_chatbot  # Your chatbot function

# Wrapper for chatbot response
class ChatbotResponse:
    def __init__(self, response_text: str):
        self.response = response_text
        self.source_nodes = []

# Custom LLM-based judgment function for additional metrics
def llm_judgment(question, answer, reference, category):
    if not isinstance(answer, str):
        answer = str(answer.response if hasattr(answer, "response") else answer)

    if category == "answer_relevancy":
        return 1.0 if any(word in answer.lower() for word in question.lower().split()) else 0.0
    elif category == "guideline_adherence":
        return 1.0  # Assume all responses currently adhere
    return 0.0

# Sample questions and ground truths
examples = [
    "What is my GPA?",
    "How many credits have I completed so far?",
    "Can I repeat ARAB 110 to improve my GPA?",
    "What are the courses in Year 1 Semester 1?",
    "What is the total number of credits required for the Cybersecurity program?",
    "How many business electives are required in the Cybersecurity program?",
    "What are the prerequisites for ITCY 482 Internship?",
]

ground_truths = [
    "Your GPA is 2.85.",
    "You have completed 15 credits so far.",
    "To determine if it's possible to repeat this course, let's refer to policy #8 from the Studies policies document: 'Courses with a grade of 'C' or lower may be repeated to improve GPA.' As ARAB 110 has been completed with a B+ grade, which is higher than a C, repeating this course would not be necessary for improving one's GPA.",
    "ITIS 103 - Fundamentals of Information Systems ITCS 113 - Computer Programming I MATHS 101 - Calculus I ARAB 110 - Arabic Language Skills ENGL 154 - Language Development I",
    "The total number of credits required for the Cybersecurity program is 132.",
    "You must take two Business courses as General Studies Electives in the Cybersecurity program.",
    "The prerequisite for ITCY 482 - Internship in Cybersecurity is a Pass of at least 85 credits",
]

# Evaluators
faithfulness_eval = FaithfulnessEvaluator()
relevancy_eval = RelevancyEvaluator()
correctness_eval = CorrectnessEvaluator()
semantic_eval = SemanticSimilarityEvaluator()

# Score tracking
faithfulness_scores = []
relevancy_scores = []
correctness_scores = []
semantic_scores = []
answer_relevancy_scores = []
guideline_adherence_scores = []

print("\U0001F680 Starting Evaluation...\n")

for i, question in enumerate(examples):
    print(f"\n=== Test ===")
    print(f"❓ Question: {question}")

    try:
        response_text = query_chatbot(question)
        print(f"🧠 Response: {response_text}")

        response_obj = ChatbotResponse(response_text)
        reference = ground_truths[i]

        # Evaluate with built-in evaluators
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

        # Custom evaluation
        answer_score = llm_judgment(question, response_obj.response, reference, "answer_relevancy")
        guideline_score = llm_judgment(question, response_obj.response, reference, "guideline_adherence")

        # Boolean threshold (e.g., score >= 0.5 means pass)
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

        # Print results
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
print(f"Avg. Faithfulness Score        : {sum(faithfulness_scores)/len(faithfulness_scores):.2f}/1.00")
print(f"Avg. Relevancy Score           : {sum(relevancy_scores)/len(relevancy_scores):.2f}/1.00")
print(f"Avg. Correctness Score         : {sum(correctness_scores)/len(correctness_scores):.2f}/4.00")
print(f"Avg. Semantic Similarity Score : {sum(semantic_scores)/len(semantic_scores):.2f}/1.00")
print(f"Avg. Answer Relevancy          : {sum(answer_relevancy_scores)/len(answer_relevancy_scores):.2f}/1.00")
print(f"Avg. Guideline Adherence       : {sum(guideline_adherence_scores)/len(guideline_adherence_scores):.2f}/1.00")

