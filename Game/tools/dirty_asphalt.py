"""Add reproducible oil, damp patches and worn grit to the courtyard asphalt."""
from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFilter

path = Path(__file__).resolve().parents[1] / "assets/textures/asphalt.png"
image = Image.open(path).convert("RGB")
w, h = image.size
rng = random.Random(1717)
overlay = Image.new("RGBA", (w, h))
draw = ImageDraw.Draw(overlay)
for _ in range(22):
    x, y = rng.randrange(w), rng.randrange(h)
    rx, ry = rng.randrange(18, 62), rng.randrange(9, 35)
    draw.ellipse((x-rx, y-ry, x+rx, y+ry), fill=(15, 21, 24, rng.randrange(24, 66)))
overlay = overlay.filter(ImageFilter.GaussianBlur(13))
image = Image.alpha_composite(image.convert("RGBA"), overlay)
draw = ImageDraw.Draw(image)
for _ in range(1150):
    x, y = rng.randrange(w), rng.randrange(h)
    d = rng.choice([1, 1, 2, 3])
    draw.line((x, y, x+d, y+rng.randrange(-1, 2)), fill=(25, 29, 30, rng.randrange(18, 55)))
image.convert("RGB").save(path)
