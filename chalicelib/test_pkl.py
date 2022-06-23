import pickle
from pprint import pprint

# with open('./last_tw_id_dev.pkl', 'rb') as f:
#     pprint(pickle.load(f))
    
with open('last_tw_id.pkl', 'wb') as f:
    pickle.dump('1535992196700454912', f)