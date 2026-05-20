questions = [
    {"question": "What is Python?", "answer": "programming language"},
    {"question": "What is HTML?", "answer": "markup language"},
    {"question": "What is Flask?", "answer": "web framework"},
    {"question": "What is a database used for?", "answer": "store data"},
    {"question": "What is a terminal", "answer": "a command line interface"}
]


class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.current_index = 0
        self.score = 0
        self.user_answers = {}

    def get_question(self):
        return self.questions[self.current_index]["question"]
    
    def check_answer(self, user_answer):
        question = self.questions[self.current_index] # Question dictionary contain question and answer
        correct_answer = question["answer"]
        self.user_answers[question["question"]] = user_answer

        if user_answer == correct_answer:
            self.score += 1
        self.current_index += 1

    def finished(self):
        return self.current_index == len(self.questions)