import reflex as rx
from app.states.quiz_state import QuizState
from app.states.location_state import LocationState
from app.components.sketchfab import sketchfab_model


def rating_bar_stat(label: str, category: str, icon: str, color: str) -> rx.Component:
    """Display a rating stat with bars instead of slider"""
    current_value = LocationState.new_rating[category]
    
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, size=20, class_name=f"mr-3", style={"color": color}),
            rx.text(label.upper(), class_name="text-sm text-gray-300 font-bold tracking-wider flex-1"),
            rx.el.div(
                rx.foreach(
                    range(5),
                    lambda i: rx.el.div(
                        class_name=rx.cond(
                            current_value > i,
                            "w-4 h-4 mr-1",
                            "w-4 h-4 mr-1 opacity-30"
                        ),
                        style={
                            "backgroundColor": rx.cond(current_value > i, color, "#333")
                        }
                    )
                ),
                class_name="flex items-center"
            ),
            class_name="flex items-center mb-2"
        ),
        rx.el.input(
            type="range",
            min=1,
            max=5,
            default_value=LocationState.new_rating[category].to(str),
            on_change=lambda val: LocationState.set_new_rating_value(category, val).throttle(50),
            key=f"rating-slider-{category}",
            class_name="w-full h-1 bg-[#1a1a2e] rounded-lg appearance-none cursor-pointer accent-[#00ff9f] opacity-0 absolute",
            style={"marginTop": "-30px"}
        ),
        rx.el.input(
            type="range",
            min=1,
            max=5,
            default_value=LocationState.new_rating[category].to(str),
            on_change=lambda val: LocationState.set_new_rating_value(category, val).throttle(50),
            class_name="w-full h-2 bg-[#0a0a0f] rounded-lg appearance-none cursor-pointer range-lg accent-[#00ff9f]",
        ),
        class_name="w-full mb-4 relative"
    )


def location_detail_page() -> rx.Component:
    return rx.cond(
        LocationState.selected_location,
        rx.el.div(
            rx.el.div(
                # Back Button and Title Header
                rx.el.div(
                    rx.el.button(
                        rx.icon("arrow-left", size=20),
                        on_click=lambda: QuizState.set_page("locations"),
                        class_name="p-2 border-2 border-[#00ff9f] text-[#00ff9f] hover:bg-[#00ff9f] hover:text-black transition-colors"
                    ),
                    rx.el.div(
                        rx.icon(
                            LocationState.selected_location["icon"],
                            size=32,
                            class_name="mr-4",
                            style={"color": "#00ff9f"}
                        ),
                        rx.el.div(
                            # Creative Name (larger, green)
                            rx.el.h1(
                                LocationState.selected_location["name"],
                                class_name="text-xl md:text-2xl text-[#00ff9f] font-bold tracking-widest uppercase text-shadow-neon-green"
                            ),
                            # Physical Location (smaller, gray)
                            rx.el.div(
                                rx.el.p(
                                    "\ud83d\udccd ", LocationState.selected_location["location"],
                                    class_name="text-xs text-gray-500 mt-1 font-mono cursor-help hover:text-[#00ff9f] transition-colors",
                                    on_mouse_enter=LocationState.set_hovering_location_title(True),
                                    on_mouse_leave=LocationState.set_hovering_location_title(False),
                                ),
                                # Hover Map Popup
                                rx.cond(
                                    LocationState.is_hovering_location_title,
                                    rx.el.div(
                                        rx.el.div(
                                            rx.image(
                                                src=LocationState.selected_location_map_image,
                                                class_name="w-full h-full object-cover opacity-50"
                                            ),
                                            # Pin
                                            rx.el.div(
                                                rx.icon("map-pin", size=24, class_name="text-[#00ff9f] animate-bounce"),
                                                class_name="absolute transform -translate-x-1/2 -translate-y-full",
                                                style={
                                                    "left": LocationState.selected_location_coords["x"],
                                                    "top": LocationState.selected_location_coords["y"]
                                                }
                                            ),
                                            class_name="relative w-64 h-48 bg-[#0a0a0f] border-2 border-[#00ff9f] overflow-hidden rounded-lg shadow-2xl"
                                        ),
                                        class_name="absolute z-50 mt-2 transform -translate-x-1/4 pointer-events-none"
                                    ),
                                    rx.el.div()
                                ),
                                class_name="relative"
                            ),
                            class_name="flex flex-col"
                        ),
                        class_name="flex items-center"
                    ),
                    class_name="flex items-center gap-4 mb-6"
                ),
                
                # Description Box
                rx.el.div(
                    rx.el.p(
                        LocationState.selected_location["description"],
                        class_name="text-xs md:text-sm text-gray-400 leading-relaxed font-mono"
                    ),
                    class_name="w-full border border-[#bd00ff] bg-[#1a1a2e] p-4 md:p-6 mb-6"
                ),

                # 3D Model Preview
                rx.el.div(
                    rx.el.h3(
                        "[ 3D LOCATION SCAN ]",
                        class_name="text-[#00d4ff] font-bold mb-3 text-center tracking-widest text-sm",
                    ),
                    sketchfab_model(
                        model_id=LocationState.selected_location["model_id"],
                        height="300px",
                        title=LocationState.selected_location["name"]
                    ),
                    class_name="w-full border border-[#00d4ff] p-4 bg-[#0a0a0f]/50 mb-6"
                ),

                # Stats Grid (Comfort, Noise, Temp, Traffic)
                rx.el.div(
                    # Comfort
                    rx.el.div(
                        rx.el.div(
                            rx.icon("sofa", size=20, class_name="mr-2 text-[#00ff9f]"),
                            rx.text("COMFORT", class_name="text-xs text-gray-400 font-bold tracking-wider"),
                            class_name="flex items-center mb-2"
                        ),
                        rx.el.div(
                            rx.foreach(
                                range(5),
                                lambda i: rx.el.div(
                                    class_name=rx.cond(
                                        LocationState.new_rating["comfort"] > i,
                                        "w-3 h-3 bg-[#00ff9f] mr-1",
                                        "w-3 h-3 bg-[#333] mr-1"
                                    )
                                )
                            ),
                            class_name="flex"
                        ),
                        class_name="border border-[#00ff9f] bg-[#00ff9f]/5 p-4"
                    ),
                    # Noise
                    rx.el.div(
                        rx.el.div(
                            rx.icon("volume-2", size=20, class_name="mr-2 text-[#bd00ff]"),
                            rx.text("NOISE", class_name="text-xs text-gray-400 font-bold tracking-wider"),
                            class_name="flex items-center mb-2"
                        ),
                        rx.el.div(
                            rx.foreach(
                                range(5),
                                lambda i: rx.el.div(
                                    class_name=rx.cond(
                                        LocationState.new_rating["quietness"] > i,
                                        "w-3 h-3 bg-[#bd00ff] mr-1",
                                        "w-3 h-3 bg-[#333] mr-1"
                                    )
                                )
                            ),
                            class_name="flex"
                        ),
                        class_name="border border-[#bd00ff] bg-[#bd00ff]/5 p-4"
                    ),
                    # Accessibility
                    rx.el.div(
                        rx.el.div(
                            rx.icon("map-pin", size=20, class_name="mr-2 text-[#ff0055]"),
                            rx.text("ACCESS", class_name="text-xs text-gray-400 font-bold tracking-wider"),
                            class_name="flex items-center mb-2"
                        ),
                        rx.el.div(
                            rx.foreach(
                                range(5),
                                lambda i: rx.el.div(
                                    class_name=rx.cond(
                                        LocationState.new_rating["accessibility"] > i,
                                        "w-3 h-3 bg-[#ff0055] mr-1",
                                        "w-3 h-3 bg-[#333] mr-1"
                                    )
                                )
                            ),
                            class_name="flex"
                        ),
                        class_name="border border-[#ff0055] bg-[#ff0055]/5 p-4"
                    ),
                    # Vibe Check
                    rx.el.div(
                        rx.el.div(
                            rx.icon("sparkles", size=20, class_name="mr-2 text-[#ffd700]"),
                            rx.text("VIBE", class_name="text-xs text-gray-400 font-bold tracking-wider"),
                            class_name="flex items-center mb-2"
                        ),
                        rx.el.div(
                            rx.foreach(
                                range(5),
                                lambda i: rx.el.div(
                                    class_name=rx.cond(
                                        LocationState.new_rating["vibe_check"] > i,
                                        "w-3 h-3 bg-[#ffd700] mr-1",
                                        "w-3 h-3 bg-[#333] mr-1"
                                    )
                                )
                            ),
                            class_name="flex"
                        ),
                        class_name="border border-[#ffd700] bg-[#ffd700]/5 p-4"
                    ),
                    # Danger
                    rx.el.div(
                        rx.el.div(
                            rx.icon("shield-alert", size=20, class_name="mr-2 text-[#00d4ff]"),
                            rx.text("DANGER", class_name="text-xs text-gray-400 font-bold tracking-wider"),
                            class_name="flex items-center mb-2"
                        ),
                        rx.el.div(
                            rx.foreach(
                                range(5),
                                lambda i: rx.el.div(
                                    class_name=rx.cond(
                                        LocationState.new_rating["danger"] > i,
                                        "w-3 h-3 bg-[#00d4ff] mr-1",
                                        "w-3 h-3 bg-[#333] mr-1"
                                    )
                                )
                            ),
                            class_name="flex"
                        ),
                        class_name="border border-[#00d4ff] bg-[#00d4ff]/5 p-4"
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6"
                ),

                # Rating Section with Interactive Sliders
                rx.el.div(
                    rx.el.div(
                        rx.icon("zap", size=16, class_name="mr-2 text-[#00ff9f]"),
                        rx.text("RATE THIS MISSION", class_name="text-sm text-[#00ff9f] font-bold tracking-widest"),
                        class_name="flex items-center justify-center mb-4"
                    ),
                    rating_bar_stat("COMFORT", "comfort", "sofa", "#00ff9f"),
                    rating_bar_stat("QUIETNESS", "quietness", "volume-2", "#bd00ff"),
                    rating_bar_stat("ACCESSIBILITY", "accessibility", "map-pin", "#ff0055"),
                    rating_bar_stat("VIBE CHECK", "vibe_check", "sparkles", "#ffd700"),
                    rating_bar_stat("DANGER", "danger", "shield-alert", "#00d4ff"),
                    class_name="w-full border-2 border-[#00ff9f] bg-[#0a0a0f] p-6 mb-6"
                ),

                # First Time Rating Bonus
                rx.cond(
                    ~LocationState.ratings.contains(LocationState.selected_location["id"]),
                    rx.el.div(
                        rx.icon("triangle-alert", size=16, class_name="mr-2 text-[#ffd700]"),
                        rx.text("▲ FIRST TIME HERE? Rate this location to unlock XP! ▲", class_name="text-xs text-[#ffd700] font-bold tracking-wider"),
                        rx.icon("triangle-alert", size=16, class_name="ml-2 text-[#ffd700]"),
                        class_name="w-full border border-[#ffd700] bg-[#ffd700]/10 p-3 flex items-center justify-center mb-6"
                    ),
                    rx.el.div()
                ),

                # Submit Button
                rx.el.button(
                    rx.icon("send", size=16, class_name="mr-2"),
                    "SUBMIT RATING",
                    on_click=LocationState.submit_rating,
                    class_name="w-full bg-[#00ff9f] text-black font-bold text-sm py-3 hover:bg-[#00ff9f]/80 transition-colors flex items-center justify-center tracking-wider mb-6"
                ),

                # Check-in Section
                rx.el.div(
                    rx.el.h3(
                        "[ CHECK IN ]",
                        class_name="text-[#bd00ff] font-bold mb-4 text-center tracking-widest text-sm",
                    ),
                    rx.el.div(
                        rx.cond(
                            LocationState.checked_in_locations.contains(LocationState.selected_location["id"]),
                            rx.el.div(
                                rx.icon("circle-check", size=48, class_name="text-[#00ff9f] mb-3"),
                                rx.text("ALREADY CHECKED IN", class_name="text-sm text-[#00ff9f] font-bold tracking-wider"),
                                rx.text("You've visited this location!", class_name="text-xs text-gray-400 mt-2"),
                                class_name="flex flex-col items-center justify-center p-6"
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.text("Visit this location and check in to earn XP!", class_name="text-xs text-gray-400 mb-4 text-center"),
                                    class_name="flex flex-col items-center"
                                ),
                                rx.el.button(
                                    rx.icon("map-pin", size=16, class_name="mr-2"),
                                    "CHECK IN NOW",
                                    on_click=lambda: LocationState.check_in_location(LocationState.selected_location["id"]),
                                    class_name="w-full border-2 border-[#bd00ff] text-[#bd00ff] text-sm py-3 hover:bg-[#bd00ff] hover:text-black transition-colors font-bold tracking-wider flex items-center justify-center"
                                ),
                                class_name="flex flex-col items-center justify-center p-6"
                            )
                        ),
                        class_name="w-full border-2 border-[#bd00ff] bg-[#bd00ff]/5 p-4"
                    ),
                    class_name="w-full mb-6",
                ),

                class_name="max-w-3xl mx-auto w-full flex flex-col"
            ),
            class_name="min-h-screen bg-[#050510] p-4 md:p-8 font-mono animate-fade-in",
        ),
        rx.el.div(
            rx.el.p(
                "No location selected. Returning to map...",
                class_name="text-xl text-center text-gray-400",
            ),
            on_mount=lambda: QuizState.set_page("locations"),
            class_name="min-h-screen bg-[#050510] flex items-center justify-center"
        ),
    )