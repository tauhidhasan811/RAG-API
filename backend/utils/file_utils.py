import os
import pandas as pd

def save_metadata(metadata, f_name,model_name):
    file_path = f'backend/storage/{model_name}/metadata/{f_name}.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if isinstance(metadata, dict):
        metadata = [metadata]
    elif isinstance(metadata, pd.DataFrame):
        metadata = metadata.to_dict(orient="records")

    new_df = pd.DataFrame(metadata)

    if os.path.exists(file_path):
        try:
            existing_df = pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            existing_df = pd.DataFrame()  # treat empty file as empty DataFrame
    else:
        existing_df = pd.DataFrame()

    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df.to_csv(file_path, index=False)
    return "Meta data saved"



