from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGBA', (50, 50), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

draw.ellipse([5, 5, 45, 45], outline='red', width=2)
draw.ellipse([10, 10, 40, 40], outline='red', width=1)

draw.text((25, 25), "章", fill='red', anchor='mm')

img.save('stamp.png')
print("Created: stamp.png")
