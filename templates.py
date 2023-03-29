# srcs/streamlit_app/templates.py
import urllib.parse

def number_of_results(total_hits: int, duration: float) -> str:
    """ HTML scripts to display number of results and duration. """
    return f"""
        <div style="color:grey;font-size:95%;">
            {total_hits} results ({duration:.2f} seconds)
        </div><br>
    """

def subheader(text):
    return f"""
    <div style="margin-top: 5px; margin-bottom: 0px;">
        <h4>{text}</h4>
    </div>
    """

def answer(answer_text):
    return f"""
    <div class="card" style="margin-top: 5px; margin-bottom: 10px;">
        <div class="card-body">
            <p class="card-text">{answer_text}</p>
        </div>
    </div>
    """


def card(title, context):
    return f"""
    <div class="card" style="margin-top: 5px; margin-bottom: 5px;">
        <div class="card-body">
            <h5 class="card-title">{title}</h5>
            <p class="card-text">{context}</p>
        </div>
    </div>
    """


