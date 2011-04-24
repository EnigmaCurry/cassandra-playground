import pycassa

# This is a reusable cassandra config.
# Requires a configuration dictionary:
# config = dict(
#     host = "localhost:9160",
#     keyspace = "my_keyspace",
#     column_families = dict(
#         ColumnFamily1 = {"comparator_type":pycassa.LONG_TYPE},
#         ColumnFamily2 = {}
#         )
#     )

def drop_create_keyspace(config):
    cas = pycassa.SystemManager(config["host"])
    try:
        cas.drop_keyspace(config["keyspace"])
    except pycassa.InvalidRequestException:
        pass
    cas.create_keyspace(config["keyspace"], replication_factor=1)
    
    #Column Families:
    for cf, args in config["column_families"].items():
        cas.create_column_family(config["keyspace"], cf, **args)
    cas.close()
    
def create_pool(config):
    pool = pycassa.ConnectionPool(
        config["keyspace"], server_list=[config["host"]])
    return pool

def connect(config):
    """Connect to the keyspace and discover all the ColumnFamilies"""
    global pool
    pool = create_pool(config)
    cas = pool.get()
    column_families = {}
    for cf in cas.get_keyspace_description():
        column_families[cf] = pycassa.ColumnFamily(pool,cf)
    cas.return_to_pool()
    globals().update(column_families)

def recreate_default_namespace():
    """Drop and re-create the default configured namespace"""
    import model
    drop_create_keyspace(model.db_config)
