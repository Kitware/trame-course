from trame.widgets import vuetify


def handle_item(action, item):
    print(action, item)

with vuetify.VDataTable():
    with vuetify.Template(
        slot_actions="{ item }",
        __properties=[
            ("slot_actions", "v-slot:item.actions"),
        ],
    ):
        vuetify.VIcon(
            "mdi-pencil",
            small=True,
            click=(handle_item, "['edit', item]"),
        )
        vuetify.VIcon(
            "mdi-delete",
            small=True,
            click=(handle_item, "['delete', item]"),
        )
