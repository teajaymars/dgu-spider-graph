import json
import re

def simplify(url):
    assert (type(url) is str or type(url) is unicode), type(url)
    url = re.sub( r'(data.gov.uk/apps/)[^/]*$', 'data.gov.uk/apps/<APP_NAME>', url )
    url = re.sub( r'(data.gov.uk/blog/)[^/]*$', 'data.gov.uk/blog/<BLOG_NAME>', url )
    url = re.sub( r'(data.gov.uk/data-requests/)[^/]*$', 'data.gov.uk/data-requests/<DATA_REQUEST_NAME>', url )
    url = re.sub( r'(data.gov.uk/forum/)[^/]*$', 'data.gov.uk/forum/<FORUM_NAME>', url )
    url = re.sub( r'(data.gov.uk/forum/)[^/]*/[^/]*$', 'data.gov.uk/forum/<FORUM_NAME>/<POST_NAME>', url )
    url = re.sub( r'(data.gov.uk/ideas/)[^/]*$', 'data.gov.uk/ideas/<IDEA_NAME>', url )
    url = re.sub( r'(data.gov.uk/library/)[^/]*$', 'data.gov.uk/library/<LIBRARY_NAME>', url )
    url = re.sub( r'(data.gov.uk/profile/)[^/]*$', 'data.gov.uk/profile/<PROFILE_NAME>', url )
    url = re.sub( r'(data.gov.uk/publisher/)[^/]*$', 'data.gov.uk/publisher/<PUBLISHER_NAME>', url )
    url = re.sub( r'(data.gov.uk/user/)[^/]*/track$', 'data.gov.uk/user/<USER_NAME>/track', url )
    url = re.sub( r'(data.gov.uk/users/)[^/]*/track$', 'data.gov.uk/users/<USER_NAME>/track', url )
    url = re.sub( r'(data.gov.uk/user/)[^/]*$', 'data.gov.uk/user/<USER_NAME>', url )
    url = re.sub( r'(data.gov.uk/users/)[^/]*$', 'data.gov.uk/users/<USER_NAME>', url )
    url = re.sub( r'\?.*', '', url )
    url = re.sub( r'http...data.gov.uk', '', url )
    return url

def dump_simplified_urls(data):
    data = set( [simplify(x['url']) for x in data] )
    with open('simplified_urls.txt','w') as f:
        for x in sorted(list(data)):
            f.write(x)
            f.write('\n')

def build_simplified_graph(data):
    raw_items = set()
    raw_edges = set()
    for entry in data:
        _from = simplify(entry['url'])
        raw_items.add(_from)
        for link in entry['local_links']:
            _to = simplify(link['url'])
            raw_edges.add((_from,_to))
    orphans = set()
    items = sorted(list(raw_items))
    item_idx = { items[i]:i for i in range(len(items)) }
    edges = []
    for _from,_to in raw_edges:
        if _to in item_idx:
            edges.append((item_idx[_from],item_idx[_to]))
        else:
            orphans.add(_to)
    graphdata = {'items':items,'edges':edges,'orphans':sorted(list(orphans))}
    with open('test/graphdata.json','w') as f:
        json.dump(graphdata,f)
    return graphdata

def ubigraph(graphdata):
    # Extract vertices to busy edges
    THRESHOLD = 50 # incoming edges would be grounds for ignoring
    freq = {}
    for _from,_to in graphdata['edges']:
        freq[_to] = freq.get(_to,0) + 1
    busy = set([ idx for idx,count in freq.items() if count>THRESHOLD ])
    # connect to server
    import xmlrpclib
    server_url = 'http://127.0.0.1:20738/RPC2'
    server = xmlrpclib.Server(server_url)
    G = server.ubigraph
    G.clear()
    for i in range(len(graphdata['items'])):
        node = G.new_vertex_w_id(i)
        if i in busy:
            G.set_vertex_attribute(i, 'color', '#ff0000')
        G.set_vertex_attribute(i, 'size', str(tween(freq[i]/30)))
        #G.set_vertex_attribute(i, 'label', graphdata['items'][i])
    for a,b in graphdata['edges']:
        if b in busy:
            continue
        G.new_edge(a,b)
        pass

def tween(x):
    import math
    return 1+(math.log(x+1))

def debugGraph():
    items = [
       'Dennis',
       'Michael',
       'Jessica',
       'Timothy',
       'Barbara',
       'Franklin',
       'Monty',
       'James',
       'Bianca',
    ]
    edges = [(2,7),(0,1)]
    with open('test/graphdata.json','w') as f:
        json.dump({'items':items,'edges':edges},f)


