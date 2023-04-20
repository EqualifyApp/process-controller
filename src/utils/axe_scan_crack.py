import json
import time
from utils.watch import logger
from data.insert import insert_axe_items, insert_axe_nodes, insert_axe_subnodes


def process_items(url_id, scan_event_id, items, item_type):
    success = True
    for item in items:
        nodes = process_nodes(url_id, scan_event_id, item["nodes"])
        if not nodes:
            success = False
            # logger.error(f"Failed to process nodes for item: {items} ")
            time.sleep(5)

        item_processed = {
            "type": item_type,
            "impact": item["impact"],
            "tags": item["tags"],
            "area": item["id"],
            "nodes": nodes
        }

        if not insert_axe_items(scan_event_id, url_id, item_type, item["id"], item["impact"], item["tags"]):
            success = False
            logger.debug("No nodes, items processed successfully")
            time.sleep(5)

    logger.info(f"Processing items for {item_type} completed")
    return success


def process_nodes(url_id, scan_event_id, nodes):
    success = True
    processed_nodes = []
    for node in nodes:
        subnodes_all = process_subnodes(url_id, scan_event_id, node["all"], "all")
        subnodes_any = process_subnodes(url_id, scan_event_id, node["any"], "any")
        subnodes_none = process_subnodes(url_id, scan_event_id, node["none"], "none")

        if not (subnodes_all and subnodes_any and subnodes_none):
            success = False
            logger.error(f"Failed to process subnodes for a node:  {nodes} ")
            time.sleep(5)

        processed_node = {
            "html": node["html"],
            "impact": node["impact"],
            "target": node["target"],
            "data": node.get("data", {}),  # Use .get() method with default value
            "all": subnodes_all,
            "any": subnodes_any,
            "none": subnodes_none
        }

        if not insert_axe_nodes(scan_event_id, url_id, node["html"], node["impact"], node["target"], json.dumps(node.get("data", {})), None):  # Convert the dictionary to JSON string
            success = False
            logger.debug("No subnodes, nodes processed successfully")
            time.sleep(5)

        processed_nodes.append(processed_node)

    logger.debug("Processing nodes completed")
    return processed_nodes if success else False


def process_subnodes(url_id, scan_event_id, subnodes, node_type):
    success = True
    processed_subnodes = []
    for index, subnode in enumerate(subnodes):
        processed_subnode = {
            "node_id": subnode["id"],
            "impact": subnode["impact"],
            "message": subnode["message"],
            "data": subnode["data"],
            "related_nodes": subnode["relatedNodes"],
            "node_type": node_type
        }

        if not insert_axe_subnodes(scan_event_id, url_id, json.dumps(subnode["data"]), subnode["id"], subnode["impact"], subnode["message"], node_type, subnode["relatedNodes"]):
            success = False
            logger.error(f"Failed to insert subnode at index {index} with data: {subnode}")
            time.sleep(5)

        processed_subnodes.append(processed_subnode)

    logger.info(f"Processing subnodes for {node_type} completed")
    return processed_subnodes if success else False

