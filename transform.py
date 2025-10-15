import duckdb

# df = pd.read_csv("food.csv")
# print(df.groupby("food_category_id").nth(0)['description'])

duckdb.sql("""
SELECT DISTINCT
    --fdc_id, 
    --food_category_id,
    trim(
        split_part(split_part(split_part(split_part(lower(description), ',', 1), ' -', 1), ';', 1), ' (', 1)
    ) description
FROM 'food.csv'
WHERE food_category_id NOT IN (
    2008,
    --2802,
    3002,
    3004,
    3006,
    3102,
    3104,
    3202,
    3204,
    3208,
    3402,
    3404,
    3702,
    3704,
    3706,
    3722,
    3730,
    3740,    
    3742,
    3744,    
    4202,
    4202,
    4402,
    5002,
    5004,
    5502,
    5504,
    6002,
    6018,
    7204,
    7506,
    8410,
    8012,
    8402,
    8412,
    8806,
    9002,
    9004,
    9006,
    9007,
    9008,
    9010,
    9012,
    9202,
    9404,
    9999,
)
ORDER BY description, fdc_id
""").write_csv("clean/food.txt")
