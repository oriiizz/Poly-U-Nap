import reflex as rx
from app.states.quiz_state import QuizState
from app.states.user_state import UserState


def home_page() -> rx.Component:
    return rx.el.div(
        # --- HEADER BOX ---
        rx.el.div(
            rx.el.div(
                rx.icon("moon", class_name="text-[#00ff9f] w-8 h-8"),
                rx.icon("zap", class_name="text-[#ff00ff] w-8 h-8"),
                class_name="flex justify-center gap-4 mb-4",
            ),
            rx.el.h1(
                "POLY U NAP",
                class_name="text-4xl md:text-6xl text-[#00ff9f] text-center font-bold mb-4 text-shadow-neon leading-tight",
            ),
            rx.el.p(
                ">> THE ULTIMATE NAP QUEST v1.0 <<",
                class_name="text-[#a855f7] text-center text-sm md:text-base font-bold mb-2 tracking-wider",
            ),
            rx.el.p(
                "[Gamifying consciousness since 2025]",
                class_name="text-gray-500 text-center text-xs md:text-sm mb-8 font-mono",
            ),
            rx.el.button(
                "▶ PRESS START ◀",
                on_click=lambda: QuizState.set_page("quiz"),
                class_name="text-[#00ff9f] hover:text-white hover:bg-[#00ff9f]/20 transition-colors duration-300 text-sm md:text-base font-bold py-2 px-4 animate-pulse",
            ),
            class_name="w-full p-8 md:p-12 pixel-border bg-[#0a0a0f] flex flex-col items-center justify-center mb-6 relative overflow-hidden",
        ),
        
        # --- WARNING BOX ---
        rx.el.div(
            rx.icon("triangle-alert", class_name="text-[#a855f7] w-5 h-5 mr-3 flex-shrink-0"),
            rx.el.p(
                "WARNING: Nap levels critically low. Seek immediate horizontal rest.",
                class_name="text-gray-300 text-xs md:text-sm font-mono",
            ),
            class_name="w-full p-3 pixel-border-magenta bg-[#0a0a0f]/50 flex items-center justify-center mb-6",
        ),

        # --- MAIN GRID ---
        rx.el.div(
            # START QUIZ
            rx.el.div(
                rx.icon("moon", class_name="text-[#00ff9f] w-8 h-8 mb-4"),
                rx.el.h3(
                    "[START QUIZ]",
                    class_name="text-[#00ff9f] text-lg font-bold mb-2",
                ),
                rx.el.p(
                    "Find your sleep type & unlock nap zones",
                    class_name="text-gray-400 text-xs text-center mb-6 h-10",
                ),
                rx.el.button(
                    "▶ BEGIN",
                    on_click=lambda: QuizState.set_page("quiz"),
                    class_name="text-[#ff00ff] hover:text-white font-bold text-sm flex items-center gap-2",
                ),
                class_name="pixel-border p-6 flex flex-col items-center justify-center bg-[#0a0a0f] hover:bg-[#00ff9f]/5 transition-colors cursor-pointer",
                on_click=lambda: QuizState.set_page("quiz"),
            ),
            # EXPLORE MAP
            rx.el.div(
                rx.icon("map-pin", class_name="text-[#00d4ff] w-8 h-8 mb-4"),
                rx.el.h3(
                    "[EXPLORE MAP]",
                    class_name="text-[#00d4ff] text-lg font-bold mb-2",
                ),
                rx.el.p(
                    "Rate nap spots & earn XP",
                    class_name="text-gray-400 text-xs text-center mb-6 h-10",
                ),
                rx.el.button(
                    "▶ EXPLORE",
                    on_click=lambda: QuizState.set_page("locations"),
                    class_name="text-[#00ff9f] hover:text-white font-bold text-sm flex items-center gap-2",
                ),
                class_name="pixel-border-cyan p-6 flex flex-col items-center justify-center bg-[#0a0a0f] hover:bg-[#00d4ff]/5 transition-colors cursor-pointer",
                on_click=lambda: QuizState.set_page("locations"),
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-6 w-full mb-6",
        ),

        # --- BUTTONS ROW ---
        rx.el.div(
            rx.el.button(
                rx.el.span("🏆 ACHIEVEMENTS"),
                on_click=lambda: QuizState.set_page("achievements"), 
                class_name="pixel-border-yellow text-[#ffd700] bg-[#0a0a0f] px-6 py-3 text-sm font-bold hover:bg-[#ffd700]/10 transition-colors w-full md:w-auto text-center",
            ),
            rx.el.button(
                rx.el.span("👤 PROFILE"),
                on_click=lambda: QuizState.set_page("profile"),
                class_name="pixel-border-magenta text-[#ff00ff] bg-[#0a0a0f] px-6 py-3 text-sm font-bold hover:bg-[#ff00ff]/10 transition-colors w-full md:w-auto text-center",
            ),
            class_name="flex flex-col md:flex-row gap-4 justify-center w-full mb-8",
        ),

        # --- PRO TIP FOOTER ---
        rx.el.div(
            rx.el.p(
                "[!] PRO TIP: Scan QR codes IRL to speedrun location ratings + unlock secret boss achievements!",
                class_name="text-[#ff00ff] text-xs md:text-sm text-center font-bold",
            ),
            class_name="w-full p-4 border-2 border-[#ff00ff] border-dashed bg-[#ff00ff]/5 mb-8",
        ),

        # --- COPYRIGHT ---
        rx.el.p(
            "© 2025 NAP QUEST LABS | INSERT COIN TO CONTINUE",
            class_name="text-gray-600 text-[10px] text-center font-mono",
        ),

        class_name="w-full max-w-3xl mx-auto flex flex-col animate-fade-in",
    )