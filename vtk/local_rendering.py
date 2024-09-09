from trame.app import get_server
from trame.widgets import vuetify3 as v3, vtk as vtk_widgets
from trame.ui.vuetify3 import SinglePageLayout
import vtk

server = get_server()
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

with SinglePageLayout(server, full_height=True) as layout:
    layout.icon.click = ctrl.view_reset_camera
    layout.title.set_text("VTK Local Rendering")

    with layout.toolbar:
        v3.VSpacer()
        v3.VSlider(
            v_model=("resolution", DEFAULT_RESOLUTION),
            min=3, max=60, step=1,
            hide_details=True, style="max-width: 300px",
        )
        v3.VDivider(vertical=True, classes="mx-2")
        v3.VBtn(icon="mdi-undo-variant", click=reset_resolution)

    with layout.content:
        with v3.VContainer(fluid=True, classes="pa-0 fill-height"):
            view = vtk_widgets.VtkLocalView(render_window)
            ctrl.view_update = view.update
            ctrl.view_reset_camera = view.reset_camera

server.start()
