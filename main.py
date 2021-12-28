import src

from src.syllabification_rules import (
    ortho_to_CV, sampa_to_CV, get_split_sampa,
    separator_character
    )


# about 5 words in the input have two possible pronunciations
# these possible pronunciations are separated by a special character
# we only work with the first pronunciation
multiple_pronunciation_character = ";"

#reading the input file
with open("./input/Input.txt") as input_file:
    lines = input_file.readlines()

    def create_output_line(input_line):
        # returns a string with the format required for the output file 
        [ortho, sampa] = input_line.split()
        sampa = (sampa.split(multiple_pronunciation_character))[0] #only work with 1st pronunciation
        ortho_cv = ortho_to_CV(ortho)
        sampa_cv = sampa_to_CV(sampa)
        split_sampa, split_cv = get_split_sampa(sampa)
        return " ".join([ortho, ortho_cv, sampa, sampa_cv, split_sampa, split_cv, "\n"])

    result = map(create_output_line, lines)

    result = list(result)


#writing the output file
with open("./output/Output.txt", "w"): #delete any previous output file
    pass

with open("./output/Output.txt",'a') as output_file:
    output_file.writelines(result)
    
     


####
#Analysis of the results
####

with open("./input/Input.txt") as input_file:
    #we want two lists:
    # one of only sampa syllables
    # one of only CV syllables
    
    lines = input_file.readlines()
    sampas = map(lambda line: line.split()[1], lines)

    sampas = map(lambda st: (st.split(multiple_pronunciation_character))[0], sampas)    #only work with 1st pronunciation

    # split into syllables
    syllables = map(get_split_sampa, sampas)
    syllables = list(syllables)

    # first column is words split by syllables in sampa, second in CV-form
    sampa_split = [elem[0] for elem in syllables]
    cv_split = [elem[1] for elem in syllables]

    # get flattened lists
    sampa_syllables = []
    for sampa_split_word in sampa_split:
        sampa_syllables += sampa_split_word.split(separator_character)

    cv_syllables = []
    for cv_split_word in cv_split:
        cv_syllables += cv_split_word.split(separator_character)


### frequency analysis


def sort_dictionary_descending(dictionary):
    #return the dicitonary in descending order by value
    new_dict = {}
    for elem in  sorted(dictionary, key = dictionary.get, reverse=True):
        new_dict[elem] = dictionary[elem]
    return new_dict


def count_frequencies(my_list):
    #return a dicitonary where the keys are the elements of  my_list 
    # and the values their frequency in my_list

    res = {}
    for item in my_list:
        if item in res:
            res[item] += 1
        else:
            res[item] = 1
    
    res = sort_dictionary_descending(res)
    return res

def get_n_first(dictionary, n):
    # get the n first key, value pairs of the dictionary
    res = {}
    count = 0
    while count < n and count < len(dictionary):
        key = list(dictionary.keys())[count]
        res[key] = dictionary[key]
        count += 1
    return res

### writing analysis result to a file

with open("./output/Frequency_analysis.txt", "w"): #delete any previous output file
    pass

# write cv frequencies to file
cv_frequencies = count_frequencies(cv_syllables)

with open("./output/Frequency_analysis.txt",'a') as output_file:
    output_file.write("Consonant-Vowel Syllables Top Frequencies\n")
    for key, value in cv_frequencies.items():
        output_file.write(" ".join(["|", str(key), "|", str(value), "\n"]) )
    
    output_file.write("\n")


#write top macro-class frequencies to file

from src.syllabification_rules import syllable_to_macroclass
macroclass_syllables = list(map(syllable_to_macroclass, sampa_syllables) )

macroclass_frequencies = get_n_first(count_frequencies(macroclass_syllables), 15)


with open("./output/Frequency_analysis.txt",'a') as output_file:
    output_file.write("Macroclass Syllables Top Frequencies\n")
    for key, value in macroclass_frequencies.items():
        output_file.write(" ".join(["|", str(key), "|", str(value), "\n"]) )
    output_file.write("\n")





#write top sampa frequencies to file
sampa_top_frequencies = get_n_first(count_frequencies(sampa_syllables), 15)

with open("./output/Frequency_analysis.txt",'a') as output_file:
    output_file.write("Sampa Syllables Top Frequencies\n")
    for key, value in sampa_top_frequencies.items():
        output_file.write(" ".join(["|", str(key), "|", str(value), "\n"]) )
    output_file.write("\n")


print(cv_frequencies)
print(macroclass_frequencies)
print(sampa_top_frequencies)