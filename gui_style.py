from ttkbootstrap import Style

def apply_style(app):
    style = Style("vapor")
    app.configure(background=style.colors.bg)

    return style
