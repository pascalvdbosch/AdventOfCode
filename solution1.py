with open('input1.txt', 'r') as i:
    lines = [line.strip() for line in i.readlines()]

nums = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
}
reverse = lambda s: ''.join(reversed(s))
total = 0
for line in lines:
    vals = {}
    for rev in [False, True]:
        val = None
        indices = range(len(line))
        if rev: line = reverse(line)
        for index in indices:
            for num in nums.keys():
                if val is None and line[index:].startswith(reverse(num) if rev else num):
                    val = nums[num]
        vals[rev] = val
    total += 10 * vals[0] + vals[1]
print(total)