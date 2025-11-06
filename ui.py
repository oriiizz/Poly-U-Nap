# ui.py - pages built with Reflex components
import reflex as rx
from state import AppState

def header():
    return rx.hstack(
        rx.heading('Poly U Nap', size='xl'),
        rx.button('Toggle Dark', on_click=AppState.toggle_dark),
        rx.link('Dashboard', href='/dashboard'),
        rx.spacer(),
        rx.box() # placeholder
    , align='center', justify='space-between', padding='2')

def index_page():
    return rx.box(
        header(),
        rx.vstack(
            rx.text('Submit a sleep review', as_='h2'),
            rx.input(placeholder='Location', value=AppState.location, on_change=AppState.set_location),
            rx.hstack(
                rx.text('Rating (1-5):'),
                rx.number_input(value=AppState.rating, min=1, max=5, on_change=AppState.set_rating)
            ),
            rx.hstack(
                rx.text('Hours slept:'),
                rx.number_input(value=AppState.hours, min=0, max=24, step=0.25, on_change=AppState.set_hours)
            ),
            rx.hstack(
                rx.text('Quality (1-5):'),
                rx.number_input(value=AppState.quality, min=1, max=5, on_change=AppState.set_quality)
            ),
            rx.textarea(placeholder='Optional comment', value=AppState.comment, on_change=AppState.set_comment),
            rx.button('Submit', on_click=AppState.submit_review),
            rx.link('Go to Dashboard', href='/dashboard')
        , padding='4', spacing='4'),
        padding='4'
    )

def simple_svg_bar_chart(values):
    # Generate a tiny inline SVG bar chart from list of numbers (values)
    if not values:
        return rx.text('No data yet')
    max_v = max(values)
    width = 300
    height = 100
    bar_width = width / len(values)
    rects = []
    for i, v in enumerate(values):
        h = (v / max_v) * height if max_v>0 else 0
        x = i * bar_width
        y = height - h
        rects.append(f'<rect x="{x}" y="{y}" width="{bar_width-2}" height="{h}" />')
    svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" preserveAspectRatio="none">{"".join(rects)}</svg>'
    return rx.box(rx.raw(svg))

def dashboard_page():
    # Dashboard reads AppState.cached_stats and recent reviews
    stats = AppState.cached_stats or {}
    reviews = AppState.get_reviews()
    hours_values = [r['hours'] for r in reviews][-10:]
    return rx.box(
        header(),
        rx.vstack(
            rx.hstack(
                rx.card(rx.vstack(rx.text('Total reviews'), rx.heading(str(stats.get('count',0))))),
                rx.card(rx.vstack(rx.text('Avg hours'), rx.heading(str(stats.get('avg_hours',0))))),
                rx.card(rx.vstack(rx.text('Avg quality'), rx.heading(str(stats.get('avg_quality',0))))),
            , spacing='4'),
            rx.box(rx.text('Recent reviews'), rx.vstack(*[
                rx.card(rx.vstack(
                    rx.hstack(rx.text(f"{r['location']} — {r['created_at'][:19]}"), rx.spacer(), rx.text(f"Score: {AppState.compute_score(r['hours'], r['quality'], r['rating'])}")),
                    rx.text(r['comment'] or '—'),
                ), padding='2') for r in reviews[:10]
            ])),
            rx.box(rx.text('Hours (last items)'), simple_svg_bar_chart(hours_values))
        , padding='4', spacing='4'),
        padding='4'
    )
