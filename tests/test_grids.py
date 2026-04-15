import uicord

def test_create_griditem():
    assert len([
        uicord.GridItem(
            "Hi"
        ),
        uicord.GridItem(
            "Hello"
        ),
        uicord.GridItem(
            "Hey"
        ),
        uicord.GridItem(
            "Heyo"
        ),
    ])==4

def test_create_griditem_em():
    assert len([
        uicord.GridItem(
            "Hi", "👋"
        ),
        uicord.GridItem(
            "Hello", "👋"
        ),
        uicord.GridItem(
            "Hey", "👋"
        ),
        uicord.GridItem(
            "Heyo", "👋"
        ),
    ])==4

def test_grid_content():
    content = uicord.Grid(
        texts=[
            uicord.GridItem(
                "Hi", "👋"
            ),
            uicord.GridItem(
                "Hello"
            ),
            uicord.GridItem(
                "Hey", "👋"
            ),
            uicord.GridItem(
                "Heyo", "👋"
            )
        ]
    ).build()
    print(content)
    assert isinstance(
        content, uicord.Text
    )
