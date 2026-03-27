import random

class NLPBot:

    def __init__(self):
        # Training data categories
        self.responses = {
            "stress": [
                "Don't worry, you're not alone. Tell me your skills, I'll guide you clearly.",
                "It's okay to feel stressed. Let's start step by step.",
                "Stay calm. We will sort your placement journey together."
            ],
            "greeting": [
                "Hello! How can I help you today?",
                "Hi! Tell me how I can assist with your placements.",
                "Hey! Ready to prepare for placements?"
            ],
            "resume": [
                "Upload your resume and I’ll analyze it instantly.",
                "I can improve your resume. Upload it for suggestions.",
                "Your resume is important — send it here and I’ll review."
            ],
            "job": [
                "Tell me your skills and experience, I’ll suggest job roles.",
                "Share your tech stack, I’ll match you with companies.",
                "Let me know your skills — I’ll find suitable jobs."
            ],
            "skills": [
                "List your skills and projects, I’ll help you improve them.",
                "Tell me your skills so I can suggest companies.",
                "Your skills decide placements. What are your top 3 skills?"
            ],
            "default": [
                "Got it! Tell me more so I can help.",
                "Okay, explain a bit more.",
                "Interesting. Want guidance for placements, jobs or resume?"
            ]
        }

    def detect_intent(self, msg: str) -> str:
        m = msg.lower()

        if "stress" in m or "tension" in m or "scared" in m:
            return "stress"
        if "hi" in m or "hello" in m or "hey" in m:
            return "greeting"
        if "resume" in m or "cv" in m:
            return "resume"
        if "job" in m or "company" in m or "placement" in m:
            return "job"
        if "skill" in m or "project" in m:
            return "skills"

        return "default"

    def reply(self, msg: str) -> str:
        intent = self.detect_intent(msg)
        return random.choice(self.responses[intent])


nlp_bot = NLPBot()
