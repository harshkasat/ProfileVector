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

    
    def _extract(*arg, **kwargs) -> dict:
        DataFromGithub = kwargs['data']
        DataFromGithubSocial = kwargs['social_links']
        Data = ""
        Data += f"twitter {DataFromGithubSocial['twitter_url']} \n"
        Data += f"linkedin {DataFromGithubSocial['linkedin_url']} \n"
        for (k, v) in DataFromGithub.items():
            if k in DataNeeded:
                Data += f" {k} {v} \n"
                if k == 'blog':
                    Data += f'personal website {v} \n'
        print(f"User Info successfully extracted.")
        return Data
 