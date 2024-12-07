
from experta import *
import json

class CarProblemEngine(KnowledgeEngine):
    def __init__(self, knowledge_base):
        super().__init__()
        self.knowledge_base = knowledge_base
        self.result = None

    def diagnose(self, issue, symptom, answers):
        self.reset()
        self.declare(Fact(issue=issue, symptom=symptom, answers=answers))
        self.run()
        return self.result

    @Rule(Fact(issue=MATCH.issue), Fact(symptom=MATCH.symptom), Fact(answers=MATCH.answers))
    def apply_rule(self, issue, symptom, answers):
        best_match = None
        max_matched_answers = 0
        
        for rule in self.knowledge_base["rules"]:
            if rule["issue"] == issue and rule["symptom"] == symptom:
                # Calculate how many answers match for this rule
                matched_answers = sum(
                    answers.get(q["question"]) == q["expected_answer"] 
                    for q in rule["questions"]
                )
                if matched_answers > max_matched_answers:
                    max_matched_answers = matched_answers
                    best_match = rule

        if best_match:
            if max_matched_answers == len(best_match["questions"]):  
                self.result = {
                    "solution": best_match["solution"],
                    "explanation": best_match["explanation"],
                    "alternative": best_match["alternative"],
                }
            else:  
                self.result = {
                    "solution": best_match["solution"],
                    "explanation": (
                        "Some answers didn't match the expected input. "
                        "This is the best possible solution based on your answers."
                    ),
                    "alternative": best_match["alternative"],
                }
        else:
            # Fallback if no rules match
            self.result = {
                "solution": "Diagnosis not available.",
                "explanation": "No rules matched your inputs.",
                "alternative": "Please consult a professional mechanic for further assistance.",
            }

