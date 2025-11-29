import reflex as rx
from typing import TypedDict, Literal, cast
from app.states.user_state import UserState
from app.states.location_state import LocationState
import operator

# --- TYPED DICTS (No Changes Needed Here) ---

class Choice(TypedDict):
    title: str
    emoji: str
    points: dict[str, int]


class Question(TypedDict):
    id: str
    part: str
    text: str
    choices: dict[str, Choice]
    layout: str | None


class Personality(TypedDict):
    title: str
    description: str
    icon: str
    spots: list[str]


class QuizState(rx.State):
    current_page: Literal[
        "home", "quiz", "results", "locations", "location_detail", "profile", "achievements", "visited_locations"
    ] = "home"
    mobile_menu_open: bool = False
    current_question_index: int = 0
    answers: list[str] = []
    # Initialize scores with the four new dimensions
    scores: dict[str, int] = {"S": 0, "C": 0, "R": 0, "A": 0}
    quiz_finished: bool = False
    # The list now contains only 6 questions, all with 4 choices, mixing old and new.
    questions: list[Question] = [
        {
            "id": "q1",
            "part": "The Nap Environment",
            "text": "What level of noise is perfect for your nap?",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "Silent as a tomb (Noise is the enemy)",
                    "emoji": "🤫",
                    "points": {"R": 2},
                },
                "B": {
                    "title": "A low, constant hum (Background chatter is calming)",
                    "emoji": "☕",
                    "points": {"S": 2},
                },
                "C": {
                    "title": "Anything goes (I can tune out a marching band)",
                    "emoji": "🎧",
                    "points": {"A": 2},
                },
                "D": {
                    "title": "Quiet, but I prefer natural white noise (Rain, fan)",
                    "emoji": "🍃",
                    "points": {"C": 1, "R": 1},
                },
            },
        },
        {
            "id": "q2",
            "part": "The Nap Environment",
            "text": "How do you feel about napping in public view?",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "Anxiety-inducing. I need total privacy.",
                    "emoji": "🥷",
                    "points": {"C": 2},
                },
                "B": {
                    "title": "Slightly thrilling. The risk is part of the fun.",
                    "emoji": "😎",
                    "points": {"S": 2},
                },
                "C": {
                    "title": "It's fine, as long as I'm in a designated spot.",
                    "emoji": "📜",
                    "points": {"R": 2},
                },
                "D": {
                    "title": "Don't care. I'll nap right in the middle of a crowd.",
                    "emoji": "🏙️",
                    "points": {"A": 2},
                },
            },
        },
        {
            "id": "q3",
            "part": "The Nap Surface",
            "text": "Your ideal nap surface is...",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "A plush cloud I can sink into (Ultimate softness)",
                    "emoji": "☁️",
                    "points": {"C": 2},
                },
                "B": {
                    "title": "Firm and supportive (Good for posture, not too squishy)",
                    "emoji": "🪵",
                    "points": {"R": 1, "A": 1},
                },
                "C": {
                    "title": "Whatever's closest (Back of a chair, desk, floor, etc.)",
                    "emoji": "🪨",
                    "points": {"A": 2},
                },
                "D": {
                    "title": "A high vantage point (I like to survey my kingdom)",
                    "emoji": "🏰",
                    "points": {"S": 2},
                },
            },
        },
        {
            "id": "q4",
            "part": "The Nap Surface",
            "text": "How much 'gear' do you bring to a nap?",
            "choices": {
                "A": {
                    "title": "Everything: Mask, pillow, special blanket, earplugs.",
                    "emoji": "🎒",
                    "points": {"C": 1, "R": 2},
                },
                "B": {
                    "title": "Maybe a hoodie/bag for a makeshift pillow.",
                    "emoji": "🧣",
                    "points": {"S": 2},
                },
                "C": {
                    "title": "Nothing. I use what's available.",
                    "emoji": "🤷",
                    "points": {"A": 2},
                },
                "D": {
                    "title": "Just headphones (Music is my blanket)",
                    "emoji": "🎧",
                    "points": {"C": 1, "S": 1},
                },
            },
        },
        {
            "id": "q5",
            "part": "The Nap Schedule",
            "text": "A good nap happens when...",
            "choices": {
                "A": {
                    "title": "It's exactly 2:00 PM (Precision timing is key).",
                    "emoji": "⏰",
                    "points": {"R": 2},
                },
                "B": {
                    "title": "I'm suddenly tired and have an unexpected opportunity.",
                    "emoji": "⚡",
                    "points": {"S": 2, "A": 1},
                },
                "C": {
                    "title": "I've carved out a comfortable block of at least 60-90 minutes.",
                    "emoji": "🛌",
                    "points": {"C": 2},
                },
                "D": {
                    "title": "Whenever I blink for too long (Accidental nap)",
                    "emoji": "😑",
                    "points": {"A": 2},
                },
            },
        },
        {
            "id": "q6",
            "part": "The Nap Schedule",
            "text": "If your favorite spot is taken, you...",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "Get mad and refuse to nap until tomorrow (Only the best will do).",
                    "emoji": "😠",
                    "points": {"R": 2},
                },
                "B": {
                    "title": "Explore until I find a new, novel, or fun place to try.",
                    "emoji": "🗺️",
                    "points": {"A": 2, "S": 1},
                },
                "C": {
                    "title": "Find the *next* most comfortable place immediately.",
                    "emoji": "🛋️",
                    "points": {"C": 2},
                },
                "D": {
                    "title": "Ask if they want to share (Nap party)",
                    "emoji": "👯",
                    "points": {"S": 2},
                },
            },
        },
    ]
    answer_stats: dict[str, dict[str, int]] = {
        "q1": {"A": 25, "B": 25, "C": 25, "D": 25},
        "q2": {"A": 25, "B": 25, "C": 25, "D": 25},
        "q3": {"A": 25, "B": 25, "C": 25, "D": 25},
        "q4": {"A": 25, "B": 25, "C": 25, "D": 25},
        "q5": {"A": 25, "B": 25, "C": 25, "D": 25},
        "q6": {"A": 25, "B": 25, "C": 25, "D": 25},
    }
    personalities: dict[str, Personality] = {
        "S": {
            "title": "The Thrill Napper",
            "description": "You thrive on the buzz of activity. A low hum of noise, people moving, and the slight risk of being noticed actually helps you drift off. **Your nap is a covert mission.**",
            "icon": "ghost",
            "spots": ["the-spynap-alley", "the-stairwell-stealth"],
        },
        "C": {
            "title": "The Comfort Connoisseur",
            "description": "Your non-negotiable is comfort. You need plush surfaces, darkness, and a controlled temperature. You seek an immersive, private cocoon for your deepest rest.",
            "icon": "couch",
            "spots": ["cloud-nine-credit", "the-modular-dream", "the-curtaincall-nap"],
        },
        "R": {
            "title": "The Precision Planner",
            "description": "Napping is a dedicated, controlled ritual. You need a designated, quiet space with minimal interruption to maximize efficiency. **Order equals rest.**",
            "icon": "alarm-clock-check",
            "spots": ["the-bobafueled-snooze", "the-public-isolation"],
        },
        "A": {
            "title": "The Spontaneous Drifter",
            "description": "You are a master of napping anywhere, anytime. Conditions don't matter; convenience and opportunity do. The world is your bed.",
            "icon": "earth",
            "spots": ["the-urban-zen", "the-shade-throne", "the-stonecold-zen"],
        },
        "SR": {
            "title": "The Stealth Scholar",
            "description": "A rare blend of routine and risk. You want a quiet, controlled setting but crave the mild stimulation of a public, studious environment.",
            "icon": "book-user",
            "spots": ["the-spynap-alley", "the-public-isolation"],
        },
        "Default": {
            "title": "Calculating Persona...",
            "description": "Your unique sleep profile is being analyzed by our highly-trained digital gnomes.",
            "icon": "loader",
            "spots": ["Please wait..."],
        },
    }

    @rx.event
    def set_page(self, page_name: str):
        self.current_page = cast(
            Literal[
                "home", "quiz", "results", "locations", "location_detail", "profile", "achievements", "visited_locations"
            ],
            page_name,
        )
        self.mobile_menu_open = False
        if page_name == "quiz":
            yield QuizState.reset_quiz

    @rx.event
    async def handle_answer(self, question_index: int, answer: str):
        from app.states.user_state import UserState
        from app.states.location_state import LocationState
        
        self.answers.append(answer)
        question = self.questions[question_index]
        points_to_add = question["choices"][answer]["points"]
        for dimension, value in points_to_add.items():
            self.scores[dimension] += value
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
        else:
            self.quiz_finished = True
            user_state = await self.get_state(UserState)
            location_state = await self.get_state(LocationState)
            
            # Award XP for completing quiz
            old_level = user_state.level
            user_state.xp += 250
            new_level = user_state.level
            
            # Check for level up
            if new_level > old_level:
                yield user_state.level_up_notification(new_level)
            
            yield rx.toast.success(
                "🎉 Quiz Complete! +250 XP",
                duration=3000,
                position="bottom-right"
            )
            
            # Check for nap legend achievement
            rated_all = len(location_state.ratings) == len(location_state.locations)
            if rated_all:
                yield user_state.unlock_achievement("nap-legend")
            yield QuizState.set_page("results")

    @rx.event
    def toggle_mobile_menu(self):
        self.mobile_menu_open = not self.mobile_menu_open

    @rx.event
    def reset_quiz(self):
        self.current_question_index = 0
        self.answers = []
        # Ensure scores are reset for all four dimensions
        self.scores = {"S": 0, "C": 0, "R": 0, "A": 0}
        self.quiz_finished = False
        self.current_page = "quiz"

    @rx.var
    def current_question(self) -> Question | None:
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    @rx.var
    def progress_percent(self) -> str:
        # Progress is calculated based on the reduced 6 questions
        if not self.questions:
             return "0%"
        progress = (self.current_question_index / len(self.questions)) * 100
        return f"{progress:.0f}%"

    @rx.var
    def personality_type(self) -> str:
        if not self.quiz_finished:
            return "Default"
            
        # Get dominant trait
        dominant_trait = max(self.scores, key=self.scores.get)
        dominant_score = self.scores[dominant_trait]
        
        # Check for a strong tie with another top score
        second_highest_score = 0
        second_dominant_trait = ""
        for trait, score in self.scores.items():
            if score > second_highest_score and trait != dominant_trait:
                second_highest_score = score
                second_dominant_trait = trait

        # Custom Hybrid Logic: Stealth Scholar (SR) if S and R are tied for highest
        if dominant_score > 0 and dominant_score == second_highest_score:
            if {dominant_trait, second_dominant_trait} == {"S", "R"}:
                return "SR"
            
        # Return the single dominant trait key
        return dominant_trait

    @rx.var
    def personality_details(self) -> Personality:
        return self.personalities.get(
            self.personality_type, self.personalities["Default"]
        )

    @rx.var
    def user_answer_stats(self) -> dict[str, int]:
        stats = {}
        if not self.answers:
            return {}
        for i, question in enumerate(self.questions):
            if i < len(self.answers):
                user_answer = self.answers[i]
                question_id = question["id"]
                # Need to safely access keys for new questions
                if question_id in self.answer_stats and user_answer in self.answer_stats[question_id]:
                    stats[question_id] = self.answer_stats[question_id][user_answer]
                else:
                    # Fallback for questions without detailed stats
                    stats[question_id] = 50 # Default to 50% percentile
        return stats