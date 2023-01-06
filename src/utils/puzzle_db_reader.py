import pandas as pd

def get_db_dataframe():
    df = pd.read_csv('data/lichess_db_puzzle_w_header.csv')
    return df

def gen_yield(generator):
    if generator:
        try:
            i, row = next(generator)
        except StopIteration:
            return
        yield row 
        yield from gen_yield(generator)

def get_random_puzzle(size: int=1, get_generator: bool=False):
    df = get_db_dataframe()
    puzzle = df.sample(size)
    if size == 1:
        puzzle = puzzle.iloc[0]
        return puzzle
    else:
        if get_generator:
            return gen_yield(puzzle.iterrows())
        else:
            return list(row for i, row in puzzle.iterrows())

if __name__ == '__main__':
    pzz = get_random_puzzle(5, get_generator=True)
    for pz in pzz:
        pz.FEN