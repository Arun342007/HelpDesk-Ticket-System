import app as helpdesk

def test_raise_page():
    assert helpdesk.app.test_client().get("/raise").status_code == 200

def test_display_page():
    assert helpdesk.app.test_client().get("/tickets").status_code == 200

def test_resolve_page():
    assert helpdesk.app.test_client().get("/resolve").status_code == 200
