import logging
import shutil
from pathlib import Path

from stactools.sentinel5p import stac

logging.basicConfig(level=0)
logging.getLogger("fsspec").propagate = False

root = Path(__file__).parents[1]
examples = root / "examples"
data_files = root / "tests" / "data-files"

# if examples.exists():
#     shutil.rmtree(examples)

# examples.mkdir()

for path in data_files.glob("*.nc"):
    item = stac.create_item(str(path))
    item.set_self_href(str(examples / item.id) + ".json")
    item.make_asset_hrefs_relative()
    item.save_object(include_self_link=False)
