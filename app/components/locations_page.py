import reflex as rx
from app.states.location_state import LocationState, Location
from app.components.sketchfab import sketchfab_model


def rating_bar(label: str, rating: rx.Var[float], color: str) -> rx.Component:
    width_percentage = rating / 5 * 100
    return rx.el.div(
        rx.el.p(f"{label}: {rating.to_string()}", class_name="text-xs text-gray-400"),
        rx.el.div(
            rx.el.div(
                style={
                    "width": width_percentage.to_string() + "%",
                    "backgroundColor": color,
                },
                class_name="h-2 transition-all duration-500",
            ),
            class_name="w-full bg-[#0a0a0f] border border-dashed border-gray-600 h-2 mt-1",
        ),
        class_name="w-full",
    )


def star_rating(rating: rx.Var[float], size_class: str = "h-4 w-4") -> rx.Component:
    return rx.el.div(
        rx.foreach(
            range(5),
            lambda i: rx.icon(
                tag=rx.cond(
                    rating >= i + 1, "star", rx.cond(rating > i, "star-half", "star")
                ),
                class_name=f"{size_class} {rx.cond(rating > i, 'text-[#ffc700]', 'text-gray-600')}",
            ),
        ),
        class_name="flex items-center",
    )


def location_card(location: Location) -> rx.Component:
    avg_ratings = LocationState.average_ratings.get(location["id"], {})
    overall_rating = avg_ratings.get("overall", 0.0)
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    location["icon"], class_name="h-8 w-8 text-[#00d4ff] mr-4 shrink-0"
                ),
                rx.el.div(
                    rx.el.h3(
                        location["name"],
                        class_name="text-md md:text-lg text-left text-[#00ff9f]",
                    ),
                    rx.el.p(
                        location["description"],
                        class_name="text-xs text-left text-gray-400 mt-1 line-clamp-2",
                    ),
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        overall_rating.to_string(), class_name="text-2xl font-bold"
                    ),
                    rx.el.p("/ 5.0", class_name="text-xs text-gray-500"),
                    class_name="flex items-baseline gap-1 text-white",
                ),
                star_rating(overall_rating),
                class_name="flex flex-col items-end",
            ),
            class_name="flex items-start justify-between",
        ),
        rx.el.div(
            rating_bar("Comfort", avg_ratings.get("comfort", 0.0), "#ff00ff"),
            rating_bar("Quietness", avg_ratings.get("quietness", 0.0), "#00d4ff"),
            rating_bar(
                "Accessibility", avg_ratings.get("accessibility", 0.0), "#00ff9f"
            ),
            rating_bar("Vibe Check", avg_ratings.get("vibe_check", 0.0), "#ffc700"),
            class_name="grid grid-cols-2 gap-x-4 gap-y-2 mt-4 pt-4 border-t border-dashed border-[#00d4ff]/20",
        ),
        on_click=lambda: LocationState.select_location(location["id"]),
        class_name="w-full p-4 md:p-6 bg-[#1a1a2e] pixel-border-cyan flex flex-col justify-between hover:bg-[#00d4ff]/20 hover:scale-105 transition-all duration-300 text-white",
    )


def locations_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Campus Nap Archives",
                class_name="text-3xl md:text-4xl text-[#00d4ff] text-shadow-neon text-center mb-4",
            ),
            rx.el.p(
                "Brave nappers have rated these spots. Find your next sanctuary or dare to review a new one.",
                class_name="text-center text-gray-300 max-w-2xl mx-auto text-sm md:text-base leading-relaxed mb-8 md:mb-12",
            ),
            class_name="flex flex-col items-center justify-center",
        ),
        rx.el.div(
            rx.foreach(LocationState.locations, location_card),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-8",
        ),
        class_name="w-full p-4 md:p-8 pixel-border bg-[#1a1a2e] animate-fade-in",
    )