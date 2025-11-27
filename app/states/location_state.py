import reflex as rx
from typing import TypedDict, cast
import qrcode
import io
import base64
from collections import Counter


class Rating(TypedDict):
    comfort: int
    quietness: int
    accessibility: int
    vibe_check: int
    danger: int


class Location(TypedDict):
    id: str
    name: str
    description: str
    icon: str
    model_id: str


class LocationState(rx.State):
    locations: list[Location] = [
        {
            "id": "library-alcove",
            "name": "Library Alcove 3F",
            "description": "A forgotten corner on the third floor, where the scent of old books lulls you to sleep. Occasional page-turning sounds.",
            "icon": "book",
            "model_id": "b26a267e5a2a4779a0c55814ded990e9",
        },
        {
            "id": "union-sofa",
            "name": "Student Union Sofa",
            "description": "A surprisingly comfy sofa near the perpetually-broken vending machine. High traffic, but a strategic nap spot.",
            "icon": "couch",
            "model_id": "54ffbfc1e493462e800e8a5935f1ca90",
        },
        {
            "id": "quad-tree",
            "name": "The Great Oak on the Quad",
            "description": "Shade-abundant and grass-cushioned. Risk of frisbees and overly-enthusiastic squirrels.",
            "icon": "tree-pine",
            "model_id": "b26a267e5a2a4779a0c55814ded990e9",
        },
        {
            "id": "basement-lounge",
            "name": "Arts Building Basement Lounge",
            "description": "Eerily quiet and perpetually cool. The hum of the building's entrails is your only companion.",
            "icon": "warehouse",
            "model_id": "b26a267e5a2a4779a0c55814ded990e9",
        },
    ]
    ratings: dict[str, list[Rating]] = {}
    selected_location_id: str | None = None
    new_rating: Rating = {
        "comfort": 3,
        "quietness": 3,
        "accessibility": 3,
        "vibe_check": 3,
        "danger": 3,
    }

    @rx.event
    async def select_location(self, location_id: str):
        from app.states.quiz_state import QuizState

        self.selected_location_id = location_id
        quiz_state = await self.get_state(QuizState)
        quiz_state.current_page = "location_detail"

    @rx.event
    def set_new_rating_value(self, category: str, value: str):
        self.new_rating[category] = int(value)

    @rx.event
    async def submit_rating(self):
        if self.selected_location_id:
            from app.states.user_state import UserState
            from app.states.quiz_state import QuizState

            if self.selected_location_id not in self.ratings:
                self.ratings[self.selected_location_id] = []
            self.ratings[self.selected_location_id].append(self.new_rating.copy())
            user_state = await self.get_state(UserState)
            if all((v == 5 for v in self.new_rating.values())):
                yield user_state.unlock_achievement("5-star-sleeper")
            if len(self.ratings) >= 3:
                yield user_state.unlock_achievement("secret-spot-explorer")
            if len(self.ratings) == len(self.locations):
                yield user_state.unlock_achievement("all-area-conqueror")
                quiz_state = await self.get_state(QuizState)
                if quiz_state.quiz_finished:
                    yield user_state.unlock_achievement("nap-legend")
            self.new_rating = {
                "comfort": 3,
                "quietness": 3,
                "accessibility": 3,
                "vibe_check": 3,
                "danger": 3,
            }
            yield rx.toast(
                "Rating submitted! Thanks for your contribution to the nap archives.",
                duration=3000,
            )
            return

    @rx.var
    def selected_location(self) -> Location | None:
        if self.selected_location_id:
            return next(
                (
                    loc
                    for loc in self.locations
                    if loc["id"] == self.selected_location_id
                ),
                None,
            )
        return None

    def _generate_qr_code(self, data: str) -> str:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#00ff9f", back_color="#0a0a0f")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

    @rx.var
    def selected_location_qr_code(self) -> str:
        if self.selected_location:
            qr_data = f"sleep-scan-repeat://location/{self.selected_location['id']}"
            return self._generate_qr_code(qr_data)
        return self._generate_qr_code("error")

    def _calculate_average(self, ratings: list[int]) -> float:
        if not ratings:
            return 0.0
        return sum(ratings) / len(ratings)

    @rx.var
    def average_ratings(self) -> dict[str, dict[str, float]]:
        avg_ratings = {}
        for loc_id, rating_list in self.ratings.items():
            if not rating_list:
                avg_ratings[loc_id] = {
                    "comfort": 0,
                    "quietness": 0,
                    "accessibility": 0,
                    "vibe_check": 0,
                    "danger": 0,
                    "overall": 0,
                }
                continue
            comfort_avg = self._calculate_average([r["comfort"] for r in rating_list])
            quietness_avg = self._calculate_average(
                [r["quietness"] for r in rating_list]
            )
            accessibility_avg = self._calculate_average(
                [r["accessibility"] for r in rating_list]
            )
            vibe_avg = self._calculate_average([r["vibe_check"] for r in rating_list])
            danger_avg = self._calculate_average([r["danger"] for r in rating_list])
            overall = self._calculate_average(
                [comfort_avg, quietness_avg, accessibility_avg, vibe_avg, danger_avg]
            )
            avg_ratings[loc_id] = {
                "comfort": round(comfort_avg, 1),
                "quietness": round(quietness_avg, 1),
                "accessibility": round(accessibility_avg, 1),
                "vibe_check": round(vibe_avg, 1),
                "danger": round(danger_avg, 1),
                "overall": round(overall, 1),
            }
        return avg_ratings

    @rx.var
    def total_ratings_submitted(self) -> int:
        return sum((len(r) for r in self.ratings.values()))

    @rx.var
    def favorite_location(self) -> str:
        if not self.ratings:
            return "Not enough data"
        loc_counts = {loc_id: len(ratings) for loc_id, ratings in self.ratings.items()}
        if not loc_counts:
            return "Not enough data"
        most_rated_id = max(loc_counts, key=loc_counts.get)
        fav_location = next(
            (loc for loc in self.locations if loc["id"] == most_rated_id), None
        )
        return fav_location["name"] if fav_location else "Unknown"

    @rx.var
    def average_rating_given(self) -> float:
        all_user_ratings = []
        for rating_list in self.ratings.values():
            for rating in rating_list:
                all_user_ratings.extend(rating.values())
        if not all_user_ratings:
            return 0.0
        return round(sum(all_user_ratings) / len(all_user_ratings), 1)

    @rx.var
    def completion_percentage(self) -> int:
        rated_count = len(self.ratings)
        total_locations = len(self.locations)
        if total_locations == 0:
            return 0
        return int(rated_count / total_locations * 100)