import functools
import inspect

def positional_only_factory(*positional_only_args):
    positional_only_args = set(positional_only_args)
    
    def positional_only(f):
        argspec = inspect.getargspec(f)
        assert all(arg in argspec.args for arg in positional_only_args)
        
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            bad_args = set(kwargs.keys()) & positional_only_args

            if bad_args:
                raise TypeError(
                    'You can only pass parameter %s as a positional argument' %
                    ', '.join(bad_args)
                )

            return f(*args, **kwargs)
    
        return wrapper
    
    return positional_only

@positional_only_factory('x')
def adder(x, y, z):
    return x + y + z

print adder(1, y=2, z=3)

@positional_only_factory('x', 'a')
def what(x, y, z):
    return x + y + z
