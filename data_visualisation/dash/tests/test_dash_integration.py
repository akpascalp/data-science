from dash_application import app
import dash.testing.application_runners as app_runner

def test_dash_app(dash_duo):
    app.layout = app_runner.AppRunner(app).start()
    dash_duo.start_server(app)

    # Test if the app is loaded correctly
    dash_duo.wait_for_element("#dropdown-statistics", timeout=10)
    assert dash_duo.find_element("#dropdown-statistics").get_attribute("value") == "Select Statistics"

    # Test selecting a statistic
    dash_duo.select_dcc_dropdown("#dropdown-statistics", "Yearly Statistics")
    dash_duo.wait_for_text_to_equal("#output-container", "Yearly Statistics", timeout=10)

    # Test selecting a year
    dash_duo.select_dcc_dropdown("#select-year", "2020")
    dash_duo.wait_for_text_to_equal("#output-container", "2020", timeout=10)
