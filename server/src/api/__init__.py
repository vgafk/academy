from .groups import router as g_router
from .educational_forms import router as ef_router
from .faculties import router as f_router
from .sub_groups import router as sg_router
from .teachers import router as t_router
from .discipline import router as d_router
from .schedule import router as sch_router
from .students import router as s_router
from .attendance import router as a_router

routers = [g_router, ef_router, f_router, sg_router, t_router, d_router, sch_router, s_router, a_router]
