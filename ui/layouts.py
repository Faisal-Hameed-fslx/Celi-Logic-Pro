"""
Cel-Logic Pro — Layout Helpers
Reusable draw helpers for panel consistency.
"""


def draw_section(layout, label, icon='NONE'):
    """Draw a collapsible section header and return the column."""
    box = layout.box()
    row = box.row()
    row.label(text=label, icon=icon)
    col = box.column(align=True)
    return col


def draw_prop_row(layout, data, prop, text="", icon='NONE', factor=0.4):
    """Draw a labelled property row with fixed label width."""
    row = layout.row(align=True)
    split = row.split(factor=factor)
    split.label(text=text or prop.replace("_", " ").title(), icon=icon)
    split.prop(data, prop, text="")
    return row


def draw_operator_row(layout, op_idname, text, icon='NONE'):
    """Draw a centred operator button."""
    row = layout.row(align=True)
    row.operator(op_idname, text=text, icon=icon)
    return row
