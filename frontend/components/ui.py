"""前端UI组件"""

import os
import gradio as gr
from pathlib import Path
from typing import Generator, Tuple

from backend.core.solver import problem_solver
from backend.core.utils import save_solution
from backend.config.settings import settings

class SolverUI:
    """求解器UI类"""
    def __init__(self):
        """初始化UI组件"""
        self.css_path = Path(__file__).parent.parent / 'styles' / 'main.css'
        with open(self.css_path, 'r', encoding='utf-8') as f:
            self.custom_css = f.read()

    def create_interface(self) -> gr.Blocks:
        """创建Gradio界面"""
        with gr.Blocks(css=self.custom_css) as iface:
            with gr.Column(elem_classes="container"):
                gr.Markdown("# 理论力学习题求解助手", elem_classes="title")
                
                with gr.Row():
                    with gr.Column(scale=1, elem_classes="input-column"):
                        # 模式选择
                        mode_select = gr.Checkbox(
                            label="启用复杂问题求解模式",
                            value=False,
                            info=self._get_mode_info()
                        )
                        
                        # 题目输入
                        text_input = gr.Textbox(
                            label="题目文字描述",
                            lines=5,
                            placeholder="请输入题目文字描述...",
                        )
                        
                        # 图片输入
                        image_input = gr.Image(
                            label="题目图片（可选）",
                            type="pil",
                        )
                        
                        # 按钮组
                        with gr.Row(elem_classes="button-row"):
                            solve_btn = gr.Button("求解")
                            save_btn = gr.Button("下载结果")
                            file_output = gr.File(label="下载解答文件（包含图片）")
                
                # 输出区域
                with gr.Column(scale=1, elem_classes="output-column"):
                    self._add_output_styles()
                    
                    # 状态指示器
                    status_indicator = gr.HTML(
                        value=self._get_status_html("准备求解"),
                        elem_classes="status-indicator status-preparing"
                    )
                    
                    with gr.Group(visible=True):
                        solution_output = gr.Markdown(
                            label="求解过程",
                            elem_classes="output-box",
                            show_label=False
                        )
                    
                    # 隐藏日志输出
                    log_output = gr.Markdown(visible=False)
            
            # 设置事件处理
            solve_btn.click(
                fn=self._handle_solve,
                inputs=[text_input, image_input, mode_select],
                outputs=[solution_output, log_output, status_indicator],
                scroll_to_output=True,
            )
            
            save_btn.click(
                fn=self._handle_save,
                inputs=[text_input, image_input, solution_output],
                outputs=file_output
            )
        
        return iface

    def _get_status_html(self, status: str) -> str:
        """生成状态HTML"""
        status_map = {
            "准备求解": "preparing",
            "正在思考": "thinking",
            "正在求解": "solving",
            "求解完成": "completed"
        }
        status_class = status_map.get(status, "preparing")
        return f'<div class="status-indicator status-{status_class}">{status}</div>'

    def _get_mode_info(self) -> str:
        """获取模式信息提示"""
        simple_image, simple_solver = settings.get_model_info(False)
        complex_image, complex_solver = settings.get_model_info(True)
        return (f"简单模式：使用 {simple_image} 解析图片，{simple_solver} 求解\n"
                f"复杂模式：使用 {complex_image} 解析图片，{complex_solver} 求解")

    def _add_output_styles(self):
        """添加输出样式"""
        gr.HTML("""<style>
            .output-column {
                height: calc(100vh - 100px);
            }
            @media (max-width: 768px) {
                .output-column {
                    height: auto;
                    min-height: 500px;
                }
            }
            </style>""")

    def _handle_solve(self, text_input, image_input, is_complex_mode):
        """处理求解请求"""
        current_solution = ""
        current_log = ""
        status_html = self._get_status_html("准备求解")
        has_started_solving = False
        
        try:
            # 更新状态为"正在思考"
            yield gr.update(value=""), gr.update(value=""), gr.update(value=self._get_status_html("正在思考"))
            
            # 使用 yield 实现流式输出
            for step in problem_solver.solve_problem(text_input, image_input, is_complex_mode):
                if isinstance(step, tuple):
                    solution, log = step
                    if solution:
                        current_solution = solution
                    if log:
                        current_log = log
                else:
                    current_solution = step
                
                # 当开始接收到模型输出时，更新状态为"正在求解"
                if not has_started_solving and current_solution.strip():
                    has_started_solving = True
                    status_html = self._get_status_html("正在求解")
                
                # 使用 gr.update() 来更新输出
                yield (gr.update(value=current_solution),
                      gr.update(value=current_log),
                      gr.update(value=status_html))
            
            # 求解完成后更新状态
            status_html = self._get_status_html("求解完成")
            yield (gr.update(value=current_solution),
                  gr.update(value=current_log),
                  gr.update(value=status_html))
                
        except Exception as e:
            error_msg = f"处理出错：{str(e)}"
            yield (gr.update(value=error_msg),
                  gr.update(value=f"错误：{str(e)}"),
                  gr.update(value=self._get_status_html("求解完成")))

    def _handle_save(self, text_input, image_input, solution_content):
        """处理保存请求"""
        try:
            zip_path, zip_name = save_solution(text_input, image_input, solution_content)
            return zip_path
        except Exception as e:
            return None

    def launch(self, **kwargs):
        """启动界面"""
        interface = self.create_interface()
        if settings.auth_enabled:
            kwargs['auth'] = settings.verify_auth
            
        interface.queue()  # 启用队列模式
        interface.launch(**kwargs)  # 启动界面

# 创建全局UI实例
solver_ui = SolverUI()