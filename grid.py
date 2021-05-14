class generate:

    def __init__(self, valid, china):
        d = {"A": (20, 500), "B": (520, 20), "C": (520, 520), "D": (520, 1100), "E": (1100, 20), "F": (1100, 520),
            "G": (1100, 1120), "H": (1400, 450), "I": (1800, 20), "J": (1800, 1120), "K": (2300, 450)}

        self.greens = [d[x] for x in valid]
        self.reds = [d[x] for x in china]
        print(self.reds)



    def generate_image(self):
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        cost_size = 40
        padding = 10
        width = 6
        height = 3

        img = Image.open("assets/images/grid_with_letters.png")
        red = Image.open("assets/images/red.png").resize((cell_size, cell_size))
        green = Image.open("assets/images/green.png").resize((cell_size, cell_size))


        img1 = img.copy()

        for i, j in self.reds:
            img1.paste(red, (i, j))

        for i, j in self.greens:
            img1.paste(green, (i, j))
        img1.save("static/result/temp.png")

        # return img1
