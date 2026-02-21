
def check_woman_priority(men:dict, women:dict, man:str, woman:str, current_pairs:dict) -> bool:
    man_pref = men.get(man) # получаем список предпочтений конкретного мужчины
    wife_index = man_pref.index(woman) # получаем индекс его текущей жены
    for i in range(wife_index):
        preferred_woman = man_pref[i] # женщина, которую мужчина предпочитает больше
        current_woman_man = current_pairs.get(preferred_woman) # текущий мужчина данной женщины
        woman_preferences = women.get(preferred_woman) # список предпочтений данной женщины
        man_index = woman_preferences.index(man) # получаем индекс мужчины в ее предпочтениях
        husband_index = woman_preferences.index(current_woman_man) # получаем индекс ее текущего мужчины
        if man_index < husband_index:
            return True
        
    return False


def stamble_match(men:dict, women:dict, pairs:list) -> bool:
    current_pairs = {woman : man for man, woman in pairs}
    for man, woman in pairs:
        woman_index = men.get(man).index(woman)
        if woman_index > 0:
            if check_woman_priority(men, women, man, woman, current_pairs):
                return False
    
    return True

def main(test_pairs:list) -> str:
    men = {
        'A': ['X', 'Y', 'Z'],
        'B': ['Y', 'X', 'Z'],
        'C': ['Y', 'Z', 'X']
    }
    women = {
        'X': ['B', 'A', 'C'],
        'Y': ['A', 'B', 'C'],
        'Z': ['C', 'A', 'B']
    }
    if stamble_match(men, women, test_pairs):
        return 'Устойчивое паросочетание'
    return 'Неустойчивое паросочетание'

if __name__ == '__main__':
    tests = [
        [['A', 'X'], ['B', 'Y'], ['C', 'Z']],
        [['A', 'Z'], ['B', 'X'], ['C', 'Y']],
        [['A', 'Y'], ['B', 'X'], ['C', 'Z']],
        [['A', 'Y'], ['B', 'Z'], ['C', 'X']],
        [['A', 'Y'], ['B', 'X'], ['C', 'Z']],
        [['A', 'X'], ['B', 'Z'], ['C', 'Y']]
    ]
    for test in tests:
        print(main(test))