from .groups import router as group_router
from .educational_forms import router as ef_router
from .faculties import router as f_router


routers = [group_router, ef_router, f_router]