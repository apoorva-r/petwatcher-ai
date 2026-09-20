# Databricks notebook source

from src.data.generate_pet_data import generate_pets

df = generate_pets(spark, count=1000)

display(df.limit(20))
