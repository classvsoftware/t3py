from t3py.interfaces.routes import T3Route
from t3py.interfaces.t3py_context import T3pyContext


exit_route: T3Route = T3Route(name="Exit")

def exit_function(*, t3py_config: T3pyContext):
    pass