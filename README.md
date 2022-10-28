# Introduction:
Online commercial platforms (e.g Bol) need to make inventory of todays available products. Inventory_tool compares the available products of the previous day with the products of the current day (both available in .csv files), and provides the following operations that can be sent to a marketing channel to update their database:

  - Create: ​the product wasn’t imported from the eCommerce system yesterday,
    but it was imported today. This means we have to send a ​create operation
    ​to the eCommerce platform

  - Update:​ the product was imported yesterday and is also imported today,
    however, one of the values for the products has changed (e.g. the price of
    the product). This means we have to send an ​update operation​ to the
    marketing channel

  - Delete: ​the product was imported yesterday, but was not imported today.
    This means we have to send a ​delete operation ​to the marketing channel


# Scope:
Make a basic implementation of the logic described above. You should have
received two CSV files to resemble the data that is imported from the eCommerce system:

  - product_inventory_before.csv​ (resembles the product data that was imported yesterday)
  - product_inventory_after.csv ​(resembles the product data that was imported today)

Build a program that compares the product data between the `before CSV` and
the `after CSV`. The `​id​` column can be assumed to be a unique identifier for the products in both CSVs. The
output should give the create, update, and delete operations that should be sent to a marketing channel.


# Output:
  - The output is a sequence of operations in the form of triples that contain:
        1. the operation type
        2. the product id
        3. either a dictionary with the complete product data where the keys are the column names
           from the CSV files or a `None`
