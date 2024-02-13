from trame.app import get_server
from trame.decorators import TrameApp, change
from trame.widgets import vuetify, vtk as vtk_widgets
from trame.ui.vuetify import SinglePageLayout


@TrameApp()
class Cone:
    def __init__(self, server_name=None):
        self.server = get_server(server_name, client_type="vue2")
        self._layout = None
        self.ui  # Force ui creation

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @property
    def resolution(self):
        return self.state.resolution

    @resolution.setter
    def resolution(self, v):
        with self.state:
            self.state.resolution = v

    def reset_resolution(self):
        self.resolution = 6

    @property
    def ui(self):
        if self._layout is None:
            with SinglePageLayout(self.server) as layout:
                self._layout = layout

                layout.icon.click = self.ctrl.view_reset_camera
                layout.title.set_text("VTK Remote Rendering")

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
                    with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                        with vtk_widgets.VtkView(ref="view", background=("[0,0,0]",)):
                            with vtk_widgets.VtkGeometryRepresentation():
                                vtk_widgets.VtkAlgorithm(
                                    vtk_class="vtkConeSource", state=("{ resolution }",)
                                )

        return self._layout


def main():
    cone_app = Cone()
    cone_app.server.start()


if __name__ == "__main__":
    main()
