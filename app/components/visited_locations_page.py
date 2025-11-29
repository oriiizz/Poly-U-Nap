import reflex as rx
from app.states.location_state import LocationState, Location
from app.states.quiz_state import QuizState


def visited_location_card(location: Location) -> rx.Component:
    avg_ratings = LocationState.average_ratings.get(location["id"], {})
    overall_rating = avg_ratings.get("overall", 0.0)
    
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
                rx.el.div(
                    rx.icon("circle-check", size=12, class_name="mr-1 text-[#00ff9f]"),
                    rx.text("CHECKED IN", class_name="text-[10px] text-[#00ff9f] font-bold"),
                    class_name="flex items-center mt-1"
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


def visited_locations_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            # Header
            rx.el.div(
                rx.el.div(
                    rx.el.button(
                        rx.icon("arrow-left", size=16),
                        on_click=lambda: QuizState.set_page("profile"),
                        class_name="p-1 border border-[#bd00ff] text-[#bd00ff] hover:bg-[#bd00ff] hover:text-black transition-colors mr-4",
                    ),
                    rx.el.div(
                        rx.el.h1("VISITED LOCATIONS", class_name="text-xl font-bold text-[#bd00ff] tracking-widest text-shadow-neon-purple"),
                        rx.el.p("Places you've checked in to", class_name="text-xs text-gray-400 font-mono"),
                        class_name="flex flex-col"
                    ),
                    class_name="flex items-center"
                ),
                rx.icon("map-pin", class_name="text-[#00ff9f] w-6 h-6"),
                class_name="w-full border-2 border-[#bd00ff] p-4 flex justify-between items-center bg-[#bd00ff]/5 mb-6"
            ),

            # Stats Bar
            rx.el.div(
                rx.el.div(
                    rx.text(LocationState.explored_count, class_name="text-2xl font-bold text-[#bd00ff] mb-1"),
                    rx.text("TOTAL VISITED", class_name="text-[10px] text-gray-400 uppercase tracking-wider"),
                    class_name="flex flex-col items-center justify-center p-4 border border-[#bd00ff] bg-[#bd00ff]/5"
                ),
                rx.el.div(
                    rx.text(f"{LocationState.explored_count}/{LocationState.locations.length()}", class_name="text-2xl font-bold text-[#00ff9f] mb-1"),
                    rx.text("PROGRESS", class_name="text-[10px] text-gray-400 uppercase tracking-wider"),
                    class_name="flex flex-col items-center justify-center p-4 border border-[#00ff9f] bg-[#00ff9f]/5"
                ),
                class_name="grid grid-cols-2 gap-4 w-full mb-8"
            ),

            # Conditional: Show locations or empty state
            rx.cond(
                LocationState.explored_count > 0,
                # Locations Grid
                rx.el.div(
                    rx.foreach(
                        LocationState.locations,
                        lambda loc: rx.cond(
                            LocationState.checked_in_locations.contains(loc["id"]),
                            visited_location_card(loc),
                            rx.fragment()
                        )
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 w-full",
                ),
                # Empty State
                rx.el.div(
                    rx.icon("map-pin-off", size=48, class_name="text-gray-600 mb-4"),
                    rx.text("NO LOCATIONS VISITED YET", class_name="text-lg font-bold text-gray-500 tracking-widest mb-2"),
                    rx.text("Start exploring and check in at locations to see them here!", class_name="text-xs text-gray-400 text-center max-w-xs mb-4"),
                    rx.el.button(
                        rx.icon("map", size=16, class_name="mr-2"),
                        "EXPLORE LOCATIONS",
                        on_click=lambda: QuizState.set_page("locations"),
                        class_name="border-2 border-[#00ff9f] text-[#00ff9f] px-6 py-3 hover:bg-[#00ff9f] hover:text-black transition-colors font-bold tracking-wider flex items-center"
                    ),
                    class_name="w-full border-2 border-gray-800 p-12 flex flex-col items-center justify-center bg-[#0a0a0f]"
                )
            ),
            
            # Tip Footer
            rx.el.div(
                rx.text("[TIP: Check in at more locations to unlock collection achievements]", class_name="text-[10px] text-gray-400 tracking-widest font-mono"),
                class_name="w-full border border-gray-700 p-3 mt-8 text-center bg-gray-900/50"
            ),

            class_name="max-w-4xl mx-auto w-full flex flex-col"
        ),
        class_name="min-h-screen bg-[#050510] p-4 md:p-8 font-mono"
    )
