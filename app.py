from chalice import Chalice, Rate
from datetime import datetime, timedelta
from dateutil.tz import gettz
import io
import json
import os
from os.path import join, dirname
import pickle
from pprint import pprint
import sys
import time
import tweepy
from http.client import RemoteDisconnected

'''origin'''
from chalicelib import Hololive, PKL_BY_BOT3

### initialize
# # 本番アカウント
# # ###############################################################################
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

# twitter api V2 本番
Client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=CONSUMER_KEY, 
                        consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN, 
                        access_token_secret=ACCESS_TOKEN_SECRET, wait_on_rate_limit=True,)

# バケット名,オブジェクト名
BUCKET_NAME = os.environ.get('BUCKET_NAME')
# OBJECT_KEY_NAME = os.environ.get('OBJECT_KEY_NAME')

LAST_TW_FILE =  os.environ.get('BUCKET_NAME')
NOTICED_SPACE_FILE =  os.environ.get('BUCKET_NAME')
# # ###############################################################################
expansions_4search = ['invited_user_ids', 'speaker_ids', 'creator_id', 'host_ids']

space_fields_4search = ['host_ids', 'created_at', 'creator_id', 'id', 'lang',
                        'invited_user_ids', 'participant_count', 'speaker_ids', 'started_at',
                        'ended_at','subscriber_count', 'topic_ids', 'state', 'title', 
                        'updated_at', 'scheduled_start', 'is_ticketed']

user_fields_4search = ['created_at', 'description', 'entities', 'id', 'location', 
                        'name', 'pinned_tweet_id', 'profile_image_url', 'protected', 
                        'public_metrics', 'url', 'username', 'verified', 'withheld']

# # ###############################################################################

app = Chalice(app_name='Twitter-Space-NoticeBot')

# Automatically runs every 5 minutes
@app.schedule(Rate(6, unit=Rate.MINUTES))
def Main(event):
    pkl_by_bot3 = PKL_BY_BOT3(BUCKET_NAME)
    space_owner = Hololive().get_twitter_num().values()
    space_owner_convert2str = [str(i) for i in space_owner]
    try:
        search_result = search_live_space(space_owner_convert2str, expansions_4search, 
                                            space_fields_4search, user_fields_4search)
    except RemoteDisconnected as err:
        pprint(err)
        return
    
    if search_result[3]['result_count'] > 0:
        tw_result = None
        last_tw_id = None
        notices = None
        live_space_id = [{i['id']:i['title']} for i in search_result.data]
        for n in live_space_id:
            for id, title in n.items():
                notices = pkl_by_bot3.noticed_space_id_check(id, 'for-Twitter-Space-NoticeBot/noticed_space_id.pkl')
                if notices:
                    continue
                try:
                    last_tw_id = pkl_by_bot3.read_pkl('for-Twitter-Space-NoticeBot/last_tw_id.pkl')
                    message = f"<Twitter Space>\n\n{title}\n\nスペース展開中です!\n#ホロスペース\n\nhttps://twitter.com/i/spaces/{id}"
                    tw_result = Client.create_tweet(text=message, 
                                                    in_reply_to_tweet_id=last_tw_id if last_tw_id else None)
                    pkl_by_bot3.write_pkl(tw_result[0]['id'], 'for-Twitter-Space-NoticeBot/last_tw_id.pkl')
                    # TODO: 通知積みidを追記する
                    noticed_space_ids = pkl_by_bot3.read_pkl('for-Twitter-Space-NoticeBot/noticed_space_id.pkl')
                    pkl_by_bot3.postscript_pkl(id, 'for-Twitter-Space-NoticeBot/noticed_space_id.pkl', noticed_space_ids)
                except EOFError as err:
                    print(f'EOFError on load pickle file: {err}')
                time.sleep(1)
    else:
        print('条件に合うスペースはありません')



def search_live_space(space_owner_convert2str, expansions_4search, 
                        space_fields_4search, user_fields_4search):
    # live中のスペースidを取得
    search_result = Client.get_spaces(user_ids=space_owner_convert2str, expansions=expansions_4search,
                        space_fields=space_fields_4search, user_fields=user_fields_4search)
    return search_result

# if __name__ == '__main__':
#     pkl_by_bot3 = PKL_BY_BOT3('my-hololive-project')
#     pprint(pkl_by_bot3)