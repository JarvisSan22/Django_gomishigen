from dataclasses import dataclass
from urllib import response
from django.shortcuts import render
import datetime
import hashlib
import json
from django.http import JsonResponse

# Create your views here.


class ShigenChian:
    def __init__(self,name,block_type,image_names,location, person, amount,units):
        self.chain = []
        self.create_block( 1, ["0"], block_type, image_names, location, person, amount, units)
        self.chain_name = name
        self.create_time = datetime.datetime.today()
        self.block_types=["raw","material","product"] 

    def create_block(self,nonce, connected_hashs,block_type,image_names,location, person, amount,units):

        block = {'index':len(self.chain)+1,
            'timestamp': str(datetime.datetime.now()),
            'nonce':nonce,
            'connected_hashs':connected_hashs,
            'connection_number':len(connected_hashs),
            #Stored info on block 
            'block_type':block_type,
            'image_names':image_names,
            'location':location,
            'person': person,
            'amount': amount,
            'unit':units,        
        }
        self.chain.append(block)

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_collection(self,previous_nonce):
        #currently just  proof of work 2022/08/27
        new_nonce = 1 
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                check_nonce = True
            else:
                new_nonce +=1
        return new_nonce

    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys= True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1 
        while block_index < len(chain):
            block = chain[block_index]
            for previous_nonce in block['connected_hashs']: #loop through all connections 
                if previous_nonce !=  self.hash(previous_block):
                    return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000': #origine block 
                return False
            previous_block = block
            block_index += 1
        return True


# Creating our Blockchain
block_type, image_names, location, person, amount, unit = "raw" ,"first_lid.jpg","nagoya","jarvis",1,"count"
ShigenChian=ShigenChian("Test Chain",block_type, image_names, location, person, amount, unit)

def mine_block(request):
    if request.method == "GET":
        previous_block = ShigenChian.get_previous_block()
        previous_nonce = previous_block['nonce']
        nonce = ShigenChian.proof_of_work(previous_block)
        #connected_hashs from ids to hash code 
        connected_hashs=[ShigenChian.hash(i) for i in request.get("connections")]
        assert request.get("block_type").lower in ShigenChian.block_type
        block_type=request.get("block_type").lower()
        image_names = request.get("image_names")
        location = request.get("location")
        person = request.get("person")
        amount = request.get("amount")
        units = request.get("units")
        block =ShigenChian.create(nonce, connected_hashs,block_type,image_names,location, person, amount,units)

        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'nonce': block['nonce'],
                    'connected_hashs': block['connected_hashs']}
    return JsonResponse(response)


# Getting the full chian; 
def get_chain(request):
    if request.method == 'GET':
        response = {'chain':ShigenChian.chain,
        'length':len(ShigenChian.chain)
            }
    return JsonResponse(response)

def is_valid(request):
    if request.method =="GET":
        is_valid = ShigenChian.is_chain_valid()
        if is_valid:
            response = {'message': 'ALL is valid'}
        else:
            response = {'message': 'problem in the chain'}

    return JsonResponse(response)
