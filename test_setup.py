from utils.data_loader import load_and_prepare_data, make_schema_text

df = load_and_prepare_data("data/coffee_sales.csv")

print("Shape       :", df.shape)
print("Columns     :", list(df.columns))
print("Year values :", sorted(df["year"].dropna().unique().tolist()))
print("Quarter vals:", sorted(df["quarter"].dropna().unique().tolist()))
print("\nSchema text for LLM prompts:")
print(make_schema_text(df))
print("\nSample rows:")
print(df.sample(3).to_string())