import flet as ft
from flet_route import Routing, path
from View.main_view import MainPage

class Router:
    def __init__(self, page: ft.Page):
        self.app_routes = [
            path(url='/', clear=True, view=MainPage().view),

        ]
        self.page = page

        Routing(
            page=self.page,
            app_routes=self.app_routes,
        )
        self.page.go(self.page.route)
