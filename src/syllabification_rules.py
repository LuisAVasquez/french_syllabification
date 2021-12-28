####
# Implmentation of syllabification rules
####

####
# Global variables and utilities
####

#French orthography
from os import error


ortho_consonants =  {'p', 't', 'k', 'b', 'd', 'g', 
                    'f', 's', 'c', 'v', 'z', 'j', 'm', 
                    'n', 'r', 'l', 'h'}

ortho_vowels = {'a', 'à', 'e', 'é', 'ê', 'ë', 
                'i', 'ï', 'î', 'o', 'u', 'y', 
                'ù', 'û', 'ù', 'ū', 'í', 'ī', 'ì', 
                'ô', 'ö', 'ò', 'œ', 'ō', 'ø', 
                'â', 'á', 'ä', 'æ', 'ã', 'ā', 
                'ÿ', 'è', 'ē'}


#SAMPA
phono_oral_vowels = {'a', 'e', 'i', 'u', 'o', 'y', 'E', '9', '2', 'O', '*'}
phono_nasal_vowels = {'@', '1', '5'}
phono_semi_vowels = {'w', 'j', '8'}
phono_plosives = {'p', 't', 'k', 'b', 'd', 'g'}
phono_fricatives = {'f', 's', 'S', 'v', 'z', 'Z'}
phono_liquids = {'R', 'l'}
phono_nasals = {'m', 'n', 'N', 'G'}


phono_vowels = phono_oral_vowels.union(phono_nasal_vowels)


#some global variables specific to this implementation

dummy_character = "+" #will be used to pad strings so that counters do not get out of range
separator_character = "-" #the character that will mark the division between syllables

## Utilities

def pattern_check(string, pattern):
    # check if string is the same as pattern
    return string == pattern

def insert_to_string(string, pos, character):
    my_list = list(string)
    my_list.insert(pos, character)
    return "".join(my_list)


####
# Converting between formats (orthographic, Consonant-Value)
####



def sampa_to_CV(sampa):
    # convert a sampa transcription to Consonant-Vowel form
    # e.g. abEs -> VCVC, ab@dOn -> VCVCVC
    return "".join(['V' if character in phono_vowels else 'C' for character in sampa])

def ortho_to_CV(ortho):
    #convert an ortographic transcription to Consonant-Vowel form
    #e.g. abaisses -> VCVVCCVC
    return "".join(['V' if character in ortho_vowels else 'C' for character in ortho])


####
# Syllable splitter
####

def get_split_sampa(sampa):
    # divide a sampa trasncription by syllables according to French phonology
    # e.g. abEs -> a-bEs, ab@dOn -> a-b@-dOn
    

    #Plan: go along the string looking for consonants surrounded by vowels
    #then, inset a separation character according to the rules for each case.

    #The 


    #initializing
    length = len(sampa)
    pos = 0
    offset = 0
    cv_form = sampa_to_CV(sampa)
    


    #padding
    padded_sampa = sampa + dummy_character * 10
    padded_cv_form = cv_form + dummy_character * 10


    #these variables will be the final output
    split_sampa = padded_sampa 
    split_cv_form = padded_cv_form

    while(pos < len(split_sampa)): #notice split_sampa may be updated
        pos += offset
        
        #VCV
        if pattern_check( split_cv_form[pos: pos + 3], "VCV" ):
            split_sampa, split_cv_form = split_VCV( split_sampa, split_cv_form, pos  )
            offset = 2

        #VV
        elif pattern_check(split_cv_form[pos: pos +2], "VV"):
            split_sampa, split_cv_form = split_VV( split_sampa, split_cv_form, pos  )
            offset = 2
        
        #VCCV
        elif pattern_check(split_cv_form[pos: pos +4], "VCCV"):
            split_sampa, split_cv_form = split_VCCV( split_sampa, split_cv_form, pos  )
            offset = 3
        
        #VCCCV
        elif  pattern_check(split_cv_form[pos: pos +5], "VCCCV"):
            split_sampa, split_cv_form = split_VCCCV( split_sampa, split_cv_form, pos  )
            offset = 4
        
        #VCCCCV
        elif  pattern_check(split_cv_form[pos: pos +6], "VCCCCV"):
            split_sampa, split_cv_form = split_VCCCCV( split_sampa, split_cv_form, pos  )
            offset = 5
        
        #VCCCCCV
        elif pattern_check(split_cv_form[pos: pos +7], "VCCCCCV"):
            split_sampa, split_cv_form = split_VCCCCCV( split_sampa, split_cv_form, pos  )
            offset = 6
        
        else:
            offset = 1

        

    #cleaning the result
    split_sampa = split_sampa.strip(dummy_character+separator_character)
    split_cv_form = split_cv_form.strip(dummy_character+separator_character)

    return split_sampa, split_cv_form




####
# Syllabification rules for each pattern
####


# It all comes down to determining the position where the separator character
# will be inserted

def split_VV(sampa, cv_form, pos):
    # two adjacent syllables
    # V-V
    separator_position = pos + 1
    return (insert_to_string(sampa, separator_position , separator_character), 
            insert_to_string(cv_form, separator_position , separator_character))

def split_VCV(sampa, cv_form, pos):
    # the consonant is the onset of the second syllable
    # V-CV
    separator_position = pos + 1
    return (insert_to_string(sampa, separator_position, separator_character),
            insert_to_string(cv_form, separator_position , separator_character) )

def split_VCCCCV(sampa, cv_form, pos):
    # the last three consonants form the onset of the second syllable
    # VC-CCCV
    separator_position = pos + 2
    return (insert_to_string(sampa, separator_position , separator_character), 
            insert_to_string(cv_form, separator_position , separator_character))

def split_VCCCCCV(sampa, cv_form, pos):
    # the last three consonants form the onset of the second syllable
    # VCC-CCCV
    separator_position = pos + 3
    return (insert_to_string(sampa, separator_position , separator_character), 
            insert_to_string(cv_form, separator_position , separator_character))


def split_VCCV(sampa, cv_form, pos):
    #we take care of the special cases first

    v_1, c_1, c_2, v_2 = sampa[pos:pos + 4]

    if c_2 in phono_semi_vowels:
        #e.g spéciaux spe-sjo
        #V-CCV
        separator_position = pos + 1
    elif c_1 in phono_fricatives and c_2 in phono_liquids:
        #e.g. découvre dé-cou-vrE
        #V-CCV
        separator_position = pos + 1
    elif c_1 in phono_plosives and c_2 in phono_liquids:
        #V-CCV
        separator_position = pos + 1
    else:
        #now we deal with the general case
        #VC-CV
        separator_position = pos + 2

    return (insert_to_string(sampa, separator_position , separator_character), 
            insert_to_string(cv_form, separator_position , separator_character))


def split_VCCCV(sampa, cv_form, pos):
    #we take care of the special cases first

    v_1, c_1, c_2, c_3, v_2 = sampa[pos: pos + 5]

    if (    c_1 in phono_fricatives
        and c_2 in phono_liquids
        and c_3 in phono_semi_vowels
        ):
        #e.g. effroyable ef-Rwa-jabl
        # V-CCCV
        separator_position = pos + 1
    
    elif (  c_1 in phono_plosives
        and c_2 in phono_liquids
        and c_3 in phono_semi_vowels
        ):
        #e.g. incroyable e~-krwa-jabl
        # V-CCCV
        separator_position = pos + 1
    
    elif (  c_1 in phono_plosives
        and c_2 in phono_liquids
        and c_3 in phono_plosives
        ):
        # e.g capable parce : ka-pabl-pas
        # VCC-CV
        separator_position = pos + 3

    else: 
        #now er deal with the general case
        #VC-CCV
        #e.g avec moi a-vek-mwa
        separator_position = pos + 2
        

    return (insert_to_string(sampa, separator_position , separator_character), 
            insert_to_string(cv_form, separator_position , separator_character))




### convert to macro-class

def sound_to_macroclass(char):
    if char in phono_vowels:
        return "Vowel"
    elif char in phono_semi_vowels:
        return "SemiVowel"
    elif char in phono_plosives:
        return "PlosiveC"
    elif char in phono_fricatives:
        return "FricativeC"
    elif char in phono_liquids:
        return "LiquidC"
    elif char in phono_nasals:
        return "NasalC"
    else:
        print("++++")
        print(char)
        print("-----")

        raise Exception("Something wrong with the syllable!")


def syllable_to_macroclass(syllable):
    #e.g. pej -> PlosiveC + V +SemiV
    res = map(sound_to_macroclass, syllable)
    res = " + ".join(list(res))
    return res


    
    



#SAMPA
phono_oral_vowels = {'a', 'e', 'i', 'u', 'o', 'y', 'E', '9', '2', 'O', '*'}
phono_nasal_vowels = {'@', '1', '5'}
phono_semi_vowels = {'w', 'j', '8'}
phono_plosives = {'p', 't', 'k', 'b', 'd', 'g'}
phono_fricatives = {'f', 's', 'S', 'v', 'z', 'Z'}
phono_liquids = {'R', 'l'}
phono_nasals = {'m', 'n', 'N', 'G'}


phono_vowels = phono_oral_vowels.union(phono_nasal_vowels)
