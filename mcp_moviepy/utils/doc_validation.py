from functools import wraps
import inspect

def ensure_doc_reference(func):
    """
    Decorator to ensure that a function's docstring contains a reference to the local
    'html/' documentation directory, adhering to the project's product guidelines.
    """
    if func.__doc__ is None:
        raise ValueError("Function must have a docstring")
    
    if "html/" not in func.__doc__:
        raise ValueError("Docstring must contain a reference to 'html/'")
        
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    return wrapper
