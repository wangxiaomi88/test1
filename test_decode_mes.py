def decode_mes(mes):
    legal = False

    if mes=="OFFLINE":
        legal = True
        return legal, "OFFLINE", ""


    if mes.find("COMM") == 0:
        legal = True
        return legal, "COMM", mes[5:]

    if mes.find("ONLINEID") == 0:
        legal = True

        index = []
        index.append(mes.find("["))
        count = -1
        content = []
        for s in mes:
            count += 1
            if s == "," or s=="]":
                index.append(count)

                if len(index) > 1:
                    content.append(int(mes[index[-2]+1:index[-1]]))
            elif s=="_":
                break

        return legal, "ONLINE", content




if __name__ == "__main__":
    online_id_list = [1, 2, 3, 4]
    online_name_list = ["kk", "gh", "fg", "df"]
    mes = "ONLINEID:" + str(online_id_list) + "_" + "ONLINENAME:" + str(online_name_list)

    print(mes)

    legal, kind, content = decode_mes(mes)
    print(content)
