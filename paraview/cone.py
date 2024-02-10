import paraview.web.venv

from trame.app import get_server
from trame.widgets import vuetify, paraview
from trame.ui.vuetify import SinglePageLayout
from trame.decorators import TrameApp, change

from paraview import simple


@TrameApp()
class Cone:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue2")
        self.cone = simple.Cone()
        self.representation = simple.Show(self.cone)
        self.view = simple.Render()
        self.state.trame__title = "ParaView cone"
        self.ui = self._build_ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @change("resolution")
    def on_resolution_change(self, resolution, **kwargs):
        self.cone.Resolution = resolution
        self.ctrl.view_update()

    def reset_resolution(self):
        self.state.resolution = 6

    def _build_ui(self):
        with SinglePageLayout(self.server) as layout:
            layout.icon.click = self.ctrl.view_reset_camera
            layout.title.set_text("Cone Application")

            with layout.toolbar:
                vuetify.VSpacer()
                vuetify.VSlider(
                    v_model=("resolution", 6),
                    min=3,
                    max=60,
                    step=1,
                    hide_details=True,
                    dense=True,
                    style="max-width: 300px",
                )
                vuetify.VDivider(vertical=True, classes="mx-2")
                with vuetify.VBtn(icon=True, click=self.reset_resolution):
                    vuetify.VIcon("mdi-undo-variant")

            with layout.content:
                with vuetify.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                ):
                    html_view = paraview.VtkRemoteView(self.view)
                    # html_view = paraview.VtkLocalView(self.view)
                    self.ctrl.view_update = html_view.update
                    self.ctrl.view_reset_camera = html_view.reset_camera


def main():
    app = Cone()
    app.server.start()


if __name__ == "__main__":
    main()
