# easy-syllab
An automatic syllabificator for the French language


# Main program
Run
```
python main.py
```

The previous command generates two files:
- `Output.txt`, which contains the syllabification for the words in `Input.txt`
- `Frequency_analysis.txt`, which contains an analysis of the frequencies of the patterns that appear in the syllabification


# Syllabification rules

`src/syllabification_rules.py` contains the rules for syllabification of French words.

- Example 1: 
```
#VCV
if pattern_check( split_cv_form[pos: pos + 3], "VCV" ):
    split_sampa, split_cv_form = split_VCV( split_sampa, split_cv_form, pos  )
    offset = 2

....

def split_VV(sampa, cv_form, pos):
    # two adjacent syllables
    # V-V
    separator_position = pos + 1
    return (insert_to_string(sampa, separator_position , separator_character), 
            insert_to_string(cv_form, separator_position , separator_character))


```

- Example 2:

```

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


```

# Results

The first five lines and last five lines from `Output.txt` are:

```
abaisses VCVVCCVC abEs VCVC a-bEs V-CVC 
abandonne VCVCCVCCV ab@dOn VCVCVC a-b@-dOn V-CV-CVC 
abandonneras VCVCCVCCVCVC ab@dOnRa VCVCVCCV a-b@-dOn-Ra V-CV-CVC-CV 
abatage VCVCVCV abataZ VCVCVC a-ba-taZ V-CV-CVC 
abatte VCVCCV abat VCVC a-bat V-CVC 

zombies CVCCVVC z1bi CVCV z1-bi CV-CV 
zonage CVCVCV zOnaZ CVCVC zO-naZ CV-CVC 
zoologique CVVCVCVCVV zOOlOZik CVVCVCVC zO-O-lO-Zik CV-V-CV-CVC 
zooxanthelles CVVCVCCCVCCVC zOOks@tEl CVVCCVCVC zO-Ok-s@-tEl CV-VC-CV-CVC 
zozotante CVCVCVCCV zOzOt@t CVCVCVC zO-zO-t@t CV-CV-CVC 
```

The results from the frequency analysis are:

Consonant-Vowel Syllables Top Frequencies
| CV | 10702 
| CVC | 3344 
| CCV | 2538 
| V | 1665 
| CCVC | 693 
| VC | 416 
| CVCC | 365 
| CCCV | 59 
| CCVCC | 33 
| CCCVC | 23 
| VCC | 20 
| CVCCC | 8 
| CCCVCC | 7 
| VCCC | 1 
| CCCCCV | 1 
| CCCCV | 1 

Macroclass Syllables Top Frequencies
| PlosiveC + Vowel | 4144 
| FricativeC + Vowel | 2481 
| LiquidC + Vowel | 2126 
| NasalC + Vowel | 1743 
| Vowel | 1665 
| PlosiveC + LiquidC + Vowel | 1299 
| PlosiveC + Vowel + LiquidC | 730 
| FricativeC + SemiVowel + Vowel | 479 
| FricativeC + Vowel + LiquidC | 424 
| PlosiveC + Vowel + FricativeC | 335 
| PlosiveC + Vowel + PlosiveC | 284 
| FricativeC + LiquidC + Vowel | 253 
| PlosiveC + SemiVowel + Vowel | 242 
| FricativeC + Vowel + PlosiveC | 220 
| NasalC + Vowel + LiquidC | 212 

Sampa Syllables Top Frequencies
| a | 470 
| de | 456 
| e | 331 
| te | 329 
| ti | 276 
| Ra | 272 
| @ | 271 
| Re | 267 
| m@ | 254 
| li | 235 
| k1 | 222 
| R* | 222 
| 5 | 219 
| se | 194 
| si | 187 

