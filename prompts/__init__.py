"""提示词模块"""

from .image_prompts import IMAGE_SYSTEM_PROMPT, get_image_prompt
from .solver_prompts import SOLVER_SYSTEM_PROMPT, get_solver_prompt

__all__ = [
    'IMAGE_SYSTEM_PROMPT',
    'get_image_prompt',
    'SOLVER_SYSTEM_PROMPT',
    'get_solver_prompt'
]