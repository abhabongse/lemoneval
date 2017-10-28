# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

def to_json(o):
    """Serialize object into JSON string."""
    import json
    def _default(obj):
        if hasattr(obj, "jsonable_class"):
            obj_class = obj.jsonable_class
            if hasattr(obj, "json_serialize"):
                obj_args = obj.json_serialize()
            else:
                obj_args = obj.__dict__
            return dict(__class__=obj_class, __value__=obj_args)
        return obj.__dict__
    return json.dumps(o, indent=2, default=_default)


def from_json(s, target_classes):
    """Return python object from JSON string."""
    import json
    def _object_hook(obj):
        try:
            obj_class = target_classes[obj["__class__"]]
            obj_args = obj["__value__"]
        except:
            return obj
        else:
            return obj_class(**obj_args)
    return json.loads(s, object_hook=_object_hook)
