from .agents.max_safe import MaxSafe
from .agents.max_risk import MaxRisk
from .agents.rand_safe import RandSafe
from .agents.rand_risk import RandRisk
from .agents.int_max_safe import IntMaxSafe
from .agents.int_max_risk import IntMaxRisk
from .agents.int_rand_safe import IntRandSafe
from .agents.int_rand_risk import IntRandRisk
from .agents.int_super_safe import IntSuperSafe

AGENT_CLASSES = {"MaxSafe": MaxSafe,
                 "MaxRisk": MaxRisk,
                 "RandSafe": RandSafe,
                 "RandRisk": RandRisk,
                 "IntMaxSafe": IntMaxSafe,
                 "IntMaxRisk": IntMaxRisk,
                 "IntRandSafe": IntRandSafe,
                 "IntRandRisk": IntRandRisk,
                 "IntSuperSafe": IntSuperSafe}                
