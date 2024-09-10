import json
DataNeeded = [
    "name",
    "location",
    "email",
    "public_repos",
    "followers",
    "following",
    "created_at",
    "avatar_url",
    "bio",
    "company",
    "blog",
]

class Helper(object):

    
    def _extract(*args, **kwargs) -> dict:
        DataFromGithub = kwargs['data']
        Data = {}
        for (k, v) in DataFromGithub.items():
            if k in DataNeeded:
                Data[k] = v
        
        return Data