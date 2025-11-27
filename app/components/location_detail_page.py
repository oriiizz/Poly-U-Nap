import reflex as rx
from app.states.quiz_state import QuizState
from app.states.location_state import LocationState
from app.components.sketchfab import sketchfab_model


def rating_slider(category: str, label: str, emoji: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(f"{label} {emoji}", class_name="text-md text-[#00d4ff]"),
            rx.el.span(
                LocationState.new_rating[category],
                class_name="text-lg font-bold text-white",
            ),
            class_name="flex justify-between items-center mb-2",
        ),
        rx.el.input(
            type="range",
            min=1,
            max=5,
            default_value=LocationState.new_rating[category].to(str),
            on_change=lambda val: LocationState.set_new_rating_value(
                category, val
            ).throttle(50),
            key=f"rating-slider-{category}",
            class_name="w-full h-2 bg-[#0a0a0f] rounded-lg appearance-none cursor-pointer range-lg accent-[#00ff9f]",
        ),
        class_name="w-full",
    )


def location_detail_page() -> rx.Component:
    return rx.cond(
        LocationState.selected_location,
        rx.el.div(
            rx.el.button(
                rx.icon("arrow-left", class_name="mr-2 h-5 w-5"),
                "Back to Locations",
                on_click=lambda: QuizState.set_page("locations"),
                class_name="mb-6 md:mb-8 flex items-center text-sm text-gray-400 hover:text-white transition-colors",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            LocationState.selected_location["name"],
                            class_name="text-2xl md:text-3xl text-[#00ff9f] text-shadow-neon mb-2",
                        ),
                        rx.el.p(
                            LocationState.selected_location["description"],
                            class_name="text-gray-300 leading-relaxed mb-6 text-sm md:text-base",
                        ),
                        # 3D Viewer
                        rx.el.div(
                            rx.el.h3(
                                "3D Preview",
                                class_name="text-lg text-center text-[#00d4ff] mb-4",
                            ),
                            sketchfab_model(
                                model_id=LocationState.selected_location["model_id"],
                                height="300px",
                                title=LocationState.selected_location["name"]
                            ),
                            class_name="mb-6 p-4 bg-transparent",  # Changed to bg-transparent
                        ),
                        class_name="w-full md:w-1/2 md:pr-8",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Submit Your Rating",
                            class_name="text-xl md:text-2xl text-[#00ff9f] text-center mb-6",
                        ),
                        rx.el.div(
                            rating_slider("comfort", "Comfort", "☺"),
                            rating_slider("quietness", "Quietness", "🤫"),
                            rating_slider("accessibility", "Accessibility", "🚶"),
                            rating_slider("vibe_check", "Vibe Check", "😎"),
                            rx.el.button(
                                "Submit to Archives",
                                on_click=LocationState.submit_rating,
                                class_name="mt-8 w-full flex items-center justify-center text-base md:text-lg bg-transparent text-[#ff00ff] font-bold py-3 px-6 md:py-4 md:px-8 pixel-border-magenta hover:bg-[#ff00ff]/20 transition-all duration-300",
                            ),
                            class_name="space-y-6 p-4 md:p-6 bg-[#1a1a2e] pixel-border-cyan",
                        ),
                        class_name="w-full md:w-1/2 mt-8 md:mt-0",
                    ),
                    class_name="flex flex-col md:flex-row",
                )
            ),
            class_name="w-full p-4 md:p-8 pixel-border bg-[#1a1a2e] animate-fade-in",
        ),
        rx.el.div(
            rx.el.p(
                "No location selected. Returning to archives...",
                class_name="text-xl text-center",
            ),
            on_mount=lambda: QuizState.set_page("locations"),
        ),
    )