# Split words.txt based on first letter
# words.txt sources: http://www.mieliestronk.com/corncob_lowercase.txt
import util

raw_file = 'words.txt'

with open(raw_file) as f:
    ctn = f.read().splitlines()

# assign to array
arr = [[] for i in range(26)]
for word in ctn:
    idx = util.get_index(word)
    arr[idx].append(word)

# save to file
for i, a in enumerate(arr):
    key = util.get_key(i)
    filename = util.get_file_name(i)
    print(f'{key}: {len(a)}')
    with open(filename, 'w') as f:
        f.write('\n'.join(a))
