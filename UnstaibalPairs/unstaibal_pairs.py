
def check_woman_priority(men:dict, women:dict, man:str, woman:str, current_pairs:dict) -> bool:
    for member in range(men.get(man).index(woman)):
        potential_woman = men.get(man)[member]
        potential_womans_man = current_pairs.get(potential_woman)
        if women.get(potential_woman).index(man) < women.get(potential_woman).index(potential_womans_man):
            return True  # Нашли блокирующую пару
    
    return False

def stamble_match(men:dict, women:dict, pairs:list) -> bool:
    current_pairs = {woman : man for man, woman in pairs}
    for man, woman in pairs:
        if men.get(man)[0] != woman:
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
    pairs = test_pairs
    if stamble_match(men, women, pairs):
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