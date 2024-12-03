from experta import *
from knowledge_base import KnowledgeBase

class VehicleIssue(Fact):
    """Information about the vehicle issue."""
    pass

class GarageServiceAssistant(KnowledgeEngine):
    def __init__(self, knowledge_file):
        super().__init__()
        self.knowledge_base = KnowledgeBase(knowledge_file)

    @Rule(VehicleIssue(issue=MATCH.issue))
    def diagnose_issue(self, issue):
        data = self.knowledge_base.get_issue_data(issue)
        if data:
            self.declare(Fact(
                symptoms=data['symptoms'],
                causes=data['causes'],
                solution=data['solution']
            ))
        else:
            self.declare(Fact(solution="No solution found for the provided issue."))

    @Rule(Fact(solution=MATCH.solution))
    def provide_solution(self, solution):
        print(f"Solution: {solution}")
