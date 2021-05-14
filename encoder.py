class message_encoder:

    def __init__(self):
        None

    def arrange(self, k):
        b = ""
        for i in sorted(k):
            b += i
        # k, b = b, k
        d = {}
        for i in range(len(k)):
            if k[i] not in d.keys():
                d[k[i]] = [i]
            else:
                d[k[i]].append(i)
        ret = []
        for i in b:
            ret.append(d[i][0])
            d[i].pop(0)
        return ret

    def encode_message(self ,x, key):
        ret_list = ["Encoded message is: "]
        ret = ""
        ctr = 0
        rows = len(x) / len(key)
        # ind = arrange(key)
        x = list(x)
        final = []
        if len(x) % rows != 0:
            rows = rows + 1

        rows = int(rows)

        for i in range(rows):
            temp = []
            for j in range(len(key)):
                try:
                    temp.append(x[ctr])
                    ctr += 1
                except:
                    temp.append("_")
            final.append(temp)

        key = self.arrange(key)
        for i in key:
            for c in final:
                t = key.index(i)
                ret += c[i]

        ret_list.append(ret)

        from grid_encode import generate

        gen = generate()

        gen.generate_image(ret)

        return ret_list
