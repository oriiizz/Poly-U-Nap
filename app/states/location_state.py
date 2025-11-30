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
    location: str
    name: str
    description: str
    icon: str
    model_id: str
    rarity: str
    is_secret: bool
    sample_rating: Rating


class LocationState(rx.State):
    checked_in_locations: set[str] = set()
    
    locations: list[Location] = [
        {
            "id": "cloud-nine-credit",
            "location": "Study room on the G floor of the library",
            "name": "Cloud Nine Credit Charge",
            "description": "Your demand for comfort rivals that of a five-star hotel sleep tester. Here, the sofa is a cloud, the power outlet is a magical spring. With stable Wi-Fi, you might even dream of being rewarded with credit hours.",
            "icon": "sofa",
            "model_id": "b67d3200015b48db9546fc8e2afd6168",
            "rarity": "LEGENDARY",
            "is_secret": False,
            "sample_rating": {"comfort": 5, "quietness": 5, "accessibility": 3, "vibe_check": 3, "danger": 1}
        },
        {
            "id": "the-spynap-alley",
            "location": "The corridor of bookshelves on the G floor of the library",
            "name": "The Spy-Nap Alley",
            "description": "Your sleep here is like a footnote in a thesis—precise, brief, yet indispensable. Each time you close your eyes, it's like activating 'Deep Recovery Mode,' restoring 80% energy in 5 minutes. But, sleeping here... is this bookshelf about to fall over...?",
            "icon": "zap",
            "model_id": "d682b1a9ea2f4683914f9e6384dcb845",
            "rarity": "EPIC",
            "is_secret": False,
            "sample_rating": {"comfort": 4, "quietness": 3, "accessibility": 4, "vibe_check": 3, "danger": 1}
        },
        {
            "id": "the-public-isolation",
            "location": "Sofa on the G floor of the library",
            "name": "The Public Isolation Island",
            "description": "This isn't a sofa; it's your 'Ergonomic Island.' People passing by? They're just the sightseers in your dream's bullet comments. You recharge your energy and your inspiration—waking up fully charged, with inspiration unlocked in a new skin.",
            "icon": "sofa",
            "model_id": "5d549bf015bf49f8add67eb74e86ad26",
            "rarity": "LEGENDARY",
            "is_secret": False,
            "sample_rating": {"comfort": 4, "quietness": 4, "accessibility": 5, "vibe_check": 3, "danger": 1}
        },
        {
            "id": "the-urban-zen",
            "location": "Outdoor wooden chair",
            "name": "The Urban Zen Bench",
            "description": "You sleep on the city's pulse. The subway vibrations are white noise, the passing shadows are your dynamic screensaver. You're not napping outdoors; you're starring in a live performance of 'Urban Sleep Log.'",
            "icon": "compass",
            "model_id": "932a64b422a94be9bec6899d36c6f6ea",
            "rarity": "UNCOMMON",
            "is_secret": False,
            "sample_rating": {"comfort": 2, "quietness": 2, "accessibility": 4, "vibe_check": 3, "danger": 1}
        },
        {
            "id": "the-shade-throne",
            "location": "Outdoor dining chair",
            "name": "The Shade Throne",
            "description": "Under the sunshade umbrella, you are your own shopkeeper. Occasionally someone studying? They're just extras in your dream~",
            "icon": "compass",
            "model_id": "0201608218144d65892e4f63647774d0",
            "rarity": "UNCOMMON",
            "is_secret": False,
            "sample_rating": {"comfort": 3, "quietness": 3, "accessibility": 5, "vibe_check": 3, "danger": 1}
        },
        {
            "id": "the-stonecold-zen",
            "location": "Outdoor stone chair",
            "name": "The Stone-Cold Zen Zone",
            "description": "A four-person stone bench, you occupy one corner, the greenery is your screen. An occasional passerby? They're just forest spirits in your dream~",
            "icon": "compass",
            "model_id": "d33020d326bb4e6bbcf6043f6f5dfb1b",
            "rarity": "UNCOMMON",
            "is_secret": False,
            "sample_rating": {"comfort": 1, "quietness": 1, "accessibility": 4, "vibe_check": 3, "danger": 1}
        },
        {
            "id": "the-bobafueled-snooze",
            "location": "JCIT Milk Tea Shop",
            "name": "The Boba-Fueled Snooze Booth",
            "description": "Fall asleep to the scent of milk tea, wake up at the round table. I will strategically choose the 'off-peak hours'!",
            "icon": "bed-double",
            "model_id": "6c59d214f3224a6b9fa9f135937ff3ff",
            "rarity": "RARE",
            "is_secret": False,
            "sample_rating": {"comfort": 3, "quietness": 2, "accessibility": 3, "vibe_check": 3, "danger": 1}
        },
        {
            "id": "the-stairwell-stealth",
            "location": "JCIT Stairwell",
            "name": "The Stairwell Stealth Suite",
            "description": "The stench is your barrier, the emptiness is your dojo. No people, right? That's called 'Stealth Skill Activated'!",
            "icon": "zap",
            "model_id": "f0ca0a25820646bf9575d7e075aefae2",
            "rarity": "EPIC",
            "is_secret": False,
            "sample_rating": {"comfort": 1, "quietness": 1, "accessibility": 2, "vibe_check": 3, "danger": 1}
        },
        {
            "id": "the-curtaincall-nap",
            "location": "JCIT Study Room Partition Area",
            "name": "The Curtain-Call Nap Studio",
            "description": "Curtain drawn, reclining on the small chair, game console on standby~ The people around are just the audience of your sleep livestream!",
            "icon": "sofa",
            "model_id": "b1c28102ab3a4a7193e7b89a2130a19f",
            "rarity": "LEGENDARY",
            "is_secret": False,
            "sample_rating": {"comfort": 3, "quietness": 3, "accessibility": 4, "vibe_check": 3, "danger": 1}
        },
        {
            "id": "the-modular-dream",
            "location": "JCIT Study Room Sofa",
            "name": "The Modular Dream Fort",
            "description": "Modular sofas for you to arrange, the view outside for you to enjoy~ Just love the 'shared sleep experience'!",
            "icon": "sofa",
            "model_id": "85aa52c8637b42d18d7fb082bd11d265",
            "rarity": "LEGENDARY",
            "is_secret": False,
            "sample_rating": {"comfort": 4, "quietness": 5, "accessibility": 5, "vibe_check": 3, "danger": 1}
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

    is_hovering_location_title: bool = False

    @rx.event
    def set_hovering_location_title(self, hover: bool):
        self.is_hovering_location_title = hover

    @rx.var
    def selected_location_map_image(self) -> str:
        if not self.selected_location_id:
            return ""
        
        # Hardcoded mapping to avoid circular imports with MapState
        # Library G
        if self.selected_location_id in ["cloud-nine-credit", "the-spynap-alley", "the-public-isolation"]:
            return "/map images/Pao Yue-kong Library G Floor.png"
        # JCIT P
        elif self.selected_location_id in ["the-bobafueled-snooze"]:
            return "/map images/Jockey Club Innovation Tower P.png"
        # JCIT 11
        elif self.selected_location_id in ["the-stairwell-stealth", "the-curtaincall-nap", "the-modular-dream"]:
            return "/map images/Jockey Club Innovation Tower 11F.png"
        # Outdoor
        elif self.selected_location_id in ["the-urban-zen", "the-shade-throne", "the-stonecold-zen"]:
            return "/map images/POLYU MAP.png"
        
        return ""

    @rx.var
    def selected_location_coords(self) -> dict[str, str]:
        if not self.selected_location_id:
            return {"x": "0%", "y": "0%"}
            
        # Hardcoded coordinates matching interactive_map.py
        coords = {
            "cloud-nine-credit": {"x": "30%", "y": "9%"},
            "the-spynap-alley": {"x": "7%", "y": "9%"},
            "the-public-isolation": {"x": "43%", "y": "65%"},
            "the-urban-zen": {"x": "60%", "y": "59%"},
            "the-shade-throne": {"x": "58%", "y": "51%"},
            "the-stonecold-zen": {"x": "57%", "y": "62%"},
            "the-bobafueled-snooze": {"x": "72%", "y": "28%"},
            "the-stairwell-stealth": {"x": "48%", "y": "35%"},
            "the-curtaincall-nap": {"x": "60%", "y": "45%"},
            "the-modular-dream": {"x": "53%", "y": "60%"},
        }
        return coords.get(self.selected_location_id, {"x": "50%", "y": "50%"})

    @rx.event
    async def check_in_location(self, location_id: str):
        from app.states.user_state import UserState
        
        if location_id not in self.checked_in_locations:
            self.checked_in_locations.add(location_id)
            user_state = await self.get_state(UserState)
            
            # Find location details
            location = next((loc for loc in self.locations if loc["id"] == location_id), None)
            
            if location:
                # XP based on rarity
                xp_gain = {
                    "LEGENDARY": 150,
                    "EPIC": 100,
                    "RARE": 75,
                    "UNCOMMON": 50,
                }.get(location["rarity"], 50)
                
                # Add XP directly
                old_level = user_state.level
                user_state.xp += xp_gain
                new_level = user_state.level
                
                # Check for level up
                if new_level > old_level:
                    yield user_state.level_up_notification(new_level)
                
                yield rx.toast.success(
                    f"✅ CHECK-IN COMPLETE\n{location['name']}\n+{xp_gain} XP",
                    duration=4000,
                    position="bottom-right"
                )
                
                if location["is_secret"]:
                    yield user_state.unlock_achievement("secret-spot-explorer")
                    yield user_state.unlock_achievement("secret-boss-defeated")
                
                # Check for location collection achievements
                checked_in_list = list(self.checked_in_locations)
                
                # Library Legend - all library locations
                library_locs = ["cloud-nine-credit", "the-spynap-alley", "the-public-isolation"]
                if all(loc in checked_in_list for loc in library_locs):
                    yield user_state.unlock_achievement("library-legend")
                
                # Outdoor Enthusiast - all outdoor locations
                outdoor_locs = ["the-urban-zen", "the-shade-throne", "the-stonecold-zen"]
                if all(loc in checked_in_list for loc in outdoor_locs):
                    yield user_state.unlock_achievement("outdoor-enthusiast")
                
                # JCIT Master - all JCIT locations
                jcit_locs = ["the-bobafueled-snooze", "the-stairwell-stealth", "the-curtaincall-nap", "the-modular-dream"]
                if all(loc in checked_in_list for loc in jcit_locs):
                    yield user_state.unlock_achievement("jcit-master")
                
                # Comfort Seeker - all LEGENDARY locations
                legendary_locs = [loc["id"] for loc in self.locations if loc["rarity"] == "LEGENDARY"]
                if all(loc in checked_in_list for loc in legendary_locs):
                    yield user_state.unlock_achievement("comfort-seeker")

    @rx.var
    def missions_count(self) -> int:
        return len(self.ratings)

    @rx.var
    def explored_count(self) -> int:
        return len(self.checked_in_locations)

    @rx.var
    def s_rank_count(self) -> int:
        count = 0
        for ratings in self.ratings.values():
            for r in ratings:
                if all(v == 5 for v in r.values()):
                    count += 1
        return count

    @rx.var
    def secrets_found_count(self) -> int:
        count = 0
        for loc_id in self.checked_in_locations:
            loc = next((l for l in self.locations if l["id"] == loc_id), None)
            if loc and loc["is_secret"]:
                count += 1
        return count

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
            
            user_state = await self.get_state(UserState)
            
            # First time rating this location bonus
            is_first_rating = len(self.ratings[self.selected_location_id]) == 0
            
            self.ratings[self.selected_location_id].append(self.new_rating.copy())
            
            # Calculate XP based on rating
            avg = sum(self.new_rating.values()) / len(self.new_rating)
            stars = int(avg)
            
            # Base XP for rating
            base_xp = 30
            # Bonus for first rating
            first_rating_bonus = 70 if is_first_rating else 0
            # Bonus for thoroughness (max ratings)
            thoroughness_bonus = 20 if all(v == 5 for v in self.new_rating.values()) else 0
            
            total_xp = base_xp + first_rating_bonus + thoroughness_bonus
            
            location_name = next(
                (loc["name"] for loc in self.locations if loc["id"] == self.selected_location_id),
                "Location"
            )
            
            # Add XP directly
            old_level = user_state.level
            user_state.xp += total_xp
            new_level = user_state.level
            
            # Check for level up
            if new_level > old_level:
                yield user_state.level_up_notification(new_level)
            
            # Achievement checks
            if all((v == 5 for v in self.new_rating.values())):
                old_level_check = user_state.level
                user_state.xp += 200
                if user_state.level > old_level_check:
                    yield user_state.level_up_notification(user_state.level)
                if "5-star-sleeper" not in user_state.unlocked_achievements:
                    user_state.unlocked_achievements.add("5-star-sleeper")
                    achievement = user_state.achievements["5-star-sleeper"]
                    yield rx.toast.warning(
                        rx.el.div(
                            rx.icon(achievement["icon"], class_name="mr-2"),
                            f"🏆 Achievement Unlocked: {achievement['title']} (+200 XP)",
                            class_name="flex items-center",
                        ),
                        duration=5000,
                        position="top-center"
                    )
            
            # New Achievements Logic
            if self.new_rating["danger"] == 5:
                if "living-on-the-edge" not in user_state.unlocked_achievements:
                    old_level_check = user_state.level
                    user_state.xp += 200
                    if user_state.level > old_level_check:
                        yield user_state.level_up_notification(user_state.level)
                    user_state.unlocked_achievements.add("living-on-the-edge")
                    achievement = user_state.achievements["living-on-the-edge"]
                    yield rx.toast.warning(
                        rx.el.div(
                            rx.icon(achievement["icon"], class_name="mr-2"),
                            f"🏆 Achievement Unlocked: {achievement['title']} (+200 XP)",
                            class_name="flex items-center",
                        ),
                        duration=5000,
                        position="top-center"
                    )
            
            if self.new_rating["quietness"] == 5:
                if "zen-master" not in user_state.unlocked_achievements:
                    old_level_check = user_state.level
                    user_state.xp += 200
                    if user_state.level > old_level_check:
                        yield user_state.level_up_notification(user_state.level)
                    user_state.unlocked_achievements.add("zen-master")
                    achievement = user_state.achievements["zen-master"]
                    yield rx.toast.warning(
                        rx.el.div(
                            rx.icon(achievement["icon"], class_name="mr-2"),
                            f"🏆 Achievement Unlocked: {achievement['title']} (+200 XP)",
                            class_name="flex items-center",
                        ),
                        duration=5000,
                        position="top-center"
                    )
            
            if self.new_rating["quietness"] == 1 and self.new_rating["vibe_check"] == 5:
                if "social-sleeper" not in user_state.unlocked_achievements:
                    old_level_check = user_state.level
                    user_state.xp += 200
                    if user_state.level > old_level_check:
                        yield user_state.level_up_notification(user_state.level)
                    user_state.unlocked_achievements.add("social-sleeper")
                    achievement = user_state.achievements["social-sleeper"]
                    yield rx.toast.warning(
                        rx.el.div(
                            rx.icon(achievement["icon"], class_name="mr-2"),
                            f"🏆 Achievement Unlocked: {achievement['title']} (+200 XP)",
                            class_name="flex items-center",
                        ),
                        duration=5000,
                        position="top-center"
                    )

            if len(self.ratings) >= 3:
                if "secret-spot-explorer" not in user_state.unlocked_achievements:
                    old_level_check = user_state.level
                    user_state.xp += 200
                    if user_state.level > old_level_check:
                        yield user_state.level_up_notification(user_state.level)
                    user_state.unlocked_achievements.add("secret-spot-explorer")
                    achievement = user_state.achievements["secret-spot-explorer"]
                    yield rx.toast.warning(
                        rx.el.div(
                            rx.icon(achievement["icon"], class_name="mr-2"),
                            f"🏆 Achievement Unlocked: {achievement['title']} (+200 XP)",
                            class_name="flex items-center",
                        ),
                        duration=5000,
                        position="top-center"
                    )
            
            if len(self.ratings) == len(self.locations):
                quiz_state = await self.get_state(QuizState)
                if "all-area-conqueror" not in user_state.unlocked_achievements:
                    old_level_check = user_state.level
                    user_state.xp += 200
                    if user_state.level > old_level_check:
                        yield user_state.level_up_notification(user_state.level)
                    user_state.unlocked_achievements.add("all-area-conqueror")
                    achievement = user_state.achievements["all-area-conqueror"]
                    yield rx.toast.warning(
                        rx.el.div(
                            rx.icon(achievement["icon"], class_name="mr-2"),
                            f"🏆 Achievement Unlocked: {achievement['title']} (+200 XP)",
                            class_name="flex items-center",
                        ),
                        duration=5000,
                        position="top-center"
                    )
                
                if quiz_state.quiz_finished and "nap-legend" not in user_state.unlocked_achievements:
                    old_level_check = user_state.level
                    user_state.xp += 200
                    if user_state.level > old_level_check:
                        yield user_state.level_up_notification(user_state.level)
                    user_state.unlocked_achievements.add("nap-legend")
                    achievement = user_state.achievements["nap-legend"]
                    yield rx.toast.warning(
                        rx.el.div(
                            rx.icon(achievement["icon"], class_name="mr-2"),
                            f"🏆 Achievement Unlocked: {achievement['title']} (+200 XP)",
                            class_name="flex items-center",
                        ),
                        duration=5000,
                        position="top-center"
                    )
            
            # Show mission complete notification
            stars_display = "⭐" * stars
            yield rx.toast.success(
                f"🎯 MISSION COMPLETE\n{location_name}\nRating: {stars_display} ({avg:.1f}/5)\n+{total_xp} XP",
                duration=4000,
                position="bottom-right"
            )
            
            self.new_rating = {
                "comfort": 3,
                "quietness": 3,
                "accessibility": 3,
                "vibe_check": 3,
                "danger": 3,
            }
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
        
        # Process all locations, including those without user ratings
        for location in self.locations:
            loc_id = location["id"]
            rating_list = self.ratings.get(loc_id, [])
            
            if not rating_list:
                # Use sample rating when no user ratings exist
                sample = location["sample_rating"]
                avg_ratings[loc_id] = {
                    "comfort": float(sample["comfort"]),
                    "quietness": float(sample["quietness"]),
                    "accessibility": float(sample["accessibility"]),
                    "vibe_check": float(sample["vibe_check"]),
                    "danger": float(sample["danger"]),
                    "overall": round(sum(sample.values()) / len(sample), 1),
                }
                continue
            
            # Calculate averages from user ratings
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