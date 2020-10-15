import mwapi
import pandas as pd

session = mwapi.Session('https://en.wikipedia.org', user_agent='aysha.kamal7')

data_list = []
missed = []

_gapcontinue = ''
_continue = ''

while True:
    params = {'action':'query',
            'generator':'allpages',
            'gapnamespace':828,
            'gaplimit':'max',
            'format':'json',
            'prop':'info',
            'inprop':'url',
            'gapcontinue': _gapcontinue,
            'continue': _continue,
            }
    
    result = session.get(params)

    for page in list(result['query']['pages'].values()):
        try:
            
            pageid = page['pageid']
            title = page['title']
            touched = page['touched']
            length = page['length']
            url = page['fullurl']
            revid = page['lastrevid']
            
            params = {'action':'query',
                    'format':'json',
                    'prop':'revisions',
                    'revids':revid,
                    'rvprop':'content',
                    'rvslots':'main',
                    'formatversion':2
                    }
    
            rev_result = session.get(params)

            content_info = rev_result['query']['pages'][0]['revisions'][0]['slots']['main']
            content = content_info['content']
            content_model = content_info['contentmodel']
            content_format = content_info['contentformat']
            
            data_list.append([pageid, title, url, length, content, content_format, content_model, touched])
        except:
            if 'title' in page.keys():
                missed+=page['title']

    try:
        _continue = result['continue']['continue']
        _gapcontinue = result['continue']['gapcontinue'] if 'gapcontinue' in  result['continue'] else ''       
    except:
        break

print(data_list)

## Create the dataframe
data_df = pd.DataFrame(data_list, columns=['id', 'title', 'url', 'length', 'content', 'format', 'model', 'touched'])

## Save dataframe
data_df.to_csv('wiki_ns.csv', index=False)