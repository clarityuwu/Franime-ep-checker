import re

with open('errors.txt', 'r') as f:
    content = f.readlines()

episodes = []
for line in content:
    match = re.search(r'Episode: (\d+)', line)
    if match:
        episodes.append(int(match.group(1)))

episodes.sort()

ranges = []
start = episodes[0]
end = episodes[0]

for i in range(1, len(episodes)):
    if episodes[i] == end + 1:
        end = episodes[i]
    else:
        ranges.append((start, end) if start != end else (start,))
        start = end = episodes[i]

ranges.append((start, end) if start != end else (start,))

for r in ranges:
    print('[' + ';'.join(map(str, r)) + ']', end=' ')