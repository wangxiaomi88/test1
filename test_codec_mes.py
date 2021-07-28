def encode_mes(kind, content="", source=-1, target=-2):
    if kind == "OFFLINE":
        return str(source)+"#OFFLINE:"+ str(content)

    if kind == "CHATCLOSE":
        return "{}#CHATCLOSE>{}".format(str(source), str(target))

    if kind == "FRIENDS":
        mes = str(source) + "#FRIENDS:" + str(content)
        return mes

    if kind == "ONLINE":
        mes = "ONLINEID:" + str(content)
        return mes

    if kind=="IDLEAVE":
        mes = "IDLEAVE:" + str(content)
        return mes


    if kind == "COMM":
        return "{}#COMM>{}:{}".format(str(source), str(target), content)


def decode_mes(mes):
    legal = False
    source = -1
    target = -2

    try:

        if mes.find("OFFLINE")>=0:
            legal = True
            s0 = mes.find("#")
            source = int(mes[0:s0])

            index = []
            index.append(mes.find("["))
            count = -1
            content = []
            for s in mes:
                count += 1
                if s == "," or s == "]":
                    index.append(count)

                    if len(index) > 1:
                        content.append(int(mes[index[-2] + 1:index[-1]]))

            return legal, "OFFLINE", source, target, content

        if mes.find("CHATCLOSE") >= 0:
            legal = True
            s0 = mes.find("#")
            s1 = mes.find(">")

            source = int(mes[0:s0])
            target = int(mes[s1 + 1:])
            return legal, "CHATCLOSE", source, target, ""

        if mes.find("COMM") > 0:
            legal = True

            s0 = mes.find("#")
            s1 = mes.find(">")
            s2 = mes.find(":")
            source = int(mes[0:s0])
            target = int(mes[s1 + 1:s2])
            return legal, "COMM", source, target, mes[s2 + 1:]

        if mes.find("FRIENDS") > 0:
            legal = True

            s1 = mes.find("#")

            source = int(mes[:s1])
            index = []
            index.append(mes.find("["))
            count = -1
            content = []
            for s in mes:
                count += 1
                if s == "," or s == "]":
                    index.append(count)

                    if len(index) > 1:
                        content.append(int(mes[index[-2] + 1:index[-1]]))
                elif s == "_":
                    break

            return legal, "FRIENDS", source, target, content


        if mes.find("IDLEAVE") == 0:
            legal = True

            index = []
            index.append(mes.find("["))
            count = -1
            content = []
            for s in mes:
                count += 1
                if s == "," or s == "]":
                    index.append(count)

                    if len(index) > 1:
                        content.append(int(mes[index[-2] + 1:index[-1]]))
                elif s == "_":
                    break

            return legal, "IDLEAVE", source, target, content




        if mes.find("ONLINEID") == 0:
            legal = True

            index = []
            index.append(mes.find("["))
            count = -1
            content = []
            for s in mes:
                count += 1
                if s == "," or s == "]":
                    index.append(count)

                    if len(index) > 1:
                        content.append(int(mes[index[-2] + 1:index[-1]]))
                elif s == "_":
                    break

            return legal, "ONLINE", source, target, content

    except:
        return legal, "ILLEGALE", source, target, ""
    else:
        return legal, "ILLEGALE", source, target, ""


if __name__ == "__main__":
    online_id_list = [10, 20, 30, 45]
    online_name_list = ["kk", "gh", "fg", "df"]
    mes = "ONLINEID:" + str(online_id_list) + "_" + "ONLINENAME:" + str(online_name_list)

    mes2 = "123#COMM>228:hahaha"
    mes3 = "adsf"

    mes4 = "12#CHATCLOSE>45"

    legal, kind, source, target, content = decode_mes(mes)
    print(content)

    legal, kind, source, target, content = decode_mes(mes2)
    print(content)
    print(source, target)

    legal, kind, source, target, content = decode_mes(mes3)
    print(legal, kind)
    print(source, target)

    legal, kind, source, target, content = decode_mes(mes4)
    print(legal, kind)
    print(source, target)
