import pandas as pd



# Drop unwanted columns
def drop_columns(data: pd.DataFrame, column_names: list) -> pd.DataFrame:

    """Picks only specified columns from DataFrame."""

    return data[column_names]



# Drop null values
def drop_nulls(data: pd.DataFrame) -> pd.DataFrame:

    """Drops rows with null values."""

    return data.dropna()



# Change type
def change_type(data: pd.DataFrame, change_dict: dict) -> pd.DataFrame:

    """Changes column types to correct type indicated on dictionary values."""

    for column, correct_type in change_dict.items():
        
        if column not in data.columns:
            raise ValueError(f"Column {column} does not exist.")
        
        if change_dict[column] == 'float':
            data[column] = data[column].astype(str).str.replace(r',', '.').str.replace(' kg', '').str.replace(' cm', '')
        
        data[column] = data[column].astype(correct_type)

    return data



# Summary
def check_quality(data: pd.DataFrame):

    """Basic Quality Check. Returns DataFrame with columns, types 
    and unique, missing and duplicate elements plus their ratios.
    Complement/extension of .info() function."""

    n = len(data)

    summary = []
    for column in data:
        col_type = type(data[column].iloc[0])
        elements = data[column].count()
        unique = data[column].nunique(dropna = True)
        rate_unique = round(unique / n * 100, 2)
        missing = data[column].isna().sum() 
        rate_missing = round(missing / n * 100, 2)
        duplicated = data[column].duplicated().sum()
        
        summary.append((column, col_type, elements, unique, rate_unique, missing, rate_missing, duplicated))
    
    return pd.DataFrame(summary, columns = ['column', 'type', 'elements', 'unique', 'rate_unique', 'missing', 'rate_missing', 'duplicated'])



# Clean data
def clean_df(data):

    """Cleans data by:
    * Selecting only useful columns.
    * Dropping rows with null values.
    * Renaming columns.
    * Changing column to correct types.
    Returns clean data."""

    # Choosing only useful columns
    df_red = drop_columns(data, ['Year', 'Gender', 'Age', '1.Body Weight (kg)', '2.Stature height (cm)',
                           '3.The height of the root of the nose in standing (cm)', '4.Height of shoulders in standing position (cm)',
                           '5.Height of the elbow in standing position (cm)', '6.The height of the tip of the 3rd finger in standing position (cm)',
                           '8.The width of the shoulders (cm)', "10.Arm's reach in standing position (cm)", '16.Knee height in sitting position (cm)',
                           '18.The length of the forearm and hand at the elbow bend  (cm)', '20.Leg length when sitting forward (cm)',
                           '22.Palm width (cm)', '23.Palm length (cm)', '24.Foot width (cm)', '25.Foot lenght (cm)'])

    # Dropping nulls
    df_red = drop_nulls(df_red)

    # Renaming columns
    df_red.columns = ['year', 'gender', 'age', 'weight', 'height', 'eye_height', 'shoulder_height', 'elbow_height', 'fingertip_height', 'shoulder_width', 'arms_reach', 'knee_height', 'fingertip_to_elbow_length', 'leg_length', 'palm_width', 'palm_length', 'foot_width', 'foot_length']

    # Changing column type
    change_dict = {}
    for column in df_red.columns:
        if column != 'gender':
            change_dict[column] = 'float'
        else:
            change_dict[column] = 'str'

    df_clean = change_type(df_red, change_dict)

    # Final check
    check_quality(df_red)

    return df_clean
