# %%
import dash_bootstrap_components as dbc
from dash import html

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# make a reuseable navitem for the different examples
nav_item_bird = dbc.NavItem(dbc.NavLink("Bird", href="/bird"))
nav_item_recent = dbc.NavItem(dbc.NavLink("Recent", href="/recent"))

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Select location", href='map'),
        dbc.DropdownMenuItem("Recent spots", href='recent'),
        dbc.DropdownMenuItem("Bird details", href='bird'),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
)

search = dbc.Row(
    [
        dbc.Col(
            dbc.Input(id="search", type="search", placeholder="Bird name")
        ),
        dbc.Col(
            dbc.Button(
                "Search", id="search_button", color="primary", className="ms-2"
            ),
            # set width of button column to auto to allow
            # search box to take up remaining space.
            width="auto",
        ),
    ],
    # add a top margin to make things look nice when the navbar
    # isn't expanded (mt-3) remove the margin on medium or
    # larger screens (mt-md-0) when the navbar is expanded.
    # keep button and search box on same row (flex-nowrap).
    # align everything on the right with left margin (ms-auto).
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

# this example that adds a logo to the navbar brand
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Birdies", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="logo-navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    # search, nav_item_bird, nav_item_recent, 
                    [dropdown],
                    className="ms-auto",
                    navbar=True,
                ),
                id="logo-navbar-collapse",
                navbar=True,
            ),
        ],
    ),
    color="dark",
    dark=True,
    className="mb-5",
)
