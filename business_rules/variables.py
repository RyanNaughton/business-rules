import inspect
from functools import wraps

TYPE_NUMERIC = 'numeric'
TYPE_STRING = 'string'

class BaseVariables(object):
    """ Classes that hold a collection of variables to use with the rules
    engine should inherit from this.
    """
    @classmethod
    def get_all_variables(cls):
        methods = inspect.getmembers(cls, predicate=inspect.ismethod)
        return [{'name': m[0],
                 'description': m[1].description,
                 'return_type': m[1].return_type,
                 'options': m[1].options,
                } for m in methods if getattr(m[1], 'is_rule_variable', False)]


def rule_variable(return_type, description=None, options=None):
    """ Decorator to make a function into a rule variable
    """
    options = options or []
    def wrapper(func):
        func = _memoize_return_values(func)
        func.is_rule_variable = True
        func.description = description \
                or _fn_name_to_pretty_description(func.__name__)
        func.return_type = return_type
        func.options = options
        return func
    return wrapper

def _fn_name_to_pretty_description(name):
    return ' '.join([w.title() for w in name.split('_')])

def _memoize_return_values(func):
    """ Simple memoization (cacheing) decorator, copied from
    http://code.activestate.com/recipes/577219-minimalistic-memoization/
    """
    cache= {}
    @wraps(func)
    def memf(*args, **kwargs):
        key = (args, frozenset(kwargs.iteritems()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memf
