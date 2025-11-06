# main.py - Reflex app entrypoint for Poly U Nap
import reflex as rx
from state import AppState
from ui import index_page, dashboard_page

app = rx.App(state=AppState)
app.add_page(index_page, route="/")
app.add_page(dashboard_page, route="/dashboard")
app.compile()

if __name__ == '__main__':
    # Reflex dev server
    rx.run(host='0.0.0.0', port=3000)
