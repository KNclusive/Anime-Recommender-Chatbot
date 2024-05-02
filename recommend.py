from joblib import load
import pandas as pd
import numpy as np
import ast

def infer(matrix, index_to_profile, profile_to_index, model, user_name = None, neighbours = 30):
    distance, suggestion_usrID = model.kneighbors(matrix[profile_to_index[user_name]].reshape(1,-1),n_neighbors=neighbours)
    user_recommended = [index_to_profile[suggestion_usrID[0][i]] for i in range(1, len(suggestion_usrID[0]))]
    return user_recommended, distance, suggestion_usrID

def distance_weights(distance):
    max_distance = distance[0][1:].max() + 1e-5
    weights = max_distance - distance[0][1:]
    # Normalize the weights
    normalized_weights = weights / np.sum(weights)
    # Compute the cumulative sum
    cumulative_weights = np.cumsum(normalized_weights)
    return cumulative_weights

# Roulette selection function, as defined previously
def roulette_selection(cumulative_weights, user_recommended):
    user_index = np.where(cumulative_weights > np.random.rand())[0][0]
    return user_recommended[user_index]

# Function to recommend items
def recommend_items(cumulative_weights, num_items, user_recommended, user_data):
    recommendations = []
    while len(recommendations) < num_items:
        usr_name = roulette_selection(cumulative_weights, user_recommended)
        items = user_data[user_data['profile'] == usr_name]['favorites_anime'].to_list()
        if items[0] != '[]':
            recommended_item = np.random.choice(ast.literal_eval(items[0]))
            if recommended_item not in recommendations:
                recommendations.append(recommended_item)
    return recommendations

def collaborative_main(user_name, model, profile_to_index, index_to_profile, matrix, user_data, rating_data, anime_data, no_of_animes):
    user_recommended, distance, suggestion_usrID = infer(matrix, index_to_profile, profile_to_index, model, user_name)
    cumulative_weights = distance_weights(distance)
    recommended_items = [int(item) for item in recommend_items(cumulative_weights, no_of_animes, user_recommended, user_data) if item.isdigit()]
    return anime_data[anime_data['uid'].isin(recommended_items)], 1


def popular_main(anime_data, found = 2):

    temp_data = anime_data.copy()

    anime_needed = temp_data.nsmallest(5, 'popularity')

    return anime_needed, found


def content_main(anime_features, model, combined_features, anime_data):

    data_mask = pd.DataFrame()
    for feature_name, feature_value in anime_features.items():
        if isinstance(feature_value, list):
            matching_rows = anime_data[feature_name].apply(lambda row: item in row for item in feature_value)
            data_mask = pd.concat([data_mask, matching_rows], axis = 1)
        else:
            matching_rows = anime_data[feature_name] == feature_value
            data_mask = pd.concat([data_mask, matching_rows], axis = 1)

    found = 1

    all_anime = anime_data[[all(x) for idx, x in data_mask.iterrows()]]
    any_anime = anime_data[[any(x) for idx, x in data_mask.iterrows()]]

    if all_anime.empty:

        if any_anime.empty:
            return popular_main(anime_data, 3)
        
        found = 0
        if len(any_anime) < 5:
            anime_needed = any_anime
        else:
            return any_anime[:5], found
    
    anime_needed = all_anime

    anime_index = anime_data[anime_data['uid'] == any_anime.iloc[0]['uid']].index
    _, indices = model.kneighbors(combined_features[anime_index.to_list()])
    return anime_data.iloc[indices[0]], found