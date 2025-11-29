import reflex as rx
from typing import TypedDict, Literal, cast
import random


class Achievement(TypedDict):
    id: str
    title: str
    description: str
    icon: str


class UserState(rx.State):
    achievements: dict[str, Achievement] = {
        "5-star-sleeper": {
            "id": "5-star-sleeper",
            "title": "5-Star Sleeper",
            "description": "Rate a single location with a perfect 5-star score in all categories.",
            "icon": "star",
        },
        "secret-spot-explorer": {
            "id": "secret-spot-explorer",
            "title": "Secret Spot Explorer",
            "description": "Submit ratings for at least 3 different nap spots.",
            "icon": "map-pin",
        },
        "all-area-conqueror": {
            "id": "all-area-conqueror",
            "title": "All-Area Conqueror",
            "description": "Leave your mark by rating all available nap locations.",
            "icon": "crown",
        },
        "nap-legend": {
            "id": "nap-legend",
            "title": "Nap Legend",
            "description": "Complete the personality quiz and rate every single location. A true master of rest.",
            "icon": "shield-check",
        },
        "living-on-the-edge": {
            "id": "living-on-the-edge",
            "title": "Living on the Edge",
            "description": "Rate a location with maximum Danger level. You laugh in the face of peril.",
            "icon": "skull",
        },
        "zen-master": {
            "id": "zen-master",
            "title": "Zen Master",
            "description": "Find a spot with perfect Quietness. Inner peace achieved.",
            "icon": "flower",
        },
        "social-sleeper": {
            "id": "social-sleeper",
            "title": "Social Sleeper",
            "description": "Rate a spot that is loud but has immaculate vibes. Who needs quiet?",
            "icon": "users",
        },
        "night-owl": {
            "id": "night-owl",
            "title": "The Night Owl",
            "description": "Access the app during the witching hours (Late Night).",
            "icon": "moon",
        },
        "secret-boss-defeated": {
            "id": "secret-boss-defeated",
            "title": "Secret Boss Defeated",
            "description": "Discover the hidden nap spot. You found the easter egg.",
            "icon": "ghost",
        },
        "library-legend": {
            "id": "library-legend",
            "title": "Library Legend",
            "description": "Check in at all library locations (G floor study room, bookshelf corridor, and sofa).",
            "icon": "book-open",
        },
        "outdoor-enthusiast": {
            "id": "outdoor-enthusiast",
            "title": "Outdoor Enthusiast",
            "description": "Check in at all outdoor seating areas (wooden, dining, and stone chairs).",
            "icon": "sun",
        },
        "jcit-master": {
            "id": "jcit-master",
            "title": "JCIT Master",
            "description": "Check in at all JCIT locations (Milk Tea Shop, Stairwell, Study Room areas).",
            "icon": "building",
        },
        "comfort-seeker": {
            "id": "comfort-seeker",
            "title": "Comfort Seeker",
            "description": "Check in at all LEGENDARY rarity locations.",
            "icon": "sofa",
        },
        "speed-napper": {
            "id": "speed-napper",
            "title": "Speed Napper",
            "description": "Complete a quiz in under 2 minutes.",
            "icon": "zap",
        },
    }
    unlocked_achievements: set[str] = set()
    gamertag: str = ""
    xp: int = 0
    titles: list[str] = ["Sleepy Newbie"]  # Unlocked titles
    current_title: str = "Sleepy Newbie"  # Currently equipped title

    @rx.var
    def level(self) -> int:
        return (self.xp // 500) + 1

    @rx.var
    def xp_to_next_level(self) -> int:
        return 500 - (self.xp % 500)

    @rx.var
    def xp_progress(self) -> int:
        return int(((self.xp % 500) / 500) * 100)
    
    @rx.var
    def level_title(self) -> str:
        """Return title based on current level"""
        if self.level >= 20:
            return "NAP DEITY"
        elif self.level >= 15:
            return "SLEEP LEGEND"
        elif self.level >= 10:
            return "DREAM MASTER"
        elif self.level >= 7:
            return "REST WARRIOR"
        elif self.level >= 5:
            return "DOZE EXPERT"
        elif self.level >= 3:
            return "SNOOZE SCOUT"
        else:
            return "SLEEPY NEWBIE"

    @rx.event
    async def add_xp(self, amount: int, reason: str = ""):
        """Add XP and check for level up"""
        old_level = self.level
        self.xp += amount
        new_level = self.level
        
        # Show XP gain notification
        if reason:
            yield rx.toast.info(
                f"+{amount} XP - {reason}",
                duration=3000,
                position="bottom-right"
            )
        
        # Check if leveled up
        if new_level > old_level:
            yield self.level_up_notification(new_level)
    
    @rx.event
    def level_up_notification(self, new_level: int):
        """Show special level up notification"""
        title = self.level_title
        
        # Unlock new title
        if title not in self.titles:
            self.titles.append(title)
        
        return rx.toast.success(
            f"🎉 LEVEL UP! 🎉\nYou are now Level {new_level}: {title}\n+50 BONUS XP!",
            duration=5000,
            position="top-center"
        )

    @rx.event
    def set_gamertag(self, gamertag: str):
        self.gamertag = gamertag

    @rx.event
    def save_gamertag(self):
        return rx.toast(f"Gamertag saved: {self.gamertag}", duration=3000)

    quotes: list[str] = [
        "To sleep, perchance to dream... ay, there's the rub... for in that sleep of death what dreams may come? Or, y'know, just drool on your textbook.",
        "The best bridge between despair and hope is a good night's sleep. Or a really, really good nap in the library.",
        "I think, therefore I am... tired.",
        "I have a dream... that one day I will get 8 full hours of sleep.",
        "Is it a crime to be this tired? Asking for a friend.",
        "My bed is a magical place where I suddenly remember everything I was supposed to do.",
        "They say 'go big or go home' as if going home to nap isn't a big win.",
        "I'm not a morning person or a night owl. I'm some form of permanently exhausted pigeon.",
        "If you love someone, let them sleep.",
        "Sleep is the best meditation. Also, it's a great way to avoid responsibilities.",
        "I've reached that age where my train of thought often leaves the station without me.",
        "Why fall in love when you can fall asleep?",
        "The only thing getting lit this weekend are my scented candles for a pre-nap vibe.",
        "A day without a nap is like... just kidding, I have no idea.",
        "I'm not lazy, I'm on energy-saving mode.",
        "Reality is a construct, and I'm constructing a nap.",
    ]

    @rx.event
    async def unlock_achievement(self, achievement_id: str):
        if achievement_id not in self.unlocked_achievements:
            self.unlocked_achievements.add(achievement_id)
            achievement = self.achievements[achievement_id]
            
            # Give XP for achievement
            old_level = self.level
            self.xp += 200
            new_level = self.level
            
            # Check for level up
            if new_level > old_level:
                yield self.level_up_notification(new_level)
            
            yield rx.toast.warning(
                rx.el.div(
                    rx.icon(achievement["icon"], class_name="mr-2"),
                    f"🏆 Achievement Unlocked: {achievement['title']} (+200 XP)",
                    class_name="flex items-center",
                ),
                duration=5000,
                position="top-center"
            )

    @rx.var
    def random_quote(self) -> str:
        return random.choice(self.quotes)

    @rx.var
    def total_achievements_count(self) -> int:
        return len(self.achievements)

    @rx.var
    def unlocked_achievements_count(self) -> int:
        return len(self.unlocked_achievements)

    @rx.var
    def completion_percentage(self) -> int:
        if not self.achievements:
            return 0
        return int((len(self.unlocked_achievements) / len(self.achievements)) * 100)

    @rx.var
    def remaining_achievements_count(self) -> int:
        return len(self.achievements) - len(self.unlocked_achievements)

    @rx.var
    def unlocked_achievements_list(self) -> list[Achievement]:
        return [self.achievements[id] for id in self.unlocked_achievements]