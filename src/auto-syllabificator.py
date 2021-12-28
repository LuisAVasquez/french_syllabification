
def determine_articulation(path="../"):
    pairs = list()
    with open(path + "input/Input.txt", encoding="utf-8") as artxt:
        lines = artxt.readlines()
        for line in lines:
            if len(line) > 0:
                pairs.append([line.split()[0].strip(), [line.split()[1].strip()]])
    return pairs


def read_ortho_rules(path="../"):
    orthos = set()
    with open(path + "input/Code.txt", encoding="utf-8") as codetxt:
        lines = codetxt.readlines()
        for line in lines:
            if line != "Ortho" and len(line) > 0:
                orthos.add(line)
            if line == "Phonetique":
                break
    return orthos


def get_ortho_rules(orthos):
    rules = dict()
    for ortho in orthos:
        try:
            lvl1 = ortho.split(" - ")
            lvl2 = lvl1[0].split(" ")
            tmp_letter = lvl2[0].strip()
            tmp_apr = lvl2[1].strip()
            tmp_form = "C" if lvl1[1].strip() == "consonant" else "V"
            rules[tmp_letter] = {"appearance": tmp_apr, "form": tmp_form}
        except:
            continue
    return rules


def read_phonetic_rules(path="../"):
    phonetics = set()
    with open(path + "input/Code.txt", encoding="utf-8") as codetxt:
        lines = codetxt.readlines()
        ptflag = False
        for line in lines:
            if line.strip() == "Phonetique":
                ptflag = True
                continue
            if ptflag and len(line) > 0:
                phonetics.add(line)
    return phonetics


def get_phonetic_rules(phonetics):
    rules = dict()
    for phonetic in phonetics:
        try:
            lvl1 = phonetic.split(" - ")
            lvl2 = lvl1[0].split(" ")
            tmp_letter = lvl2[0].strip()
            tmp_apr = lvl2[1].strip()
            tmp_form = "C" if lvl1[1].strip() == "consonant" \
                else "V" if lvl1[1].strip() == "vowel" \
                else "S" if lvl1[1].strip() == "semi-vowel" \
                else "-"
            try:
                tmp_macro = lvl1[2].strip()
            except:
                tmp_macro = ""
            rules[tmp_letter] = {"appearance": tmp_apr, "form": tmp_form, "macro": tmp_macro}
        except:
            continue
    return rules


def determine_form(victim, rules):
    output = ""
    for char in victim.lower():
        output += rules[char]["form"]
    return output


def get_segmentation_form(articulation):
    parts = []
    phonetic_rules = get_phonetic_rules(read_phonetic_rules())
    rule_1 = "VV"
    rule_2 = "VCV"
    rule_3 = "VCCV"
    rule_4 = "VCCCV"
    form = determine_form(articulation, phonetic_rules)

    pass


print(determine_form("abaise", get_ortho_rules(read_ortho_rules())))
print(determine_form("e@Uj", get_phonetic_rules(read_phonetic_rules())))
