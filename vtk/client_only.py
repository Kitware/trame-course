from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3, vtk as vtk_widgets

server = get_server()
state, ctrl = server.state, server.controller

with SinglePageLayout(server, full_height=True) as layout:
    with layout.content:
        with v3.VContainer(fluid=True, classes="pa-0 fill-height"):
            with vtk_widgets.VtkView() as view:
                ctrl.view_reset_camera = view.reset_camera
                with vtk_widgets.VtkGeometryRepresentation():
                    vtk_widgets.VtkAlgorithm(
                        vtk_class="vtkConeSource",
                        state=("{ resolution }",),
                    )

    with layout.toolbar:
        v3.VSpacer()
        v3.VSlider(
            v_model=("resolution", 6),
            min=3,
            max=60,
            step=1,
            hide_details=True,
            style="max-width: 300px;",
        )
        v3.VBtn(icon="mdi-crop-free", click=ctrl.view_reset_camera)

server.start()
