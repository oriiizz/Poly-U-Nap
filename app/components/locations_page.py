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
    is_checked_in = LocationState.checked_in_locations.contains(location["id"])
    
    rarity_color = rx.match(
        location["rarity"],
        ("LEGENDARY", "#ffd700"),
        ("EPIC", "#bd00ff"),
        ("RARE", "#00d4ff"),
        ("UNCOMMON", "#00ff9f"),
        ("MYTHICAL", "#ff0055"),
        "gray-400"
    )

    return rx.el.div(
        # Header with Icon and Name
        rx.el.div(
            rx.icon(
                location["icon"], 
                class_name="h-8 w-8 mr-4 shrink-0",
                style={"color": rarity_color}
            ),
            rx.el.div(
                rx.el.h3(
                    location["name"],
                    class_name="text-md md:text-lg text-left font-bold tracking-wider",
                    style={"color": rarity_color}
                ),
                rx.cond(
                    is_checked_in,
                    rx.el.div(
                        rx.icon("circle-check", size=12, class_name="mr-1 text-[#00ff9f]"),
                        rx.text("CHECKED IN", class_name="text-[10px] text-[#00ff9f] font-bold"),
                        class_name="flex items-center mt-1"
                    ),
                    rx.el.div()
                ),
                class_name="flex flex-col"
            ),
            class_name="flex items-center mb-4",
        ),
        
        # Description
        rx.el.p(
            location["description"],
            class_name="text-xs text-left text-gray-400 mb-4 font-mono leading-relaxed",
        ),

        # Stats and Button
        rx.el.div(
            rx.el.div(
                rx.icon("volume-2", size=12, class_name="mr-1 text-gray-500"),
                rx.text(avg_ratings.get("quietness", 0.0), "/5", class_name="text-xs text-gray-400 mr-3"),
                
                rx.icon("user", size=12, class_name="mr-1 text-gray-500"),
                rx.text(avg_ratings.get("comfort", 0.0), "/5", class_name="text-xs text-gray-400 mr-3"),
                
                rx.icon("star", size=12, class_name="mr-1 text-gray-500"),
                rx.text(overall_rating, "/5", class_name="text-xs text-gray-400"),
                
                class_name="flex items-center mb-3"
            ),
            rx.el.button(
                "VIEW DETAILS",
                on_click=lambda: LocationState.select_location(location["id"]),
                class_name="w-full border border-[#00ff9f] text-[#00ff9f] text-xs py-2 hover:bg-[#00ff9f] hover:text-black transition-colors font-bold tracking-wider"
            ),
            class_name="mt-auto w-full"
        ),
        
        class_name="w-full p-4 md:p-6 bg-[#1a1a2e] border border-[#00ff9f]/30 flex flex-col h-full hover:border-[#00ff9f] transition-all duration-300",
    )


def stat_box(value: rx.Var, label: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.text(value, class_name=f"text-xl font-bold text-[{color}] mb-1"),
        rx.text(label, class_name="text-[10px] text-gray-400 uppercase tracking-wider"),
        class_name=f"flex flex-col items-center justify-center p-4 border border-[{color}] bg-[{color}]/5"
    )


def locations_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            # Header
            rx.el.div(
                rx.el.div(
                    rx.el.button(
                        rx.icon("arrow-left", size=16),
                        # on_click=lambda: QuizState.set_page("home"), # Assuming QuizState is available or imported if needed, but keeping it simple for now or removing back button if not in design. 
                        # The design shows a back button.
                        class_name="p-1 border border-[#00ff9f] text-[#00ff9f] hover:bg-[#00ff9f] hover:text-black transition-colors mr-4",
                    ),
                    rx.el.div(
                        rx.el.h1("NAP QUEST MAP", class_name="text-xl font-bold text-[#00ff9f] tracking-widest text-shadow-neon-green"),
                        rx.el.p("Select location to begin mission", class_name="text-xs text-gray-400 font-mono"),
                        class_name="flex flex-col"
                    ),
                    class_name="flex items-center"
                ),
                rx.icon("map-pin", class_name="text-[#bd00ff] w-6 h-6"),
                class_name="w-full border-2 border-[#00ff9f] p-4 flex justify-between items-center bg-[#00ff9f]/5 mb-6"
            ),

            # Stats Bar
            rx.el.div(
                stat_box(LocationState.missions_count, "MISSIONS", "#00ff9f"),
                stat_box(LocationState.explored_count, "CHECKED IN", "#bd00ff"),
                stat_box(LocationState.s_rank_count, "S-RANK", "#ffd700"),
                stat_box(LocationState.secrets_found_count, "SECRETS", "#ff0055"),
                class_name="grid grid-cols-4 gap-4 w-full mb-8"
            ),

            # Locations Grid
            rx.el.div(
                rx.foreach(LocationState.locations, location_card),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 w-full",
            ),
            
            # Tip Footer
            rx.el.div(
                rx.text("[TIP: Click on location to start quest and rate your experience]", class_name="text-[10px] text-gray-400 tracking-widest font-mono"),
                class_name="w-full border border-gray-700 p-3 mt-8 text-center bg-gray-900/50"
            ),

            class_name="max-w-4xl mx-auto w-full flex flex-col"
        ),
        class_name="min-h-screen bg-[#050510] p-4 md:p-8 font-mono"
    )
