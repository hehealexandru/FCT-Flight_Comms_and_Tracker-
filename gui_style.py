from ttkbootstrap import Style

def apply_style(app):
    style = Style("litera")
    app.configure(background=style.colors.bg)

    return style
