import reflex as rx
from app.states.quiz_state import QuizState
from app.components.header import header
from app.components.home_page import home_page
from app.components.quiz_page import quiz_page
from app.components.results_page import results_page
from app.components.locations_page import locations_page
from app.components.location_detail_page import location_detail_page
from app.components.profile_page import profile_page
from app.components.achievements_page import achievements_page
from app.components.visited_locations_page import visited_locations_page


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            header(),
            rx.el.div(
                rx.match(
                    QuizState.current_page,
                    ("home", home_page()),
                    ("quiz", quiz_page()),
                    ("results", results_page()),
                    ("locations", locations_page()),
                    ("location_detail", location_detail_page()),
                    ("profile", profile_page()),
                    ("achievements", achievements_page()),
                    ("visited_locations", visited_locations_page()),
                    home_page(),
                ),
                class_name="w-full max-w-4xl mx-auto p-4 md:p-8",
            ),
            class_name="min-h-screen bg-[#0a0a0f] text-white flex flex-col items-center",
        ),
        class_name="font-['Press_Start_2P'] bg-[#0a0a0f]",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap",
            rel="stylesheet",
        ),
    ],
    stylesheets=["/styles.css"],
)
app.add_page(index, route="/")