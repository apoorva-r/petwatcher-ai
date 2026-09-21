from faker import Faker
import random

fake = Faker()

SPECIES = {
    "dog": ["Labrador", "Golden Retriever", "German Shepherd", "Mixed"],
    "cat": ["British Shorthair", "Maine Coon", "Persian", "Mixed"],
}

COLORS = [
    "black",
    "white",
    "brown",
    "grey",
    "black-white",
    "brown-white",
]


def generate_pets(spark, count=1000):
    rows = []

    for i in range(count):
        species = random.choice(list(SPECIES))

        rows.append(
            (
                f"PET-{i:05d}",
                fake.first_name(),
                species,
                random.choice(SPECIES[species]),
                random.choice(COLORS),
                fake.sentence(),
            )
        )

    return spark.createDataFrame(
        rows,
        ["pet_id", "name", "species", "breed", "color", "description"],
    )


if __name__ == "__main__":
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()

    df = generate_pets(spark)

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable("petwatch_dev.bronze.pets")
    )

    print(f"Wrote {df.count()} pets to petwatch_dev.bronze.pets")