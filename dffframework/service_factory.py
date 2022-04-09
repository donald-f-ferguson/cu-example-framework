from episode_resource import EpisodesResource, MongoDBResource

_service_cache = dict()

def get_service(service_name):
    global _service_cache

    result_svc = _service_cache.get(service_name, None)

    if result_svc is None:

        if service_name == "episodes":
            config_info = {"database": "CU_Example_GoT"}
            d_service = MongoDBResource(config_info)
            s_service = EpisodesResource(d_service, "episodes", "/episodes", None)

            _service_cache["episodes"] = s_service
            result_svc = s_service

    return result_svc


