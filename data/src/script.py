from config.psql import conn
from data_utils.vacant_properties import vacant_properties
from data_utils.priority_level import priority_level
from data_utils.access_process import access_process
from data_utils.city_owned_properties import city_owned_properties
from data_utils.phs_properties import phs_properties
from data_utils.l_and_i import l_and_i
from data_utils.rco_geoms import rco_geoms
from data_utils.tree_canopy import tree_canopy
from data_utils.nbhoods import nbhoods
from data_utils.gun_crimes import gun_crimes
from data_utils.drug_crimes import drug_crimes
from data_utils.deliquencies import deliquencies
from data_utils.opa_properties import opa_properties
from data_utils.unsafe_buildings import unsafe_buildings
from data_utils.imm_dang_buildings import imm_dang_buildings
from data_utils.tactical_urbanism import tactical_urbanism
from data_utils.conservatorship import conservatorship
from data_utils.llc_owner import llc_owner
import sys


# Ensure the directory containing awkde is in the Python path
awkde_path = "/usr/src/app"
if awkde_path not in sys.path:
    sys.path.append(awkde_path)

services = [
    city_owned_properties,
    phs_properties,
    l_and_i,
    rco_geoms,
    tree_canopy,
    nbhoods,
    gun_crimes,
    drug_crimes,
    deliquencies,
    opa_properties,
    unsafe_buildings,
    imm_dang_buildings,
    tactical_urbanism,
    conservatorship,
    llc_owner,
]


# Load Vacant Property Data
dataset = vacant_properties()

# Load and join other datasets
for service in services:
    dataset = service(dataset)

# Add Priority Level
dataset = priority_level(dataset)

# Add Access Process
dataset = access_process(dataset)


# Post to Mapbox
dataset.build_and_publish_pmtiles("vacant_properties_tiles")

# Finalize in Postgres
dataset.gdf.to_postgis("vacant_properties_end", conn, if_exists="replace", index=False)
conn.commit()
conn.close()
