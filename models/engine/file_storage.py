#!/usr/bin/env python3

from models import *
import json
import os



class FileStorage:
    """ File Storage class """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ Returns the dictionary __objects """
        if cls:
            return {k: v for k, v in self.__objects.items()
                    if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """ Sets in __objects the obj with key <obj class name>.id """
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """ Serializes __objects to the JSON file """
        with open(self.__file_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """ Deserializes the JSON file to __objects """

        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r") as f:
                data = json.load(f)
                for value in data.values():
                    self.new(eval(value["__class__"])(**value))

    def delete(self, obj=None):
        """ Deletes an object from __objects """
        if obj:
            key = obj.__class__.__name__ + "." + obj.id
            del self.__objects[key]
            self.save()

    def close(self):
        """ Calls reload() method for deserializing the JSON file to objects """
        self.reload()
