class Option:
    def __init__(self, index="", name="", defineName="", valueDefine=""):
        self.index = index
        self.name = name
        self.defineName = defineName
        self.valueDefine = valueDefine


class Feature:
    def __init__(self, index='', name="", options=[]):
        self.index = index
        self.options = options
        self.name = name

    def appendOption(self, option):
        self.options.append(option)

    def getOptionByName(self, oname):
        for o in self.options:
            if o.name == oname:
                return o
        return None


text = open("template.txt", "r").read()
indexC = 65
indexN = -1
KEY = "HITSPV200AUTO"
version = ""
features = []
lines = text.split('\n')

for line in lines:
    words = line.split(" ")
    if "Version:" in line:
        version = words[2]
    elif str(chr(indexC) + ":") in line:
        nameF = ""
        for w in words:
            nameF += w + " "
        features.append(Feature(chr(indexC), nameF.strip(), []))
        indexC += 1
        indexN += 1
    elif line.startswith("///*"):
        index = words[0].replace('/', '').replace('*', '')
        oname = words[1].strip()
        defineName = words[3].strip()
        valueDefine = ""
        if len(words) >= 5:
            valueDefine = words[4].strip()
        features[indexN].appendOption(Option(index, oname, defineName, valueDefine))
    else:
        pass


def create_file(selected, name):
    isNewFeature = True
    indexN = 0
    text = ""

    for line in lines:
        if line.startswith("///*"):
            if isNewFeature:
                words = line.split(" ")

                op = features[indexN].getOptionByName(words[1])
                if op is not None and op.index == selected[indexN]:
                    if op.valueDefine == "":
                        text += "/*" + op.index + "*/" + " `define " + op.defineName + "\n"
                    else:
                        text += "/*" + op.index + "*/" + " `define " + op.defineName + " " + op.valueDefine + "\n"
                    indexN += 1
                    isNewFeature = False
        elif KEY in line:
            text += "// HITSPV200AUTO" + version
            counter = 0
            for f in features:
                text += f.index + "" + selected[counter]
                counter += 1
            text += '\n'
        else:
            text += line
            isNewFeature = True
            text += '\n'

    f = open(name+".txt", "a")
    f.write(text)


def rec(n, output):
    if n == len(features):
        create_file(output.split("_"), name=output)
    else:
        for o in features[n].options:
            if output == "":
                rec_output = str(o.index)
            else:
                rec_output = output + "_" + str(o.index)
            rec(n + 1, rec_output)


rec(0, "")
