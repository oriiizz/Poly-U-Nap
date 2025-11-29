import reflex as rx
from app.states.quiz_state import QuizState


def nav_button(text: str, page: str, is_mobile: bool = False) -> rx.Component:
    return rx.el.button(
        text,
        on_click=lambda: QuizState.set_page(page),
        class_name=rx.cond(
            QuizState.current_page == page,
            "px-4 py-2 text-sm text-[#00ff9f] text-shadow-neon border-b-2 border-[#00ff9f]",
            "px-4 py-2 text-sm text-gray-400 hover:text-white transition-colors",
        ),
    )


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "bed-double",
                    class_name="h-6 w-6 md:h-8 md:w-8 text-[#00ff9f] mr-2 md:mr-4",
                ),
                rx.el.h1(
                    "Poly U Nap",
                    class_name="text-base md:text-2xl font-bold text-shadow-neon text-[#00ff9f]",
                ),
                class_name="flex items-center",
            ),
            rx.el.nav(
                nav_button("Home", "home"),
                nav_button("Quiz", "quiz"),
                nav_button("Locations", "locations"),
                nav_button("Profile", "profile"),
                class_name="hidden md:flex items-center gap-4",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon(tag="menu", class_name="h-6 w-6"),
                    on_click=QuizState.toggle_mobile_menu,
                    class_name="md:hidden p-2 text-white",
                ),
                class_name="md:hidden",
            ),
            class_name="w-full max-w-4xl flex justify-between items-center",
        ),
        rx.cond(
            QuizState.mobile_menu_open,
            rx.el.div(
                rx.el.nav(
                    nav_button("Home", "home", is_mobile=True),
                    nav_button("Quiz", "quiz", is_mobile=True),
                    nav_button("Locations", "locations", is_mobile=True),
                    nav_button("Profile", "profile", is_mobile=True),
                    class_name="flex flex-col items-start gap-4 p-4",
                ),
                class_name="md:hidden absolute top-full left-0 w-full bg-[#1a1a2e]/90 backdrop-blur-sm border-b-2 border-[#00ff9f]/20",
            ),
            None,
        ),
        class_name="w-full p-4 bg-[#1a1a2e]/50 backdrop-blur-sm border-b-2 border-[#00ff9f]/20 flex justify-center relative z-10",
    )