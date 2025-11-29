import reflex as rx
from app.states.quiz_state import QuizState
from app.states.location_state import LocationState
from app.states.user_state import UserState


def profile_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            # Header
            rx.el.div(
                rx.el.div(
                    rx.el.button(
                        rx.icon("arrow-left", size=16),
                        on_click=lambda: QuizState.set_page("home"),
                        class_name="p-1 border border-[#00ff9f] text-[#00ff9f] hover:bg-[#00ff9f] hover:text-black transition-colors mr-4",
                    ),
                    rx.el.div(
                        rx.el.h1("PLAYER STATS", class_name="text-xl font-bold text-[#00ff9f] tracking-widest text-shadow-neon-green"),
                        rx.el.p("Your napping career overview", class_name="text-xs text-gray-400 font-mono"),
                        class_name="flex flex-col"
                    ),
                    class_name="flex items-center"
                ),
                rx.icon("user", class_name="text-[#bd00ff] w-6 h-6"),
                class_name="w-full border-2 border-[#00ff9f] p-4 flex justify-between items-center bg-[#00ff9f]/5 mb-6"
            ),

            # Gamertag Input
            rx.el.div(
                rx.el.div(
                    rx.text("LEVEL", class_name="text-[10px] text-gray-500 tracking-widest mb-1"),
                    rx.el.div(
                        rx.text(UserState.level, class_name="text-2xl font-bold text-[#ffd700] mr-2"),
                        rx.text(UserState.level_title, class_name="text-xs text-[#00ff9f] font-bold tracking-wider"),
                        class_name="flex items-center mb-3"
                    ),
                    class_name="mb-3"
                ),
                rx.el.input(
                    placeholder="Enter your gamertag",
                    value=UserState.gamertag,
                    on_change=UserState.set_gamertag,
                    class_name="w-full bg-transparent border border-[#00ff9f] text-[#00ff9f] p-2 text-sm font-mono focus:outline-none focus:bg-[#00ff9f]/10 mb-2 placeholder-gray-600"
                ),
                rx.el.button(
                    "SAVE",
                    on_click=UserState.save_gamertag,
                    class_name="bg-[#00ff9f] text-black font-bold text-xs px-4 py-1 hover:bg-[#00ff9f]/80 transition-colors"
                ),
                class_name="w-full border border-[#bd00ff] p-4 bg-[#bd00ff]/5 mb-6"
            ),

            # EXP Bar
            rx.el.div(
                rx.el.div(
                    rx.text("EXP TO NEXT LEVEL", class_name="text-xs font-bold text-gray-400 tracking-wider"),
                    rx.text("500 XP", class_name="text-xs font-bold text-[#00ff9f]"),
                    class_name="flex justify-between mb-2"
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="h-full bg-[#00ff9f] transition-all duration-500",
                        style={"width": f"{UserState.xp_progress}%"}
                    ),
                    class_name="w-full h-2 border border-[#00ff9f] bg-[#00ff9f]/10 p-0.5"
                ),
                class_name="w-full border border-[#00ff9f] p-4 bg-[#00ff9f]/5 mb-6"
            ),

            # Stats Grid
            rx.el.div(
                # Total Missions (clickable)
                rx.el.button(
                    rx.el.div(
                        rx.el.div(
                            rx.icon("map-pin", size=14, class_name="mr-2 text-gray-400"),
                            rx.text("MISSIONS", class_name="text-xs font-bold text-gray-300 tracking-wider"),
                            class_name="flex items-center mb-3"
                        ),
                        rx.text(LocationState.missions_count, class_name="text-3xl font-bold text-[#00ff9f] mb-2"),
                        rx.text("View history", class_name="text-[10px] text-gray-500 font-mono hover:text-[#00ff9f] transition-colors"),
                        class_name="flex flex-col"
                    ),
                    on_click=lambda: QuizState.set_page("locations"),
                    class_name="p-4 border border-[#00ff9f] bg-[#00ff9f]/5 hover:bg-[#00ff9f]/10 transition-colors cursor-pointer w-full text-left"
                ),
                # Locations (clickable)
                rx.el.button(
                    rx.el.div(
                        rx.el.div(
                            rx.icon("map", size=14, class_name="mr-2 text-gray-400"),
                            rx.text("CHECKED IN", class_name="text-xs font-bold text-gray-300 tracking-wider"),
                            class_name="flex items-center mb-3"
                        ),
                        rx.text(LocationState.explored_count, class_name="text-3xl font-bold text-[#bd00ff] mb-2"),
                        rx.text("View history", class_name="text-[10px] text-gray-500 font-mono hover:text-[#bd00ff] transition-colors"),
                        class_name="flex flex-col"
                    ),
                    on_click=lambda: QuizState.set_page("visited_locations"),
                    class_name="p-4 border border-[#bd00ff] bg-[#bd00ff]/5 hover:bg-[#bd00ff]/10 transition-colors cursor-pointer w-full text-left"
                ),
                # S-Ranks
                rx.el.div(
                    rx.el.div(
                        rx.icon("star", size=14, class_name="mr-2 text-gray-400"),
                        rx.text("S-RANKS", class_name="text-xs font-bold text-gray-300 tracking-wider"),
                        class_name="flex items-center mb-3"
                    ),
                    rx.text(LocationState.s_rank_count, class_name="text-3xl font-bold text-[#ffd700] mb-2"),
                    rx.text(
                        rx.cond(
                            LocationState.missions_count > 0,
                            f"{(LocationState.s_rank_count / LocationState.missions_count * 100):.0f}% perfect rate",
                            "0% perfect rate"
                        ),
                        class_name="text-[10px] text-gray-500 font-mono"
                    ),
                    class_name="p-4 border border-[#ffd700] bg-[#ffd700]/5 flex flex-col"
                ),
                # Achievements (clickable)
                rx.el.button(
                    rx.el.div(
                        rx.el.div(
                            rx.icon("trophy", size=14, class_name="mr-2 text-gray-400"),
                            rx.text("ACHIEVEMENTS", class_name="text-xs font-bold text-gray-300 tracking-wider"),
                            class_name="flex items-center mb-3"
                        ),
                        rx.text(UserState.unlocked_achievements_count, class_name="text-3xl font-bold text-[#ff00ff] mb-2"),
                        rx.text(f"{UserState.unlocked_achievements_count}/{UserState.total_achievements_count} unlocked", class_name="text-[10px] text-gray-500 font-mono hover:text-[#ff00ff] transition-colors"),
                        class_name="flex flex-col"
                    ),
                    on_click=lambda: QuizState.set_page("achievements"),
                    class_name="p-4 border border-[#ff00ff] bg-[#ff00ff]/5 hover:bg-[#ff00ff]/10 transition-colors cursor-pointer w-full text-left"
                ),
                class_name="grid grid-cols-2 gap-4 w-full mb-6"
            ),

            # No Data Found
            rx.cond(
                LocationState.total_ratings_submitted == 0,
                rx.el.div(
                    rx.el.div(
                        rx.icon("triangle-alert", size=16, class_name="text-[#ffd700] mr-2"),
                        rx.text("NO DATA FOUND", class_name="text-sm font-bold text-[#ff00ff] tracking-wider"),
                        rx.icon("triangle-alert", size=16, class_name="text-[#ffd700] ml-2"),
                        class_name="flex items-center justify-center mb-2"
                    ),
                    rx.text(
                        "Complete the quiz and start rating locations to unlock stats!",
                        class_name="text-xs text-gray-400 text-center font-mono max-w-xs"
                    ),
                    class_name="w-full border border-[#ff00ff] p-6 bg-[#ff00ff]/5 flex flex-col items-center justify-center mb-6"
                )
            ),

            # Footer
            rx.el.div(
                rx.text("💾 GAME SAVED AUTOMATICALLY | PRESS START TO CONTINUE 💾", class_name="text-[10px] text-gray-400 tracking-widest"),
                class_name="w-full border border-[#bd00ff] p-3 text-center bg-[#bd00ff]/5"
            ),

            class_name="max-w-2xl mx-auto w-full"
        ),
        class_name="min-h-screen bg-[#050510] p-4 md:p-8 font-mono"
    )
