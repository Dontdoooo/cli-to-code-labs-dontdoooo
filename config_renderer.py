import argparse
import csv
import json
import os
import xml.etree.ElementTree as ET
from typing import Any, Dict, List

from jinja2 import Template


def load_template(template_path: str) -> Template:
    """Load and return a Jinja2 Template from `template_path`.

    Args:
        template_path: Path to the .j2 template file.

    Returns:
        A compiled Jinja2 `Template` instance.
    """
    with open(template_path, encoding="utf-8") as f:
        return Template(f.read())


def load_inventory(inventory_path: str, fmt: str) -> List[Dict[str, Any]]:
    """Load inventory data from a file in CSV, JSON, or XML format.

    Args:
        inventory_path: Path to the inventory file.
        fmt: Format of the inventory file: 'csv', 'json', or 'xml'.

    Returns:
        A list of dictionaries with inventory items.

    Raises:
        FileNotFoundError: If `inventory_path` does not exist or cannot be opened.
        ValueError: If `fmt` is not one of the supported formats.
    """
    try:
        with open(inventory_path, "r", encoding="utf-8") as f:
            if fmt == "json":
                data = json.load(f)
                if isinstance(data, list):
                    return data
                if isinstance(data, dict):
                    # If a dict of devices, return its values as a list
                    return list(data.values())
                return [data]

            if fmt == "csv":
                reader = csv.DictReader(f)
                return [dict(row) for row in reader]

            if fmt == "xml":
                tree = ET.parse(f)
                root = tree.getroot()
                items: List[Dict[str, Any]] = []
                for child in root:
                    item: Dict[str, Any] = {}
                    # include attributes
                    item.update(child.attrib)
                    for sub in child:
                        item[sub.tag] = sub.text
                    items.append(item)
                return items

            raise ValueError(f"Unsupported inventory format: {fmt}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Inventory file not found: {inventory_path}") from e


def render_configs(template: Template, inventory: List[Dict[str, Any]], output_dir: str) -> None:
    """Render configuration files from a Jinja2 template and inventory items.

    Args:
        template: Compiled Jinja2 Template to render.
        inventory: List of dicts containing device variables.
        output_dir: Directory to write rendered files into.
    """
    os.makedirs(output_dir, exist_ok=True)

    for idx, item in enumerate(inventory, start=1):
        name = (
            item.get("hostname")
            or item.get("name")
            or item.get("host")
            or item.get("device")
            or f"device_{idx}"
        )
        filename = os.path.join(output_dir, f"{name}.cfg")
        rendered = template.render(**item)
        with open(filename, "w", encoding="utf-8") as out_f:
            out_f.write(rendered)
        print(f"Rendered: {filename}")


def main(argv: List[str] | None = None) -> int:
    """Command-line entry point for the renderer.

    Parses arguments, loads template and inventory, and renders configs.

    Args:
        argv: Optional list of arguments to parse (defaults to sys.argv).

    Returns:
        Exit code (0 on success).
    """
    parser = argparse.ArgumentParser(description="Render configs from a Jinja2 template and inventory")
    parser.add_argument("--template", required=True, help="Path to the .j2 template file")
    parser.add_argument("--inventory", required=True, help="Path to the inventory file")
    parser.add_argument(
        "--format",
        required=True,
        choices=["csv", "json", "xml"],
        help="Inventory format (csv, json, xml)",
    )
    parser.add_argument("--output-dir", default=None, help="Output directory for rendered configs")

    args = parser.parse_args(argv)

    tpl = load_template(args.template)
    inventory = load_inventory(args.inventory, args.format)
    output_dir = args.output_dir or f"./rendered_{args.format}"
    render_configs(tpl, inventory, output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())