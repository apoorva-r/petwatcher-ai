from src.data.generate_pet_data import SPECIES, COLORS


def test_species_configuration():
    assert "dog" in SPECIES
    assert "cat" in SPECIES


def test_colors_configuration():
    assert len(COLORS) > 0
