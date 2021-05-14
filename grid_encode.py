class generate:
    def __init__(self):
        self.d = {"A": (20, 500), "B": (520, 20), "C": (520, 520), "D": (520, 1100), "E": (1100, 20), "F": (1100, 520),
            "G": (1100, 1120), "H": (1400, 450), "I": (1800, 20), "J": (1800, 1120), "K": (2300, 450)}


    def generate_image(self, x):
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        cost_size = 40
        padding = 10
        width = 10
        height = 5

        img = Image.open("assets/images/grid_with_letters.png").resize((width * cell_size, height * cell_size))
        red = Image.open("assets/images/red.png").resize((cell_size, cell_size))
        green = Image.open("assets/images/green.png").resize((cell_size, cell_size))
        black = Image.open("assets/images/black.png")


        img1 = Image.new(
            "RGBA",
            (width * cell_size,
             height * cell_size + cost_size + padding * 2),
            "black"
        )

        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 18)
        draw = ImageDraw.Draw(img1)

        #for i, j in self.reds:
            #img1.paste(red, (i, j))

        #for i, j in self.greens:
            #img1.paste(green, (i, j))

        # Add cost
        draw.rectangle(
            (0, height * cell_size, width * cell_size,
             height * cell_size + cost_size + padding * 2),
            "black"
        )

        draw.text(
            (padding, height * cell_size + padding),
            f"{x}",
            fill="white",
            font=font
        )

        img1.paste(img)

        img1.save("static/result/encode.png")
