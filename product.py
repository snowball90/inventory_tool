from enum import Enum, auto
from typing import Tuple, Optional, Dict, Iterator, Any
import csv


class Operation(Enum):
    CREATE = auto()
    UPDATE = auto()
    DELETE = auto()


def csv_to_dict_of_dicts(path_to_before_csv: str, path_to_after_csv: str) -> Dict[str, Any]:
    """Reads the .csv files as dictionaries

    Args:
        path_to_before_csv (str): path for the product_inventory_before.csv file
        path_to_after_csv (str): path for the product_inventory_after.csv file

    Returns:
        Dict[str, Any]: dictionaries (e.g. {product id: dictionary with info about the product})
    """
    dict_before = {}
    dict_after = {}
    with open(path_to_before_csv) as file_obj_before, open(path_to_after_csv) as file_obj_after:
        reader_before = csv.DictReader(file_obj_before)
        reader_after = csv.DictReader(file_obj_after)
        for row in reader_before:
            dict_before[row['id']] = row
        for row in reader_after:
            dict_after[row['id']] = row
    return dict_before, dict_after


def dict_parser_comparison(dict_before: dict, dict_after: dict) -> Iterator[Tuple[Operation, str, Optional[Dict[str, Any]]]]:
    """Parses two dictionaries of dictionaries, compares them based on the unique key 'id, and
    returns an list of tuples with three elements:
    first elementL: operation -> CREATE/UPDATE/DELETE
    second element: value of the product id (e.g. 008735-03-170-162)
    third element: dictionary with all data of a product or None if operation==DELETE

    Args:
        dict_before (dict): dictionary of the product_inventory_before.csv file
        dict_after (dict): dictionary of the product_inventory_after.csv file

    Returns:
        (list): Iterator[Tuple[Operation, str, Optional[Dict[str, Any]]]]: list of tuple that have the potential to
        be used to construct an HTTP request to update a database.

    """

    """
    - Delete: the product was imported yesterday, but was not imported today.
            This means we have to send a delete operation to the marketing channel
    """
    deleted_id = [id for id in dict_before.keys() if id not in dict_after.keys()]
    deleted_items = [(Operation.DELETE, id, None) for id in deleted_id]

    """
    - Create: the product wasn’t imported from the eCommerce system yesterday,
        but it was imported today. This means we have to send a create operation to the eCommerce platform
    """
    created_id = [id for id in dict_after.keys() if id not in dict_before.keys()]
    created_items = [(Operation.CREATE, id, dict_after[id]) for id in created_id]

    """
    - Update: the product was imported yesterday and is also imported today,
    however, one of the values for the products has changed(e.g. the price of
    the product). This means we have to send an update operation to the
    marketing channel
    """
    common_id = [id for id in dict_before.keys() if id not in deleted_id and id not in created_id]
    updated_items = []
    for id in common_id:
        if dict_before[id] != dict_after[id]:
            updated_items.append((Operation.UPDATE, id, dict_after[id]))

    return deleted_items + created_items + updated_items


if __name__ == "__main__":
    old_excel = 'path of the product_inventory_before.csv file as a string'
    new_excel = 'path of the product_inventory_after.csv file as a string'
    dict1, dict2 = csv_to_dict_of_dicts(old_excel, new_excel)
    result_operation = dict_parser_comparison(dict1, dict2)
    print(result_operation)
