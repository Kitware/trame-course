from trame.app import get_server
from trame.widgets import vuetify, vtk as vtk_widgets
from trame.ui.vuetify import SinglePageLayout
import vtk

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

DEFAULT_RESOLUTION = 6


def create_vtk_pipeline():
    renderer, render_window = vtk.vtkRenderer(), vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    render_window_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

    cone, mapper, actor = vtk.vtkConeSource(), vtk.vtkPolyDataMapper(), vtk.vtkActor()

    mapper.SetInputConnection(cone.GetOutputPort())
    actor.SetMapper(mapper)
    renderer.AddActor(actor)
    renderer.ResetCamera()
    render_window.Render()

    return render_window, cone


render_window, cone = create_vtk_pipeline()


@state.change("resolution")
def update_resolution(resolution=DEFAULT_RESOLUTION, **kwargs):
    cone.SetResolution(resolution)
    ctrl.view_update()


def reset_resolution():
    state.resolution = DEFAULT_RESOLUTION


with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.view_reset_camera
    layout.title.set_text("VTK Remote Rendering")

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSlider(
            v_model=("resolution", DEFAULT_RESOLUTION),
            min=3,
            max=60,
            step=1,
            hide_details=True,
            dense=True,
            style="max-width: 300px",
        )
        vuetify.VDivider(vertical=True, classes="mx-2")
        with vuetify.VBtn(icon=True, click=reset_resolution):
            vuetify.VIcon("mdi-undo-variant")

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            view = vtk_widgets.VtkRemoteView(render_window)
            ctrl.view_update = view.update
            ctrl.view_reset_camera = view.reset_camera

server.start()
