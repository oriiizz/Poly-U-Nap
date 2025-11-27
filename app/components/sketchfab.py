import reflex as rx
from typing import Optional

def sketchfab_model(model_id: str, height: str = "360px", title: Optional[str] = None):
    """
    Returns an rx.html containing a Sketchfab iframe.
    - model_id: the Sketchfab model id (the part in the URL after /models/)
    - height: CSS height (e.g. "360px" or "50vh")
    """
    # Handle the title properly for reactive variables
    if isinstance(title, rx.Var):
        # If title is a Var, we need to handle it differently
        # We'll use a conditional approach in the component
        return rx.cond(
            title,
            rx.html(
                f"""
                <div style="width:100%; position:relative; padding-bottom:56.25%; height:0; overflow:hidden;">
                  <iframe
                    title="{{title.to(str)}}"
                    src="https://sketchfab.com/models/{model_id}/embed"
                    frameborder="0"
                    allow="autoplay; fullscreen; xr-spatial-tracking"
                    allowfullscreen
                    loading="lazy"
                    style="position:absolute; top:0; left:0; width:100%; height:100%; background: transparent; border: none;">
                  </iframe>
                </div>
                """
            ),
            rx.html(
                f"""
                <div style="width:100%; position:relative; padding-bottom:56.25%; height:0; overflow:hidden;">
                  <iframe
                    title="Sketchfab Model"
                    src="https://sketchfab.com/models/{model_id}/embed"
                    frameborder="0"
                    allow="autoplay; fullscreen; xr-spatial-tracking"
                    allowfullscreen
                    loading="lazy"
                    style="position:absolute; top:0; left:0; width:100%; height:100%;">
                  </iframe>
                </div>
                """
            )
        )
    else:
        # For static titles
        title_attr = title or f"Sketchfab {model_id}"
        return rx.html(
            f"""
            <div style="width:100%; position:relative; padding-bottom:56.25%; height:0; overflow:hidden;">
              <iframe
                title="{title_attr}"
                src="https://sketchfab.com/models/{model_id}/embed"
                frameborder="0"
                allow="autoplay; fullscreen; xr-spatial-tracking"
                allowfullscreen
                loading="lazy"
                style="position:absolute; top:0; left:0; width:100%; height:100%;">
              </iframe>
            </div>
            """
        )