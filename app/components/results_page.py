import reflex as rx
from app.states.quiz_state import QuizState
from app.states.user_state import UserState
from app.states.location_state import LocationState


def unlocked_location_tag(spot_id: str) -> rx.Component:
    # We need to find the location name from the ID
    location_name = rx.match(
        spot_id,
        ("cloud-nine-credit", "Cloud Nine Credit Charge"),
        ("the-spynap-alley", "The Spy-Nap Alley"),
        ("the-public-isolation", "The Public Isolation Island"),
        ("the-urban-zen", "The Urban Zen Bench"),
        ("the-shade-throne", "The Shade Throne"),
        ("the-stonecold-zen", "The Stone-Cold Zen Zone"),
        ("the-bobafueled-snooze", "The Boba-Fueled Snooze Booth"),
        ("the-stairwell-stealth", "The Stairwell Stealth Suite"),
        ("the-curtaincall-nap", "The Curtain-Call Nap Studio"),
        ("the-modular-dream", "The Modular Dream Fort"),
        "Unknown Location"
    )
    
    return rx.el.div(
        rx.icon("map-pin", size=12, class_name="mr-1"),
        rx.text(location_name, class_name="text-[10px] font-bold"),
        on_click=LocationState.select_location(spot_id),
        class_name="flex items-center px-2 py-1 border border-[#bd00ff] text-[#bd00ff] bg-[#bd00ff]/10 mr-2 mb-2 cursor-pointer hover:bg-[#bd00ff]/30 transition-colors"
    )


def results_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            # Header Box
            rx.el.div(
                # Top decorative squares
                rx.el.div(class_name="absolute top-0 left-0 w-2 h-2 bg-[#00ff9f]"),
                rx.el.div(class_name="absolute bottom-0 left-0 w-2 h-2 bg-[#ffd700]"),
                
                rx.el.div(
                    rx.icon(
                        QuizState.personality_details["icon"],
                        class_name="h-16 w-16 text-[#ff0055] mb-4 animate-bounce-slow",
                    ),
                    rx.text("[ CHARACTER ANALYSIS COMPLETE ]", class_name="text-xs text-gray-400 font-mono mb-2 tracking-widest"),
                    rx.el.h2(
                        QuizState.personality_details["title"],
                        class_name="text-3xl md:text-4xl text-[#00ff9f] font-bold text-shadow-neon-green mb-4 text-center tracking-wider uppercase",
                    ),
                    rx.el.div(
                        rx.el.span("■", class_name="text-[#bd00ff] text-xs mr-2"),
                        rx.text("RANK: S-TIER NAPPER", class_name="text-sm text-[#bd00ff] font-bold tracking-widest"),
                        rx.el.span("■", class_name="text-[#bd00ff] text-xs ml-2"),
                        class_name="flex items-center justify-center mb-2"
                    ),
                    class_name="flex flex-col items-center justify-center"
                ),
                class_name="w-full border-2 border-[#00ff9f] p-8 bg-[#00ff9f]/5 mb-6 relative max-w-2xl mx-auto"
            ),

            # Details Box
            rx.el.div(
                rx.el.div(
                    rx.icon("zap", size=16, class_name="text-[#ffd700] mr-2 mt-1"),
                    rx.el.div(
                        rx.text(
                            f"Class: {QuizState.personality_details['title']} | Stats: REQUIREMENTS +MAX, SATISFACTION +100 WHEN MET",
                            class_name="text-xs text-gray-300 font-mono mb-2"
                        ),
                        rx.text(
                            f"Special Ability: \"Perfect Setup\" - {QuizState.personality_details['description']}",
                            class_name="text-xs text-gray-400 font-mono mb-2 leading-relaxed"
                        ),
                        rx.text(
                            "Weakness: Everything else.",
                            class_name="text-xs text-gray-500 font-mono"
                        ),
                        class_name="flex flex-col"
                    ),
                    class_name="flex items-start mb-6"
                ),
                
                rx.el.div(
                    rx.text(">> BEST MATCH / RECOMMENDED LOCATIONS:", class_name="text-xs text-[#00ff9f] font-bold mb-3 tracking-wider"),
                    rx.el.div(
                        rx.foreach(
                            QuizState.personality_details["spots"],
                            unlocked_location_tag
                        ),
                        class_name="flex flex-wrap"
                    ),
                    class_name="border-t border-dashed border-gray-700 pt-4"
                ),
                
                class_name="w-full border border-[#bd00ff] p-6 bg-[#1a1a2e] mb-6 max-w-2xl mx-auto"
            ),

            # Action Buttons
            rx.el.div(
                rx.el.button(
                    rx.icon("map-pin", size=14, class_name="mr-2 text-black"),
                    "START QUEST",
                    on_click=lambda: QuizState.set_page("locations"),
                    class_name="flex-1 bg-[#00ff9f] text-black font-bold text-sm py-3 hover:bg-[#00ff9f]/80 transition-colors flex items-center justify-center mr-2"
                ),
                rx.el.button(
                    rx.icon("rotate-ccw", size=14, class_name="mr-2 text-[#bd00ff]"),
                    "RETRY",
                    on_click=QuizState.reset_quiz,
                    class_name="px-6 border border-[#bd00ff] text-[#bd00ff] font-bold text-sm py-3 hover:bg-[#bd00ff]/10 transition-colors flex items-center justify-center mr-2"
                ),
                rx.el.button(
                    rx.icon("home", size=14, class_name="mr-2 text-[#bd00ff]"),
                    "HOME",
                    on_click=lambda: QuizState.set_page("home"),
                    class_name="px-6 border border-[#bd00ff] text-[#bd00ff] font-bold text-sm py-3 hover:bg-[#bd00ff]/10 transition-colors flex items-center justify-center"
                ),
                class_name="flex w-full max-w-2xl mx-auto mb-8"
            ),

            # Achievement Notification
            rx.el.div(
                rx.el.div(
                    rx.text("[ ACHIEVEMENT UNLOCKED ]", class_name="text-[10px] text-[#00ff9f] font-bold mb-1 tracking-widest text-center"),
                    rx.el.div(
                        rx.icon("trophy", size=16, class_name="text-[#ffd700] mr-2"),
                        rx.text("\"First Steps\" - You've created your character!", class_name="text-xs font-bold text-[#ffd700]"),
                        rx.icon("trophy", size=16, class_name="text-[#ffd700] ml-2"),
                        class_name="flex items-center justify-center"
                    ),
                    class_name="w-full border border-[#ffd700] bg-[#ffd700]/10 p-3 mb-4 striped-bg" # striped-bg class would need css, but simple bg is fine
                ),
                
                # XP Gained
                rx.el.div(
                    rx.text("XP GAINED:", class_name="text-xs font-bold text-[#00ff9f] mr-2"),
                    rx.el.div(
                        class_name="h-2 w-32 bg-gradient-to-r from-[#00ff9f] to-[#bd00ff] mr-2"
                    ),
                    rx.text("+500", class_name="text-xs font-bold text-white"),
                    class_name="w-full border border-[#00ff9f] p-2 flex items-center justify-center bg-[#00ff9f]/5"
                ),
                
                class_name="w-full max-w-2xl mx-auto"
            ),

            class_name="flex flex-col items-center w-full"
        ),
        class_name="min-h-screen bg-[#050510] p-4 md:p-8 font-mono flex flex-col items-center justify-center animate-fade-in",
    )
