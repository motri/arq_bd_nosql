def transform_player_data(dataframe):
    # Convert DataFrame to dictionary format for MongoDB
    data = dataframe.to_dict('records')
    for player in data:
        # Transformations: Add default fields if necessary
        player.setdefault("awards", {"best_club_year": 0, "golden_glove": 0})
    return data
