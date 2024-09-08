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

    def _save(*args, **kwargs) -> None:
        
        data = kwargs.get('data')
        filename = data['filename']
        json_data = data['extracted_data']
        with open('{}.json'.format(filename), 'w') as f:
            json.dump(json_data, f, indent=True)
        print(f'Data saved to {filename}.json')
    
    def _extract(*args, **kwargs) -> dict:
        DataFromGithub = kwargs['data']
        Data = {}
        for (k, v) in DataFromGithub.items():
            if k in DataNeeded:
                Data[k] = v
        
        return Data