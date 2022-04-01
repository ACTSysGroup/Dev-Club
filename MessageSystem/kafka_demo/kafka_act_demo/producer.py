# -*- coding: utf-8 -*-
 
import os
from io import BytesIO
from kafka.admin import KafkaAdminClient,NewTopic

import json
import avro.schema
from avro.io import DatumReader, DatumWriter, BinaryDecoder, BinaryEncoder
from avro.datafile import DataFileReader, DataFileWriter
from kafka import KafkaProducer
from time import sleep
from datetime import datetime
 
class AvroUtils(object):
    """avro序列化接口
    """
 
    REQUEST_SCHEMA = {}
    REQUEST_AVSC =  'hq_sample.avrc'
 
    @classmethod
    def init_schma(self, request_file=''):
        request_file = request_file or self.REQUEST_AVSC
        with open(request_file, 'r') as fileOpen:
            self.REQUEST_SCHEMA = avro.schema.Parse(fileOpen.read())
 
    @classmethod
    def avro_encode(self, json_data, schema=None):
        """avro 序列化json数据为二进制
        :param json_data:
        :param schema:
        :return:
        """
        bio = BytesIO()
        binary_encoder = BinaryEncoder(bio)
        dw = DatumWriter(writer_schema=schema or self.REQUEST_SCHEMA)
        dw.write(json_data, binary_encoder)
        return bio.getvalue()
 
    @classmethod
    def avro_decode(cls, binary_data, schema=None):
        """avro 反序列化二进制数据为json
        :param binary_data:
        :param schema:
        :return:
        """
        bio = BytesIO(binary_data)
        binary_decoder = BinaryDecoder(bio)
        return DatumReader(writer_schema=schema or self.REQUEST_SCHEMA).read(binary_decoder)

"""
{
"namespace":"aihpc.realtime",
"type":"record",
"name":"HangQing",
"fields":[
{"name":"LocalTimeStamp", "type":"int"},
{"name":"Time", "type":["long","null"]},
{"name":"Symbol", "type":"string"},
{"name":"ClosePrice", "type":["double", "null"]}
]
}
"""

def time_stick():
    time_now = datetime.now()
    hour = time_now.strftime('%H')
    minu = time_now.strftime('%M')
    sec = time_now.strftime('%S')
    msec = time_now.strftime('%f')
    hour = int(hour)
    minu = int(minu)
    sec = int(sec)
    msec = int(int(msec)/1000)
    return hour*10000000+minu*100000+sec*1000+msec


if __name__ == '__main__':
    topic = 'test200'
    brokers = "localhost:9092"
    admin_client = KafkaAdminClient(bootstrap_servers=brokers, client_id='test')
    topic_list = [(NewTopic(name=topic, num_partitions=3, replication_factor=1))]
    try:
        pass
        #admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except Exception as e:
        print(e)

    avroUtil = AvroUtils()
    avroUtil.init_schma("hq_sample.avrc")
    """
    ori_data = {'LocalTimeStamp':304,'Time':9820183,'Symbol':'lfj1314','ClosePrice':3304}
    bina_data = avroUtil.avro_encode(ori_data)
    print(bina_data)
    """
    producer = KafkaProducer(bootstrap_servers=brokers)
    count = 0
    while count < 300:
        ori_data = {'LocalTimeStamp':time_stick(),'Time':time_stick(),'Symbol':'lfj1314','ClosePrice':count}
        bina_data = avroUtil.avro_encode(ori_data)
        print("count: "+str(count)+" "+str(ori_data))
        producer.send(topic, bina_data)
        count += 1
        sleep(0.01)
    producer.close()
