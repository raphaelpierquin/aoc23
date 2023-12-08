def translate_11(interval, mapping):
    if len(interval) == 0:
        return (),()
    s,e = interval
    ms,me,sh = mapping
    left, mapped = [], []
    if ms >= s and me <= e:
        left.append((s,ms))
        left.append((me,e))
        mapped.append((ms+sh,me+sh))
    elif s >= ms and e <= me:
        mapped.append((s+sh,e+sh))
    elif ms >= s and ms < e:
        left.append((s,ms))
        mapped.append((ms+sh,e+sh))
    elif me >=s and me < e:
        mapped.append((s+sh,me+sh))
        left.append((me,e))
    else:
        left.append(interval)
    return left, mapped

def translate_m1(intervals, mapping):
    lefties, mappeds = [], []
    for interval in intervals:
        left, mapped = translate_11(interval, mapping)
        lefties.extend(left)
        mappeds.extend(mapped)
    return lefties,mappeds

def translate(intervals, mappings):
    lefties, mappeds = [], []
    for mapping in mappings:
        intervals, mapped = translate_m1(intervals, mapping)
        mappeds.extend(mapped)
    intervals.extend(mappeds)
    return intervals

def test_translate_11():
    assert translate_11((),(20,40,10)) == ((),())
    # [1] [2]
    assert translate_11(( 1,10),(20,40,10)) == ([(1,10)],[])
    # [  1  ]
    #    [  2  ]
    assert translate_11(( 1,10),(5 ,40,10)) == ([(1,5)],[(15,20)])
    #    [  1  ]        [10  20]
    # [  2  ]         [5   15] -> 30
    assert translate_11((10,20),(5 ,15,30)) == ([(15,20)],[(40,45)])
    # [  1  ]         [10     40]
    #  [ 2 ]            [20 30] -> 30
    #                 [10 20] [30 40] -> [50,60]
    assert translate_11((10,40),(20,30,30)) == ([(10,20),(30,40)],[(50,60)])
    #  [ 1 ]            [20 30]
    # [  2  ]         [10     40] -> 30
    #                             -> [50,60]
    assert translate_11((20,30),(10,40,30)) == ([],[(50,60)])
    assert translate_11((5,10),(0,10,100)) == ([],[(105,110)])

def test_translate_m1():
    # [] []
    #       []
    assert translate_m1([( 1,10)],(20,40,10)) == ([(1,10)],[])
    assert translate_m1([( 1,10)],(20,40,10)) == ([(1,10)],[])
    assert translate_m1([( 1,10),(11,15)],(20,40,10)) == ([(1,10),(11,15)],[])
    # [1   4] [5 6]
    #  [2 3] -> 10
    # [1 2] [3 4] [5 6] -> [12 13]
    assert translate_m1([(1,4),(5,6)],(2,3,10)) == ([(1,2),(3,4),(5,6)],[(12,13)])
    # [10 30] [40 60]
    #    [20    50] -> 50
    # [10, 20] [50 60] -> [70 80] [90 100]
    assert translate_m1([(10,30),(40,60)],(20,50,50)) == ([(10,20),(50,60)],[(70,80),(90,100)])

def test_translate():
    assert translate([(1,10)],[(20,40,10)]) == [(1,10)]
    assert translate([(1,10)],[(30,50,1000),(0,20,10),(100,200,300)]) == ([(11,20)])
    # [1       6]
    #   [2  4] -> 10
    #     [3  5] -> 100
    # [1 2] [5 6] ->  [12 14] [104 105]
    assert translate([(1,6)],[(2,4,10),(3,5,100)]) == ([(1,2),(5,6),(12,14),(104,105)])
    assert translate([(79, 93)],[(98, 100, -48), (50, 98, 2)]) == ([(81,95)])
