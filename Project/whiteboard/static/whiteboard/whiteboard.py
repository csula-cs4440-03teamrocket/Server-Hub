from pyscript import when, window, document
from pyodide.ffi import to_js, create_proxy
from js import Image

canvas = document.getElementById("board")
ctx = canvas.getContext("2d")

state = {
    "color": "black",
    "width": 5,
    "drawing": False,
    "x": 0,
    "y": 0,
    "eraser": False,
    "image": None,
}

COLORS = ["black", "gray", "brown", "red", "orange", "yellow", "green", "blue", "purple"]

#Canvas Setup
def reset_canvas():
    ctx.fillStyle = "white"
    ctx.fillRect(0, 0, canvas.width, canvas.height)

reset_canvas()
ctx.lineCap = "round"
ctx.lineJoin = "round"

#Color Palette
palette = document.getElementById("palette")
colorsChosen = []

for color in COLORS:
    btn = document.createElement("button")
    btn.className = "colorChosen"
    btn.style.background = color
    btn.dataset.color = color
    palette.appendChild(btn)
    colorsChosen.append(btn)

def set_color(color):
    state["color"] = color
    state["eraser"] = False
    for c in colorsChosen:
        c.classList.toggle("active", c.dataset.color == color)

@when("click", ".colorChosen")
def pick_colorChosen(event):
    set_color(event.currentTarget.dataset.color)

#Drawing
@when("pointerdown", "#board")
def pointer_down(event):
    if state["image"] is not None:
        img = state["image"]
        ctx.drawImage(img, event.offsetX - img.width / 2, event.offsetY - img.height / 2)
        state["image"] = None
        canvas.style.cursor = "crosshair"
        return
    state["drawing"] = True
    state["x"] = event.offsetX
    state["y"] = event.offsetY
    canvas.setPointerCapture(event.pointerId)

@when("pointermove", "#board")
def pointermove(event):
    if not state["drawing"]:
        return
    ctx.strokeStyle = "white" if state["eraser"] else state["color"]
    ctx.lineWidth = state["width"] * (2 if state["eraser"] else 1)
    ctx.beginPath()
    ctx.moveTo(state["x"], state["y"])
    ctx.lineTo(event.offsetX, event.offsetY)
    ctx.stroke()
    state["x"] = event.offsetX
    state["y"] = event.offsetY

@when("pointerup", "#board")
def pointerup(event):
    state["drawing"] = False

#Stroke Size Slider
@when("input", "#size")
def input_size(event):
    state["width"] = float(event.target.value)
    document.getElementById("size-label").innerText = event.target.value

#Buttons
@when("click", "#eraser")
def eraser(event):
    state["eraser"] = True
    for c in colorsChosen:
        c.classList.remove("active")

@when("click", "#clear")
def clear(event):
    reset_canvas()

#Inserting Image
@when("click", "#insert-image")
def open_dialog(event):
    document.getElementById("file").click()

@when("change", "#file")
def file_chosen(event):
    file_input = event.target
    file = file_input.files.item(0)
    if file is None:
        return
    img = Image.new()

    def load(e):
        state["image"] = img
        canvas.style.cursor = "copy"

    img.onload = create_proxy(load)
    img.src = window.URL.createObjectURL(file)
    file_input.value = ""

