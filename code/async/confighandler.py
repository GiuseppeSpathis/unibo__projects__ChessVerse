import random


def gen_start_fen(rank=50):
    def calc_imb(x):
        firstVal = 30
        secondVal = -30
        return ((secondVal - firstVal) / 100) * x + firstVal
    pieces = ["p", "n", "b", "r", "q"]
    pieces_weight = {"k":0, "p": 1, "n": 3, "b": 3, "r": 5, "q": 9}
    imbalance = calc_imb(rank)
    while True:
        wb = [random.choice(pieces) for _ in range(8)]
        wf = [random.choice(pieces[:3]) for _ in range(8)]
        bb = [random.choice(pieces) for _ in range(8)]
        bf = [random.choice(pieces[:3]) for _ in range(8)]
        wb[4] = "k"
        bb[4] = "k"
        white = sum(pieces_weight[p] for p in wb+wf)
        black = sum(pieces_weight[p] for p in bb+bf)
        bigger, smaller = (white, black) if rank < 50 else (black, white)
        if abs(white-black) >= max(abs(imbalance), 1) and bigger > smaller:
            break
    wb = "".join(wb)
    bb = "".join(bb)
    wf = "".join(wf)
    bf = "".join(bf)
    castle = f"""{
        "K" if any(wb[i] == "r" for i in [5, 6, 7]) else ""}{
        "Q" if any(wb[i] == "r" for i in [0, 1, 2, 3]) else ""}{
        "k" if any(bb[i] == "r" for i in [5, 6, 7]) else ""}{
        "q" if any(bb[i] == "r" for i in [0, 1, 2, 3]) else ""}"""
    return f"{bb}/{bf}/8/8/8/8/{wf.upper()}/{wb.upper()} w {castle if len(castle) else '-'} - 0 1"