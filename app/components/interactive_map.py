import reflex as rx
from app.states.location_state import LocationState as LS


class MapState(rx.State):
    """State for interactive map navigation"""
    selected_building: str = ""  # "library" or "jcit" or ""
    current_floor: str = "G"  # Current floor level
    hovered_icon: str = ""  # Currently hovered location icon
    show_floor_detail: bool = False  # Show detailed floor map
    
    # Building to floor mapping
    building_floors: dict[str, list[str]] = {
        "library": ["G"],
        "jcit": ["11", "P"]
    }
    
    # Location to building/floor mapping
    location_map: dict[str, dict[str, str]] = {
        "cloud-nine-credit": {"building": "library", "floor": "G", "icon": "far", "x": "60%", "y": "9%"},
        "the-spynap-alley": {"building": "library", "floor": "G", "icon": "middle", "x": "7%", "y": "9%"},
        "the-public-isolation": {"building": "library", "floor": "G", "icon": "close", "x": "43%", "y": "65%"},
        "the-urban-zen": {"building": "outdoor", "floor": "outdoor", "icon": "middle", "x": "60%", "y": "59%"},
        "the-shade-throne": {"building": "outdoor", "floor": "outdoor", "icon": "close", "x": "50%", "y": "48%"},
        "the-stonecold-zen": {"building": "outdoor", "floor": "outdoor", "icon": "far", "x": "40%", "y": "60%"},
        "the-bobafueled-snooze": {"building": "jcit", "floor": "P", "icon": "close", "x": "72%", "y": "28%"},
        "the-stairwell-stealth": {"building": "jcit", "floor": "11", "icon": "far", "x": "48%", "y": "35%"},
        "the-curtaincall-nap": {"building": "jcit", "floor": "11", "icon": "middle", "x": "60%", "y": "45%"},
        "the-modular-dream": {"building": "jcit", "floor": "11", "icon": "middle", "x": "53%", "y": "60%"},
    }
    
    @rx.event
    def select_building(self, building: str):
        """Select a building and show its first floor"""
        self.selected_building = building
        self.show_floor_detail = True
        if building in self.building_floors:
            self.current_floor = self.building_floors[building][0]
    
    @rx.event
    def change_floor(self, direction: str):
        """Navigate between floors"""
        if not self.selected_building:
            return
        
        floors = self.building_floors.get(self.selected_building, [])
        if not floors:
            return
        
        try:
            current_index = floors.index(self.current_floor)
            if direction == "up" and current_index > 0:
                self.current_floor = floors[current_index - 1]
            elif direction == "down" and current_index < len(floors) - 1:
                self.current_floor = floors[current_index + 1]
        except ValueError:
            pass
    
    @rx.event
    async def select_location_and_close(self, location_id: str):
        """Select a location and close the floor view"""
        location_state = await self.get_state(LS)
        await location_state.select_location(location_id)
        self.show_floor_detail = False
        self.selected_building = ""
    
    @rx.event
    def close_floor_view(self):
        """Close the detailed floor view"""
        self.show_floor_detail = False
        self.selected_building = ""
    
    @rx.event
    def set_hovered_icon(self, location_id: str):
        """Set the hovered location icon"""
        self.hovered_icon = location_id
    
    @rx.var
    def current_floor_locations(self) -> list[dict]:
        """Get locations for the current floor"""
        if not self.selected_building:
            return []
        
        # Access locations directly from the class
        all_locations = [
            {
                "id": "cloud-nine-credit",
                "location": "Study room on the G floor of the library",
                "name": "Cloud Nine Credit Charge",
                "icon_type": "far",
                "x": "30%",
                "y": "18%"
            },
            {
                "id": "the-spynap-alley",
                "location": "The corridor of bookshelves on the G floor of the library",
                "name": "The Spy-Nap Alley",
                "icon_type": "middle",
                "x": "7%",
                "y": "18%"
            },
            {
                "id": "the-public-isolation",
                "location": "Sofa on the G floor of the library",
                "name": "The Public Isolation Island",
                "icon_type": "close",
                "x": "42%",
                "y": "64%"
            },
            {
                "id": "the-bobafueled-snooze",
                "location": "JCIT Milk Tea Shop",
                "name": "The Boba-Fueled Snooze Booth",
                "icon_type": "close",
                "x": "68%",
                "y": "33%"
            },
            {
                "id": "the-stairwell-stealth",
                "location": "JCIT Stairwell",
                "name": "The Stairwell Stealth Suite",
                "icon_type": "far",
                "x": "43%",
                "y": "35%"
            },
            {
                "id": "the-curtaincall-nap",
                "location": "JCIT Study Room Partition Area",
                "name": "The Curtain-Call Nap Studio",
                "icon_type": "middle",
                "x": "63%",
                "y": "55%"
            },
            {
                "id": "the-modular-dream",
                "location": "JCIT Study Room Sofa",
                "name": "The Modular Dream Fort",
                "icon_type": "middle",
                "x": "54%",
                "y": "75%"
            },
        ]
        
        locations = []
        for loc in all_locations:
            loc_id = loc["id"]
            if loc_id in self.location_map:
                loc_info = self.location_map[loc_id]
                if (loc_info["building"] == self.selected_building and 
                    loc_info["floor"] == self.current_floor):
                    locations.append(loc)
        return locations
    
    def get_floor_locations(self, all_locations: list) -> list[dict]:
        """Get locations for the current floor (unused, kept for compatibility)"""
        return []
    
    @rx.var
    def can_go_up(self) -> bool:
        """Check if can navigate up"""
        if not self.selected_building:
            return False
        floors = self.building_floors.get(self.selected_building, [])
        try:
            return floors.index(self.current_floor) > 0
        except ValueError:
            return False
    
    @rx.var
    def can_go_down(self) -> bool:
        """Check if can navigate down"""
        if not self.selected_building:
            return False
        floors = self.building_floors.get(self.selected_building, [])
        try:
            return floors.index(self.current_floor) < len(floors) - 1
        except ValueError:
            return False
    
    @rx.var
    def floor_map_image(self) -> str:
        """Get the floor map image path"""
        if not self.selected_building or not self.current_floor:
            return ""
        
        if self.selected_building == "library":
            if self.current_floor == "G":
                return "/map images/Pao Yue-kong Library G Floor.png"
            elif self.current_floor == "1":
                return "/map images/Pao Yue-kong Library floor 1.png"
        elif self.selected_building == "jcit":
            if self.current_floor == "P":
                return "/map images/Jockey Club Innovation Tower P.png"
            elif self.current_floor == "11":
                return "/map images/Jockey Club Innovation Tower 11F.png"
        
        return ""
    
    @rx.var
    def building_display_name(self) -> str:
        """Get display name for building"""
        if self.selected_building == "library":
            return "Pao Yue-kong Library"
        elif self.selected_building == "jcit":
            return "Jockey Club Innovation Tower"
        return ""
    
    @rx.var
    def floor_display_name(self) -> str:
        """Get display name for current floor"""
        if self.selected_building == "library":
            if self.current_floor == "G":
                return "Ground Floor"
            elif self.current_floor == "1":
                return "1st Floor"
        elif self.selected_building == "jcit":
            if self.current_floor == "P":
                return "P Floor"
            elif self.current_floor == "11":
                return "11th Floor"
        return self.current_floor
    
    @rx.var
    def current_map_image(self) -> str:
        """Get current map image - floor map if building selected, otherwise campus map"""
        if self.selected_building:
            return self.floor_map_image
        return "/map images/POLYU MAP.png"


def floor_location_icon(location: rx.Var[dict]) -> rx.Component:
    """Interactive location icon on floor map"""
    
    return rx.el.div(
        # Icon
        rx.icon(
            tag="locate-fixed",
            size=32,
            color="#00ff9f",
            class_name="cursor-pointer transition-all duration-300",
            style={
                "filter": "drop-shadow(0 0 4px #00ff9f)",
                "_hover": {
                    "filter": "drop-shadow(0 0 12px #00ff9f)"
                }
            }
        ),
        # Popup on hover
        rx.cond(
            MapState.hovered_icon == location.id,
            rx.el.div(
                rx.el.div(
                    rx.text(
                        location.name,
                        class_name="text-xs font-bold text-white mb-1"
                    ),
                    rx.text(
                        location.location,
                        class_name="text-[10px] text-gray-300"
                    ),
                    class_name="bg-[#1a1a2e] border-2 border-[#00ff9f] p-2 rounded shadow-lg"
                ),
                class_name="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 whitespace-nowrap z-50"
            ),
            rx.el.div()
        ),
        on_mouse_enter=MapState.set_hovered_icon(location.id),
        on_mouse_leave=MapState.set_hovered_icon(""),
        on_click=MapState.select_location_and_close(location.id),
        class_name="absolute cursor-pointer",
        # Position based on location data
        style={
            "top": location.y,
            "left": location.x,
            "transform": "translate(-50%, -100%)",  # Center the icon horizontally and position bottom at coordinate
            "zIndex": rx.cond(MapState.hovered_icon == location.id, "100", "40"),
        }
    )


def outdoor_location_icon(location_id: str, location_name: str, x: str, y: str, icon_type: str) -> rx.Component:
    """Individual outdoor location icon on main campus map"""
    
    return rx.el.div(
        # Clickable icon
        rx.el.div(
            rx.icon(
                tag="locate-fixed",
                size=32,
                color="#00ff9f",
                class_name="cursor-pointer transition-all duration-300",
                style={
                    "filter": "drop-shadow(0 0 4px #00ff9f)",
                    "_hover": {
                        "filter": "drop-shadow(0 0 12px #00ff9f)"
                    }
                }
            ),
            on_click=LS.select_location(location_id),
            class_name="relative z-30"
        ),
        
        # Hover popup showing location name
        rx.cond(
            MapState.hovered_icon == location_id,
            rx.el.div(
                rx.el.div(
                    rx.text(
                        location_name,
                        class_name="text-sm font-bold text-[#00ff9f] mb-1"
                    ),
                    rx.text(
                        "Click to view details",
                        class_name="text-xs text-gray-300"
                    ),
                    class_name="bg-[#1a1a2e] border-2 border-[#00ff9f] p-3 rounded shadow-xl"
                ),
                class_name="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 whitespace-nowrap z-50"
            ),
            rx.el.div()
        ),
        
        on_mouse_enter=MapState.set_hovered_icon(location_id),
        on_mouse_leave=MapState.set_hovered_icon(""),
        
        class_name="absolute cursor-pointer",
        style={
            "top": y,
            "left": x,
            "transform": "translate(-50%, -100%)",
            "zIndex": rx.cond(MapState.hovered_icon == location_id, "100", "30"),
        }
    )


def building_icon_on_main_map(building: str, x: str, y: str) -> rx.Component:
    """Interactive building icon on main campus map"""
    
    return rx.el.div(
        # Clickable icon
        rx.el.div(
            rx.icon(
                tag="locate-fixed",
                size=32,
                color="#00ff9f",
                class_name="cursor-pointer transition-all duration-300",
                style={
                    "filter": "drop-shadow(0 0 4px #00ff9f)",
                    "_hover": {
                        "filter": "drop-shadow(0 0 12px #00ff9f)"
                    }
                }
            ),
            on_click=MapState.select_building(building),
            class_name="relative z-30"
        ),
        
        # Hover popup showing building name
        rx.cond(
            MapState.hovered_icon == building,
            rx.el.div(
                rx.el.div(
                    rx.text(
                        "Pao Yue-kong Library" if building == "library" else "Jockey Club Innovation Tower",
                        class_name="text-sm font-bold text-[#00ff9f] mb-1"
                    ),
                    rx.text(
                        "Click to explore",
                        class_name="text-xs text-gray-300"
                    ),
                    class_name="bg-[#1a1a2e] border-2 border-[#00ff9f] p-3 rounded shadow-xl"
                ),
                class_name="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 whitespace-nowrap z-50"
            ),
            rx.el.div()
        ),
        
        on_mouse_enter=MapState.set_hovered_icon(building),
        on_mouse_leave=MapState.set_hovered_icon(""),
        
        class_name="absolute cursor-pointer",
        style={
            "top": y,
            "left": x,
            "zIndex": rx.cond(MapState.hovered_icon == building, "100", "30"),
        }
    )


def interactive_campus_map() -> rx.Component:
    """Main interactive campus map"""
    return rx.el.div(
        # Map container
        rx.el.div(
            # Header with title and back button
            rx.el.div(
                rx.cond(
                    MapState.selected_building != "",
                    # Floor view header
                    rx.el.div(
                        rx.el.button(
                            rx.icon(tag="arrow-left", size=20, color="#00ff9f"),
                            rx.text("Back to Campus Map", class_name="ml-2 text-[#00ff9f]"),
                            on_click=MapState.close_floor_view,
                            class_name="flex items-center gap-2 px-3 py-2 hover:bg-gray-800 rounded transition-colors mb-2"
                        ),
                        rx.el.h3(
                            f"[ ", MapState.building_display_name, " - ", MapState.floor_display_name, " ]",
                            class_name="text-[#00ff9f] font-bold mb-3 text-center tracking-widest text-sm"
                        ),
                        class_name="w-full"
                    ),
                    # Campus map header
                    rx.el.h3(
                        "[ CAMPUS MAP ]",
                        class_name="text-[#00ff9f] font-bold mb-3 text-center tracking-widest text-sm"
                    )
                ),
                class_name="w-full"
            ),
            
            # Main map display area
            rx.el.div(
                # Map image (campus or floor)
                rx.el.div(
                    rx.image(
                        src=MapState.current_map_image,
                        class_name="w-full h-auto"
                    ),
                    
                    # Campus map icons (only show when no building selected)
                    rx.cond(
                        MapState.selected_building == "",
                        rx.fragment(
                            # Building icons
                            building_icon_on_main_map("library", "47%", "76%"),
                            building_icon_on_main_map("jcit", "48%", "28%"),
                            
                            # Outdoor locations
                            outdoor_location_icon("the-urban-zen", "The Urban Zen Bench", "60%", "59%", "middle"),
                            outdoor_location_icon("the-shade-throne", "The Shade Throne", "58%", "51%", "close"),
                            outdoor_location_icon("the-stonecold-zen", "The Stone-Cold Zen Zone", "57%", "62%", "far"),
                        ),
                        rx.fragment()
                    ),
                    
                    # Floor location icons (only show when building selected)
                    rx.cond(
                        MapState.selected_building != "",
                        rx.foreach(
                            MapState.current_floor_locations,
                            floor_location_icon
                        ),
                        rx.fragment()
                    ),
                    
                    class_name="relative w-full"
                ),
                
                # Floor navigation arrows (only show when building selected and has multiple floors)
                rx.cond(
                    (MapState.can_go_up) | (MapState.can_go_down),
                    rx.el.div(
                        # Up arrow
                        rx.cond(
                            MapState.can_go_up,
                            rx.el.button(
                                rx.icon(tag="chevron-up", size=32, color="#00ff9f"),
                                on_click=MapState.change_floor("up"),
                                class_name="p-3 hover:bg-gray-800 rounded transition-colors"
                            ),
                            rx.el.div(class_name="w-12 h-12")
                        ),
                        # Down arrow
                        rx.cond(
                            MapState.can_go_down,
                            rx.el.button(
                                rx.icon(tag="chevron-down", size=32, color="#00ff9f"),
                                on_click=MapState.change_floor("down"),
                                class_name="p-3 hover:bg-gray-800 rounded transition-colors"
                            ),
                            rx.el.div(class_name="w-12 h-12")
                        ),
                        class_name="flex flex-col items-center justify-center gap-2 px-4 absolute right-4 top-1/2 transform -translate-y-1/2 z-50 bg-[#0a0a0f]/90 border-2 border-[#00ff9f] rounded p-2"
                    ),
                    rx.fragment()
                ),
                
                class_name="relative"
            ),
            
            class_name="w-full border-2 border-[#00ff9f] bg-[#0a0a0f] p-4"
        ),
        
        class_name="w-full mb-8"
    )
