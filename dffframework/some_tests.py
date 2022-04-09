
from dffframework.mongo_db_data_resource import MongoDBResource
from dffframework.base_application_resource import BaseApplicationResource
from episode_resource import EpisodesResource

import json


def t1():
    config_info = {"database": "CU_Example_GoT"}
    m_resource = MongoDBResource(config_info)
    colls = m_resource.get_resource_names()
    print(colls)


def t2():
    config_info = {"database": "CU_Example_GoT"}
    m_resource = MongoDBResource(config_info)

    template = {'seasonNum': 3}
    field_list = ['seasonNum', 'episodeNum', 'episodeAirDate', 'episodeTitle', 'episodeLink']
    docs = m_resource.get_by_template('episodes', template, field_list)
    print(json.dumps(docs, indent=2, default=str))

def t3():
    config_info = {"database": "CU_Example_GoT"}
    m_resource = MongoDBResource(config_info)
    ba = EpisodesResource(data_service=m_resource, data_resource_name="episodes",
                          resource_path="/episodes", config_info=None)
    result = ba.get_by_template(
        {"seasonNum": 2},
        None
    )
    print(json.dumps(result, indent=2, default=str))



if __name__ == "__main__":
    # TODO I hate doing things this way. It is sloppy.
    #t1()
    #t2()
    t3()
    pass
