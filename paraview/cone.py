from trame.app import get_server
from trame.widgets import vuetify3 as v3, paraview
from trame.ui.vuetify3 import SinglePageLayout
from trame.decorators import TrameApp, change

from paraview import simple


@TrameApp()
class Cone:
    def __init__(self, server=None):
        self.server = get_server(server)

        self.cone = simple.Cone()
        self.representation = simple.Show(self.cone)
        self.view = simple.Render()

        self._build_ui()

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
            self.ui = layout
            self.state.trame__title = "ParaView cone"

            layout.icon.click = self.ctrl.view_reset_camera
            layout.title.set_text("PV Cone")

            with layout.toolbar:
                v3.VSpacer()
                v3.VSlider(
                    v_model=("resolution", 6),
                    min=3, max=60, step=1,
                    hide_details=True, style="max-width: 300px",
                )
                v3.VDivider(vertical=True, classes="mx-2")
                v3.VBtn(icon="mdi-undo-variant", click=self.reset_resolution)

            with layout.content:
                with v3.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                ):
                    html_view = paraview.VtkRemoteView(
                        self.view, still_ratio=2, interactive_ratio=2
                    )
                    # html_view = paraview.VtkLocalView(self.view)
                    self.ctrl.view_update = html_view.update
                    self.ctrl.view_reset_camera = html_view.reset_camera

            return layout


def main():
    app = Cone()
    app.server.start()


if __name__ == "__main__":
    main()
