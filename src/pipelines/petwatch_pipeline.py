from pyspark import pipelines as dp
from pyspark.sql.functions import col, current_timestamp, lower, trim


@dp.table(
    name="silver_pets",
    comment="Cleaned and normalized pet records"
)
def silver_pets():
    return (
        spark.read.table("petwatch_dev.bronze.pets")
        .select(
            trim(col("pet_id")).alias("pet_id"),
            trim(col("name")).alias("name"),
            lower(trim(col("species"))).alias("species"),
            trim(col("breed")).alias("breed"),
            lower(trim(col("color"))).alias("color"),
            trim(col("description")).alias("description"),
            current_timestamp().alias("created_at"),
        )
        .dropDuplicates(["pet_id"])
        .filter(
            col("pet_id").isNotNull()
            & col("species").isNotNull()
        )
    )