import pandas as pd
import numpy as np



def power_distance(series_a, series_b, power=1, ord=1):
    return np.linalg.norm((series_a**power) - (series_b**power), ord=ord)

def id(arr: np.array)-> np.array:
    return arr

def pattern_estimations_near_contrarian(
    series,
    window=20,
    horizon=5,
    k=5,
    n=5,
    f_distance=power_distance,
    f_treatment=id
):

    """
    series  : np.array ou pd.Series de returns
    window  : longueur du pattern
    horizon : horizon du return futur
    k       : nombre de patterns near 
    n       : nombre de patterns far (contrarian)
    """
    if np.isnan(series).any():
        return np.nan
    
    series = np.asarray(series)
    current_pattern = series[-window:]
    
    
    distances = []

    # calcul des distances
    for i in range(len(series) - window - horizon + 1):
        past_pattern = series[i:i + window]
        dist = f_distance(f_treatment(past_pattern), f_treatment(current_pattern))
        distances.append((dist, i))

    # tri par distance
    distances.sort(key=lambda x: x[0])
    
    
    # near et far séparés
    if k==0:
        near = []
    else:
        near = distances[:k]

    if n==0:
        far = []
    else:
        far = distances[-n:]
    
    
    estimations = []

    for dist, idx in near:
        future_return = np.prod(
            [1 + series[idx + window + i] for i in range(horizon)]
        ) - 1
        estimations.append({
            "start_index": idx,
            "distance": dist,
            "estimation": future_return  # signe + pour near
        })

    for dist, idx in far:
        future_return = np.prod(
            [1 + series[idx + window + i] for i in range(horizon)]
        ) - 1
        estimations.append({
            "start_index": idx,
            "distance": dist,
            "estimation": -future_return  # signe - pour far
        })
    

    if len(estimations) == 0:
        estimations.append({
            "start_index": None,
            "distance": None,
            "estimation": np.nan
        })
        print('k and n ==0')
    return estimations



def applicate_mean(
    series,
    window=20,
    horizon=5,
    k=5,
    n=5
):
    result = pattern_estimations_near_contrarian(
    series,
    window,
    horizon,
    k=k,
    n=n)

    estimations = [x['estimation'] for x in result]
    
    return np.mean(estimations) if estimations else np.nan

def applicate_std(
    series,
    window=20,
    horizon=5,
    k=5,
    n=5
):
    result = pattern_estimations_near_contrarian(
    series,
    window,
    horizon,
    k=k,
    n=n)

    estimations = [x['estimation'] for x in result]
    
    return np.std(estimations) if estimations else np.nan