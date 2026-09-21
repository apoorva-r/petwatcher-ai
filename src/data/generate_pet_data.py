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

DISTINGUISHING_FEATURES = [
    "white patch on chest",
    "white paws",
    "dark patch around left eye",
    "small scar on right ear",
    "floppy left ear",
    "white tip on tail",
    "pink nose",
    "black spot on back",
    "long fluffy tail",
    "small white marking on forehead",
]

COLLARS = [
    "red collar",
    "blue collar",
    "black collar",
    "green collar",
    "yellow collar",
    "no collar",
]

TEMPERAMENTS = [
    "friendly and approachable",
    "shy around strangers",
    "calm and quiet",
    "energetic and playful",
    "usually cautious around people",
    "very social and curious",
]


def generate_description(species, breed, color):
    feature = random.choice(DISTINGUISHING_FEATURES)
    collar = random.choice(COLLARS)
    temperament = random.choice(TEMPERAMENTS)

    if collar == "no collar":
        collar_text = "It is not wearing a collar."
    else:
        collar_text = f"It is wearing a {collar}."

    return (
        f"A {color} {breed}. "
        f"It has a {feature}. "
        f"{collar_text} "
        f"The animal is {temperament}."
    )


def generate_pets(spark, count=1000):
    rows = []

    for i in range(count):
        species = random.choice(list(SPECIES))
        breed = random.choice(SPECIES[species])
        color = random.choice(COLORS)

        description = generate_description(
            species=species,
            breed=breed,
            color=color,
        )

        rows.append(
            (
                f"PET-{i:05d}",
                fake.first_name(),
                species,
                breed,
                color,
                description,
            )
        )

    return spark.createDataFrame(
        rows,
        [
            "pet_id",
            "name",
            "species",
            "breed",
            "color",
            "description",
        ],
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

    print(
        f"Wrote {df.count()} pets "
        "to petwatch_dev.bronze.pets"
    )