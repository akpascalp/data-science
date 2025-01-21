from dash_application import create_layout

def test_create_layout():
    layout = create_layout()
    assert layout is not None
    assert layout.children[0].children == "Automobile Sales Statistics Dashboard"
