from trame.app import get_server
from trame.widgets import html
from trame.ui.html import DivLayout

# ---------------------------------------------------------
# Trame setup
# ---------------------------------------------------------

server = get_server()
state = server.state

# ---------------------------------------------------------
# ViewModel
# ---------------------------------------------------------

# Read/Write
state.a = 1
state["b"] = state.a + 2
print(state.b == state["b"])


# Reactivity
@state.change("a", "b")
def on_change(a, b, **kwargs):
    print(f"Something has changed {a=} or {b=}")


@state.change("a")
def on_a_change(a, **kwargs):
    print(f"a changed to {a}")


# ---------------------------------------------------------
# Model
# ---------------------------------------------------------


def reset_a():
    state.a = 10


# ---------------------------------------------------------
# View
# ---------------------------------------------------------

with DivLayout(server):
    html.Div("a={{ a }} and b={{ b }}")
    html.Input(type="range", min=0, max=100, step=1, v_model="a")
    html.Input(type="range", min=0, max=50, step=2, v_model="b")
    html.Button("Reset", click=reset_a)
    with html.Ul():
        html.Li("List item {{ i }}", v_for="i in Number(a)", key="i")

# ---------------------------------------------------------
# Trame start application
# ---------------------------------------------------------
server.start()
