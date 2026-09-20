import glob
from src.chunking import ChunkingStrategyComparator
import os

def get_content(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    if text.startswith('---\n'):
        text = text[text.find('---\n', 4)+4:].strip()
    return text

comparator = ChunkingStrategyComparator()
files = sorted(glob.glob('data/shopee-orders/*.md'))[:3]
for file in files:
    content = get_content(file)
    res = comparator.compare(content, chunk_size=350)
    print(f'=== {os.path.basename(file)} ===')
    for strat, data in res.items():
        print(f'{strat}: count={data["count"]}, avg={data["avg_length"]:.2f}')
