**Poly-U-Nap** is a web application designed to help students at PolyU find the best places to take a nap on campus. Whether you''re looking for a quiet corner in the library or a hidden gem in the Innovation Tower, this app has you covered.

> *Scan. Rate. Nap. Repeat.*

## 🌟 Features

*   **Interactive Campus Map**: Navigate through different buildings (Library, JCIT) and floors to find nap spots.
*   **Nap Spot Discovery**: Detailed information about each nap spot, including comfort, quietness, and "danger" levels.
*   **Sleep Personality Quiz**: Find out what kind of sleeper you are and get personalized recommendations.
*   **Check-in System**: "Check in" to locations to earn XP and level up your profile.
*   **Rating System**: Rate locations based on your experience.
*   **Achievements**: Unlock badges and achievements for exploring different spots and leveling up.
*   **Profile & Stats**: Track your visited locations, favorite spots, and sleeper rank.

## 🛠️ Tech Stack

*   **Framework**: [Reflex](https://reflex.dev/) (Python)
*   **Styling**: Tailwind CSS (via Reflex)
*   **Icons**: Lucide Icons (via Reflex)

## 🚀 Getting Started

### Prerequisites

*   Python 3.8 or higher
*   [Node.js](https://nodejs.org/) (required by Reflex for the frontend build)

### Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd Poly-U-Nap
    ```

2.  **Create a virtual environment** (Recommended)
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

1.  **Initialize Reflex** (First time only)
    ```bash
    reflex init
    ```

2.  **Run the development server**
    ```bash
    reflex run
    ```

    The app should now be running at `http://localhost:3000`.

## 📂 Project Structure

```
Poly-U-Nap/
├── app/                    # Main application source code
│   ├── components/         # UI components (pages, map, header, etc.)
│   ├── states/             # State management (logic, variables)
│   ├── app.py              # Main entry point
│   └── __init__.py
├── assets/                 # Static assets
│   ├── map images/         # Campus and floor maps
│   └── styles.css          # Custom CSS
├── rxconfig.py             # Reflex configuration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 🗺️ How to Edit Map Locations

To adjust the position of icons on the interactive map:

1.  Open `app/components/interactive_map.py`.
2.  Locate the `current_floor_locations` function.
3.  Update the `x` (horizontal) and `y` (vertical) percentage values for the specific location dictionary.

```python
{
    "id": "location-id",
    "x": "50%",  # 0% is Left, 100% is Right
    "y": "50%"   # 0% is Top, 100% is Bottom
}
```

## 📄 License

This project is for educational and creative purposes.
'