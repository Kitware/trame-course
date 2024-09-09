from trame.app import get_server
from trame.decorators import TrameApp, change
from trame.widgets import vuetify3 as v3, vtk as vtk_widgets
from trame.ui.vuetify3 import SinglePageLayout
import vtk


@TrameApp()
class Cone:
    def __init__(self, server=None):
        self.server = get_server(server)
        self._init_vtk()
        self._build_ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    def _init_vtk(self):
        renderer, render_window = vtk.vtkRenderer(), vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)

        render_window_interactor = vtk.vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(render_window)
        render_window_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        cone, mapper, actor = (
            vtk.vtkConeSource(),
            vtk.vtkPolyDataMapper(),
            vtk.vtkActor(),
        )

        mapper.SetInputConnection(cone.GetOutputPort())
        actor.SetMapper(mapper)
        renderer.AddActor(actor)
        renderer.ResetCamera()
        render_window.Render()

        self.render_window = render_window
        self.renderer = renderer
        self.actor = actor
        self.cone = cone

    @property
    def resolution(self):
        return self.state.resolution

    @resolution.setter
    def resolution(self, v):
        with self.state:
            self.state.resolution = v

    @change("resolution")
    def _on_resolution_change(self, resolution, **kwargs):
        self.cone.SetResolution(resolution)
        self.ctrl.view_update()

    def reset_resolution(self):
        self.resolution = 6

    def _build_ui(self):
        with SinglePageLayout(self.server, full_height=True) as layout:
            self.ui = layout

            layout.icon.click = self.ctrl.view_reset_camera
            layout.title.set_text("VTK Remote Rendering")

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
                with v3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    view = vtk_widgets.VtkRemoteView(
                        self.render_window, 
                        interactive_ratio=1,
                    )
                    self.ctrl.view_update = view.update
                    self.ctrl.view_reset_camera = view.reset_camera

def main():
    cone_app = Cone()
    cone_app.server.start()


if __name__ == "__main__":
    main()
