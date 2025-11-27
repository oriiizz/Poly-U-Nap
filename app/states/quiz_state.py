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
        "home", "quiz", "results", "locations", "location_detail", "profile"
    ] = "home"
    mobile_menu_open: bool = False
    current_question_index: int = 0
    answers: list[str] = []
    # Initialize scores with the four new dimensions
    scores: dict[str, int] = {"S": 0, "C": 0, "R": 0, "A": 0}
    quiz_finished: bool = False
    # The list now contains only 6 questions, all with 4 choices, mixing old and new.
    questions: list[Question] = [
        # NEW Q1 (The Bedside Creed) - Part I
        {
            "id": "nq1",
            "part": "PART I: The Bedside Creed",
            "text": "When you spot a bed, what’s your instinct?",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "The Iron Spine (Hard as justice, firm as fate)",
                    "emoji": "🪵",
                    "points": {"C": 2}, # C – Comfort (Sturdy support)
                },
                "B": {
                    "title": "The Cloud Whisperer (Soft, cozy, infinite fluff)",
                    "emoji": "☁️",
                    "points": {"C": 3}, # C – Comfort (Total plush nirvana)
                },
                "C": {
                    "title": "The Ritualist (Your altar, your temple, your sacred zone)",
                    "emoji": "🕯️",
                    "points": {"R": 3}, # R – Ritual
                },
                "D": {
                    "title": "The Battle Sleeper (Sleep is WAR, thrive in hostile conditions)",
                    "emoji": "⚔️",
                    "points": {"S": 2}, # S – Stimulation
                },
            },
        },
        # NEW Q2 (The Bedside Creed) - Part I
        {
            "id": "nq2",
            "part": "PART I: The Bedside Creed",
            "text": "What makes a *perfect nap*?",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "Thrill of the Spot (Nap where you *shouldn’t*)",
                    "emoji": "⚡",
                    "points": {"S": 3}, # S – Stimulation
                },
                "B": {
                    "title": "Sweet Serenity (Soft, quiet, kind environment)",
                    "emoji": "🌸",
                    "points": {"C": 2}, # C – Comfort
                },
                "C": {
                    "title": "The Ceremony (Candles, music, the same blanket every time)",
                    "emoji": "🔮",
                    "points": {"R": 3}, # R – Ritual
                },
                "D": {
                    "title": "Driftwood Soul (Any time, any place, any floor)",
                    "emoji": "🍃",
                    "points": {"A": 3}, # A – Adaptability
                },
            },
        },
        # OLD Q2 (Updated to 4 choices and new score logic)
        {
            "id": "q2",
            "part": "Part 1: The Spark",
            "text": "Your ideal napping light level?",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "Pitch Black Void",
                    "emoji": "🌑",
                    "points": {"C": 2}, # Preference for darkness suggests comfort/control
                },
                "B": {
                    "title": "A Little Ambient Light (Curtains drawn)",
                    "emoji": "🌤️",
                    "points": {"C": 1}, # Neutral/Medium comfort
                },
                "C": {
                    "title": "Direct, Blazing Sunlight (Window seat)",
                    "emoji": "☀️",
                    "points": {"A": 2}, # Adaptable, can sleep anywhere
                },
                "D": {
                    "title": "Dim, non-disruptive, specific light (e.g. nightlight)",
                    "emoji": "🕯️",
                    "points": {"R": 2}, # Ritual/Preference
                },
            },
        },
        # NEW Q4 (Field Test Simulation) - Part II
        {
            "id": "nq4",
            "part": "PART II: Field Test Simulation",
            "text": "A new nap spot appears on your map. Your move?",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "Hardcore Challenge (The harder the surface, the greater the glory)",
                    "emoji": "🧗",
                    "points": {"S": 2}, # S – Stimulation/Challenge
                },
                "B": {
                    "title": "Cozy Den (If it’s soft and quiet, it’s already home)",
                    "emoji": "🪶",
                    "points": {"C": 3}, # C – Comfort
                },
                "C": {
                    "title": "Hidden Nook (Secret corners call to your inner stealth napper)",
                    "emoji": "🕳️",
                    "points": {"S": 1, "R": 1}, # Stealth/Ritual of hiding
                },
                "D": {
                    "title": "Public Legend (Napping proudly in plain sight)",
                    "emoji": "🌆",
                    "points": {"A": 2}, # A – Adaptability/Public
                },
            },
        },
        # NEW Q5 (Deep Nap Philosophy) - Part III
        {
            "id": "nq5",
            "part": "PART III: Deep Nap Philosophy",
            "text": "Your nap soundtrack of choice?",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "Chaos Ambience (Arguing neighbors, street sounds)",
                    "emoji": "🔊",
                    "points": {"S": 3}, # S – Stimulation
                },
                "B": {
                    "title": "Sleep Sanctuary (Total silence or a soft lullaby)",
                    "emoji": "🎧",
                    "points": {"C": 2}, # C – Comfort
                },
                "C": {
                    "title": "Ritual Noise (White noise machine, specific playlist)",
                    "emoji": "🎛️",
                    "points": {"R": 2}, # R – Ritual
                },
                "D": {
                    "title": "Freestyler (Can nap through anything, from construction to karaoke)",
                    "emoji": "🌀",
                    "points": {"A": 3}, # A – Adaptability
                },
            },
        },
        # OLD Q10 (Updated to 4 choices and new score logic)
        {
            "id": "q10",
            "part": "Part 4: The Chameleon",
            "text": "Napping in public?",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "A big no from me (Need absolute privacy)",
                    "emoji": "🙅",
                    "points": {"C": 1}, # C – Comfort/Security
                },
                "B": {
                    "title": "Anywhere is a good spot (Embrace the chaos)",
                    "emoji": "😎",
                    "points": {"A": 2}, # A – Adaptability
                },
                "C": {
                    "title": "Only if I am desperate (A last resort)",
                    "emoji": "😥",
                    "points": {"R": 1, "C": 1}, # R – Breaks the ritual/C - Reluctantly
                },
                "D": {
                    "title": "A quiet, public place is ideal (Like a library nook)",
                    "emoji": "🤫",
                    "points": {"S": 1, "R": 1}, # Blends S (public) and R (quiet) - LHP lean
                },
            },
        },
        # NOTE: Original questions 1, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, and new questions nq3, nq6, nq7, nq8 are excluded
        # to meet the maximum question count of 6.
    ]
    answer_stats: dict[str, dict[str, int]] = {
        "nq1": {"A": 20, "B": 50, "C": 10, "D": 20},
        "nq2": {"A": 15, "B": 40, "C": 30, "D": 15},
        "q2": {"A": 40, "B": 60, "C": 0, "D": 0},
        "nq4": {"A": 10, "B": 50, "C": 20, "D": 20},
        "nq5": {"A": 10, "B": 40, "C": 30, "D": 20},
        "q10": {"A": 15, "B": 85, "C": 0, "D": 0},
    }
    personalities: dict[str, Personality] = {
        "LDP": {
            "title": "Lecture Hall Phantom (LDP)",
            "description": "Thrives on tension and danger. You nap at the edge of chaos. Your ability to nap is triggered by stimulation, not the lack of it.",
            "icon": "⚡",  # Using emoji instead of 'ghost' to match the new scoring system's icons
            "spots": ["union-sofa", "library-alcove"],
        },
        "CDM": {
            "title": "Couch Daydreamer (CDM)",
            "description": "Comfort is law. You rest like royalty, anywhere soft. You are a connoisseur of cushions, a baron of blankets, and a master of the plush arts.",
            "icon": "☁️",
            "spots": ["union-sofa", "basement-lounge"],
        },
        "PNP": {
            "title": "Precision Napper (PNP)",
            "description": "Every nap is a sacred rite, optimized to perfection. You have a designated time, a perfect spot, and a full pre-sleep checklist.",
            "icon": "🕯️",
            "spots": ["library-alcove", "basement-lounge"],
        },
        "WSD": {
            "title": "Wandering Sleep Deity (WSD)",
            "description": "Can nap on clouds, cliffs, or chaos. The world is your bed. Your adaptability is legendary.",
            "icon": "🍃", # Using emoji instead of 'earth' to match the new scoring system's icons
            "spots": ["quad-tree", "union-sofa"],
        },
        "LHP": {
            "title": "Library Slacker (LHP)",
            "description": "A rare hybrid forged from equal parts Stimulation (S) and Ritual (R). You thrive in peaceful, public realms where stealth and ceremony intertwine.",
            "icon": "book-user",
            "spots": ["library-alcove", "quad-tree"],
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
                "home", "quiz", "results", "locations", "location_detail", "profile"
            ],
            page_name,
        )
        self.mobile_menu_open = False
        if page_name == "quiz":
            yield QuizState.reset_quiz

    @rx.event
    async def handle_answer(self, question_index: int, answer: str):
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
            # This logic will need to be adjusted based on the final UserState/LocationState implementation
            # For now, it's left as is.
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

        # Find the highest score(s)
        max_score = max(self.scores.values())
        dominant_traits = [trait for trait, score in self.scores.items() if score == max_score]

        # Check for the specific S/R hybrid (LHP)
        if len(dominant_traits) == 2 and "S" in dominant_traits and "R" in dominant_traits and max_score > 0:
            # Check if S and R are strictly greater than or equal to C and A
            is_lhp = True
            for trait in ["C", "A"]:
                 if self.scores.get(trait, 0) > max_score:
                      is_lhp = False
                      break
            if is_lhp:
                return "LHP"

        # If it's a single dominant trait or another tie, default to the one in the table order (S, C, R, A)
        if "S" in dominant_traits:
            return "LDP"
        elif "C" in dominant_traits:
            return "CDM"
        elif "R" in dominant_traits:
            return "PNP"
        elif "A" in dominant_traits:
            return "WSD"
        
        return "Default"

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