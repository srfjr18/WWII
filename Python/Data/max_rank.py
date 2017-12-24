#!/usr/bin/env python
import pickle, os

path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)), 'userdata')
with open(path, "rb") as file:
    data = pickle.load(file)
                    
data["rank"] = 834

with open(path, "wb+") as file:
    pickle.dump(data, file, protocol=2)
