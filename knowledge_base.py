import json

class KnowledgeBase:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_knowledge_base()

    def load_knowledge_base(self):
        """Load the knowledge base from a JSON file."""
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Knowledge base file not found. Starting with an empty knowledge base.")
            return {}

    def get_issue_data(self, issue):
        """Retrieve details of a specific issue."""
        return self.data.get(issue, None)

    def add_issue(self, issue, symptoms, causes, solution):
        """Add a new issue to the knowledge base."""
        if issue in self.data:
            print(f"Issue '{issue}' already exists in the knowledge base.")
            return False

        self.data[issue] = {
            "symptoms": symptoms,
            "causes": causes,
            "solution": solution
        }
        self.save_knowledge_base()
        return True

    def update_issue(self, issue, symptoms=None, causes=None, solution=None):
        """Update an existing issue in the knowledge base."""
        if issue not in self.data:
            print(f"Issue '{issue}' not found in the knowledge base.")
            return False

        if symptoms:
            self.data[issue]["symptoms"] = symptoms
        if causes:
            self.data[issue]["causes"] = causes
        if solution:
            self.data[issue]["solution"] = solution

        self.save_knowledge_base()
        return True

    def delete_issue(self, issue):
        """Delete an issue from the knowledge base."""
        if issue in self.data:
            del self.data[issue]
            self.save_knowledge_base()
            return True
        print(f"Issue '{issue}' not found in the knowledge base.")
        return False

    def save_knowledge_base(self):
        """Save the current knowledge base to the JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)
