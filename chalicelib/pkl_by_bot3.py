import boto3
import pickle

'''
s3のpklファイルを扱うためのクラス
'''
class PKL_BY_BOT3:
    def __init__(self, bucket_name):
        self.BUCKET_NAME = bucket_name
        # self.OBJECT_KEY_NAME = object_key_name

    def get_s3object(self, object_key_name):
        s3 = boto3.resource('s3')
        s3_object = s3.Object(self.BUCKET_NAME, object_key_name)
        return s3_object
        # pprint(pickle.loads(s3_object['Body'].read()))
        # return pickle.loads(s3_object['Body'].read())

    def read_pkl(self, object_key_name):
        s3_object = self.get_s3object(object_key_name).get()
        return pickle.loads(s3_object['Body'].read())

    def noticed_space_id_check(self, space_id, object_key_name):
        noticed_space_id_list = None
        try:
            noticed_space_id_list = self.read_pkl(object_key_name)
        except EOFError as err:
            print(f'EOFError on load pickle file: {err}')
                
        if space_id in noticed_space_id_list:
            return True
        else:
            return False

    def write_pkl(self, data, object_key_name):
        pickle_byte_obj = pickle.dump(data)
        s3_object = self.get_s3object(object_key_name)
        s3_object.put(Body=pickle_byte_obj)
        
    def postscript_pkl(self, data, object_key_name, noticed_space_id: list):
        noticed_space_id.append(data)
        pickle_byte_obj = pickle.dump(noticed_space_id)
        s3_object = self.get_s3object(object_key_name)
        s3_object.put(Body=pickle_byte_obj)







# def read_noticed_space_id(NOTICED_SPACE_FILE):
#     try:
#         with open(NOTICED_SPACE_FILE, 'rb') as f:
#             noticed_space_id_list = pickle.load(f)
#             return noticed_space_id_list
#     except EOFError as err:
#             print(f'EOFError on load pickle file: {err}')
