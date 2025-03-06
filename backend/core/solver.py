"""题目求解模块"""

from typing import Generator, Tuple, Optional, Any
from openai import OpenAI

from backend.config.settings import settings
from backend.logger.log_config import logger
from backend.core.utils import convert_formula_format
from backend.core.image_processor import image_processor
from prompts.solver_prompts import SOLVER_SYSTEM_PROMPT, get_solver_prompt

class ProblemSolver:
    """题目求解类"""
    def __init__(self):
        """初始化OpenAI客户端"""
        self.client = OpenAI(
            base_url=settings.api_base_url,
            api_key=settings.api_key,
        )

    def _update_output(
        self,
        content: str,
        current_output: list,
        replace_last: bool = False,
        add_separator: bool = True
    ) -> Generator[Tuple[str, str], None, None]:
        """
        更新输出内容
        
        Args:
            content: 新内容
            current_output: 当前输出列表
            replace_last: 是否替换最后一个内容
            add_separator: 是否添加分隔符
            
        Yields:
            Tuple[str, str]: (输出内容, 日志内容)
        """
        # 如果是替换最后一个内容，先移除
        if replace_last and current_output:
            current_output.pop()
        
        # 添加新内容
        content_with_separator = content + ("\n\n---\n\n" if add_separator else "")
        current_output.append(content_with_separator)
        
        # 只显示实际内容，不显示API调用记录
        yield "\n\n".join(current_output).rstrip('---\n\n'), ""

    def solve_problem(
        self,
        text_input: str,
        image: Optional[Any] = None,
        is_complex_mode: bool = False
    ) -> Generator[Tuple[str, str], None, None]:
        """
        处理完整题目求解流程
        
        Args:
            text_input: 题目文本
            image: 题目图片（可选）
            is_complex_mode: 是否使用复杂模式
            
        Yields:
            Tuple[str, str]: (解答内容, 日志内容)
        """
        api_logs = []
        full_result = []
        current_output = []
        
        # 处理图片描述
        if image is not None:
            try:
                description_gen = image_processor.get_image_description(
                    text_input, image, is_complex_mode
                )
                latest_desc = []
                
                # 处理流式输出
                for desc in description_gen:
                    if isinstance(desc, tuple):  # 如果是最终结果
                        final_desc, _ = desc
                        if "出错" in final_desc:  # 如果是错误信息
                            api_logs.append(f"# API调用错误\n{final_desc}")
                            yield final_desc, "\n\n".join(api_logs)
                            return
                        latest_desc = [final_desc]
                    else:  # 流式输出的部分内容
                        latest_desc = [desc]
                        yield from self._update_output(
                            f"# 图片描述\n\n{desc}",
                            current_output,
                            replace_last=True
                        )
                
                if latest_desc:
                    full_result.append(latest_desc[0])
                    logger.logger.info("图片描述完成")
                else:
                    raise Exception("未获取到图片描述")
                    
            except Exception as e:
                error_msg = f"图片处理出错：{str(e)}"
                logger.log_error(error_msg)
                yield error_msg, ""
                return
        
        # 获取求解器模型
        _, solver_model = settings.get_model_info(is_complex_mode)
        yield from self._update_output(
            f"# {solver_model} 求解过程\n\n",
            current_output,
            add_separator=True
        )
        
        # 构建完整问题描述
        full_problem = get_solver_prompt(text_input, full_result[0] if full_result else None)
        
        # 构建消息
        messages = [
            {
                "role": "system",
                "content": SOLVER_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": full_problem
            }
        ]
        
        try:
            # 根据模式决定是否添加 reasoning_effort
            if is_complex_mode and solver_model == "o3-mini":
                stream = self.client.chat.completions.create(
                    model=solver_model,
                    messages=messages,
                    reasoning_effort="high",
                    stream=True,
                    temperature=0.01
                )
            else:
                stream = self.client.chat.completions.create(
                    model=solver_model,
                    messages=messages,
                    stream=True,
                    temperature=0.01
                )
                
            # 流式接收并更新输出
            collected_chunks = []
            buffer = []
            formula_buffer = []
            in_formula = False
            latex_start = ""  # 记录LaTeX公式的开始标记
            
            try:
                for chunk in stream:
                    if not (hasattr(chunk, 'choices') and
                           chunk.choices and
                           hasattr(chunk.choices[0], 'delta') and
                           hasattr(chunk.choices[0].delta, 'content') and
                           chunk.choices[0].delta.content is not None):
                        continue
                        
                    content = chunk.choices[0].delta.content
                    collected_chunks.append(content)
                    
                    # 处理LaTeX公式
                    for char in content:
                        if not in_formula:
                            if char == '\\':
                                latex_start = char
                                continue
                            elif latex_start:
                                latex_start += char
                                if latex_start == "\\[" or latex_start == "\\(":
                                    in_formula = True
                                    formula_buffer = []
                                    buffer.append("$$" if latex_start == "\\[" else "$")
                                    latex_start = ""
                                elif len(latex_start) > 1:
                                    buffer.extend(list(latex_start))
                                    latex_start = ""
                            else:
                                buffer.append(char)
                        else:
                            formula_buffer.append(char)
                            if (len(formula_buffer) >= 2 and
                                formula_buffer[-2] == '\\' and
                                formula_buffer[-1] == ']'):
                                in_formula = False
                                buffer.extend(formula_buffer[:-2])
                                buffer.append("$$")
                                formula_buffer = []
                            elif (len(formula_buffer) >= 2 and
                                  formula_buffer[-2] == '\\' and
                                  formula_buffer[-1] == ')'):
                                in_formula = False
                                buffer.extend(formula_buffer[:-2])
                                buffer.append("$")
                                formula_buffer = []
                    
                    # 输出当前缓冲区内容
                    if buffer:
                        current_content = f"# {solver_model} 求解过程\n\n{''.join(buffer)}"
                        yield from self._update_output(
                            current_content,
                            current_output,
                            replace_last=True
                        )
                
                if not collected_chunks:
                    raise Exception("未收到模型响应")
                    
                # 生成最终输出和日志
                final_content = f"# {solver_model} 求解过程\n\n{''.join(buffer)}"
                log_str = logger.log_api_interaction(solver_model, messages, final_content)
                logger.logger.info(f"{solver_model} 求解完成")
                full_result.append(final_content)
                
            except Exception as e:
                error_msg = f"模型响应处理出错：{str(e)}"
                logger.log_error(f"Stream处理错误 - 模型: {solver_model}, 错误: {str(e)}")
                yield from self._update_output(
                    f"# {solver_model} 求解出错\n\n{error_msg}",
                    current_output,
                    add_separator=True
                )
        
        except Exception as e:
            error_msg = f"模型 {solver_model} 求解出错：{str(e)}"
            logger.log_error(error_msg)
            yield from self._update_output(
                f"# {solver_model} 求解出错\n\n{error_msg}",
                current_output,
                add_separator=True
            )

# 创建全局求解器实例
problem_solver = ProblemSolver()