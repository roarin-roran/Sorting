simpsons_characters = [
    ['Homer', 'Simpson'],
    ['Ralph', 'Wiggum'],
    ['Maggie', 'Simpson'],
    ['Abraham', 'Simpson'],
    ['Cletus', 'Spuckler'],
    ['Barney', 'Gumble'],
    ['Bart', 'Simpson'],
    ['Hans', 'Moleman'],
    ['Ned', 'Flanders'],
    ['Edna', 'Krabappel'],
    ['Lenny', 'Leonard'],
    ['Jimbo', 'Jones'],
    ['John', 'Frink'],
    ['Agnes', 'Skinner'],
    ['Martin', 'Prince'],
    ['Fat', 'Tony'],
    ['Marge', 'Simpson'],
    ['Otto', 'Mann'],
    ['Troy', 'Mcclure'],
    ['Moe', 'Szyslak'],
    ['Apu', 'Nahasapeemapetilon'],
    ['Patty', 'Bouvier'],
    ['Lisa', 'Simpson'],
    ['Chief', 'Wiggum'],
    ['Kent', 'Brockman'],
    ['Waylon', 'Smithers'],
    ['Jasper', 'Beardly'],
    ['Nelson', 'Muntz'],
    ['Principal', 'Skinner'],
    ['Helen', 'Lovejoy'],
    ['Carl', 'Carlson'],
    ['Lionel', 'Hutz'],
    ['Milhouse', 'Van Houten'],
    ['Selma', 'Bouvier'],
    ['Charles Montgomery', 'Burns'],
    ['Snake', 'Jailbird'],
    ['Rainier', 'Wolfcastle'],
]

# Format string with first name and last name with same length
# for each name in the list
#
# >>> for name in simpsons_characters:
# ...     print(f'{name[0]:{len(name[1])}} {name[1]}')
# ...
# Homer Simpson
# Ralph Wiggum
# Maggie Simpson


def qsort(lst, lo, hi, key=lambda x: x):
    if hi - lo <= 1:
        return
    pivot = lst[lo]
    k = lo + 1
    g = hi - 1
    while k <= g:
        print(lst, k, g)
        while k <= g and key(lst[k]) <= key(pivot):
            k += 1
        while k <= g and key(lst[g]) >= key(pivot):
            g -= 1
        if k < g:
            lst[k], lst[g] = lst[g], lst[k]
            k += 1
            g -= 1
    lst[lo], lst[g] = lst[g], lst[lo]
    print(lst, k, g)
    print()
    qsort(lst, lo, g, key)
    qsort(lst, g+1, hi, key)

import Inputs.Inputs as inputs

A = inputs.random_uary_array(10,100)
A = inputs.random_permutation(10)
print(A)
qsort(A, 0, len(A), key=lambda x: -x+100)
print(A)

