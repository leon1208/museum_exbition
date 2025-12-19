"""
AI处理模块，用于调用千问大模型处理用户信息
"""
from typing import Dict, Any, List
import json
import asyncio, logging
import dashscope
from dashscope import Generation
from ruoyi_common.ruoyi.config import CONFIG_CACHE

# 配置日志
logger = logging.getLogger(__name__)


class AIProcessor:

    def __init__(self):
        """初始化千问模型"""
        try:
            api_key = CONFIG_CACHE.get('aicrawl.qwen.api_key')
            model_name = CONFIG_CACHE.get('aicrawl.qwen.model_name', 'qwen3-max')
            
            if not api_key or api_key == "your-api-key-here":
                raise ValueError("请在config.yaml中配置有效的千问API密钥")
            
            # 设置API密钥
            dashscope.api_key = api_key
            
            # 保存模型名称
            self.model_name = model_name
        except Exception as e:
            raise Exception(f"初始化千问模型失败: {str(e)}")
    
    def _call_qwen_model(self, prompt: str) -> str:
        """
        直接调用千问模型
        
        Args:
            prompt (str): 提示文本
        
        Returns:
            str: 模型返回的文本
        """
        try:
            response = Generation.call(
                model=self.model_name,
                prompt=prompt,
                max_tokens=64*1024,
                temperature=0.7
            )
            
            # 修复响应处理逻辑 - 适配dashscope API的实际返回格式
            if response.status_code == 200 and response.output and 'choices' in response.output:
                if response.output['choices'] and 'message' in response.output['choices'][0] and 'content' in response.output['choices'][0]['message']:
                    return response.output['choices'][0]['message']['content']
                else:
                    logger.error(f"响应结构不完整: {response}")
                    raise Exception(f"响应结构不完整: {response}")
            else:
                logger.error(f"模型调用失败: {response}")
                raise Exception(f"模型调用失败: {response}")
        except Exception as e:
            logger.error(f"调用千问模型时出错: {str(e)}")
            raise
    
    def analyze_user_info(self, name: str, email: str, phone: str) -> Dict[str, Any]:
        """
        使用千问大模型分析用户信息
        
        Args:
            name (str): 用户姓名
            email (str): 用户邮箱
            phone (str): 用户手机号
            
        Returns:
            dict: 包含分析结果的字典
        """
        try:
            # 创建提示
            prompt = f"""
            你是一个专业的信息分析师，请根据以下用户信息进行分析：
            
            姓名: {name}
            邮箱: {email}
            手机号: {phone}
            
            请提供以下信息的分析：
            1. 根据邮箱域名判断用户可能所在的行业或公司类型
            2. 根据手机号码判断用户可能所在的地区
            3. 对该用户进行一个简短的画像描述
            
            请以简洁明了的方式回答，不要超过200字。
            """
            
            # 调用模型
            analysis = self._call_qwen_model(prompt)
            
            return {
                "status": "success",
                "analysis": analysis
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"AI分析失败: {str(e)}"
            }
    
    def generate_user_summary(self, name: str, email: str, phone: str) -> Dict[str, Any]:
        """
        使用千问大模型生成用户摘要
        
        Args:
            name (str): 用户姓名
            email (str): 用户邮箱
            phone (str): 用户手机号
            
        Returns:
            dict: 包含用户摘要的字典
        """
        try:
            # 创建提示
            prompt = f"""
            请为以下用户生成一个简短的摘要：
            
            姓名: {name}
            邮箱: {email}
            手机号: {phone}
            
            摘要应包括：
            1. 用户标识信息
            2. 可能的联系方式有效性评估
            3. 简要的用户价值评估
            
            请以不超过100字的方式回答。
            """
            
            # 调用模型
            summary = self._call_qwen_model(prompt)
            
            return {
                "status": "success",
                "summary": summary
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"生成用户摘要失败: {str(e)}"
            }
    
    def extract_markdown_section(self, markdown_content: str, section_title: str, keywords: List[str] = None) -> Dict[str, Any]:
        """
        从Markdown内容中提取指定栏目下的内容，并解析为结构化数据
        
        Args:
            markdown_content (str): Markdown格式的内容
            section_title (str): 要提取的栏目标题
            keywords (List[str]): 用户关注的关键词列表
            
        Returns:
            dict: 包含提取结果的字典，每个元素包含标题、发布时间、链接
        """
        try:
            # 限制输入长度以避免超出模型限制
            # max_input_length = 128*1024
            # if len(markdown_content) > max_input_length:
            #     # 截取前max_input_length个字符，并添加提示
            #     markdown_content = markdown_content[:max_input_length] + "\n\n... (内容已截断)"
            #     logger.warning(f"输入内容已截断至{max_input_length}字符")
            
            # 创建提示
            prompt = f"""
            你是一个专业的数据提取专家，请从以下Markdown内容中提取"{section_title}"栏目下的所有条目信息。
            
            Markdown内容：
            {markdown_content}
            
            请按照以下要求提取信息：
            1. 只提取"{section_title}"栏目下的内容
            2. 对于每个条目，提取以下信息：
               - 标题
               - 发布时间（如果没有明确的发布时间，请标注为"未知"）
               - 链接（如果没有链接，请标注为"无"）
            3. 以严格的JSON格式返回结果，不要包含任何其他文本
            4. JSON格式应为：
            {{
              "status": "success",
              "data": [
                {{
                  "title": "标题1",
                  "publish_time": "发布时间1",
                  "link": "链接1"
                }},
                {{
                  "title": "标题2",
                  "publish_time": "发布时间2",
                  "link": "链接2"
                }}
              ]
            }}
            
            请严格按照上述格式返回结果，不要添加任何解释或额外文本。
            """
            # print(prompt)
            # 调用模型
            result_str = self._call_qwen_model(prompt)
            
            # 检查结果是否为空
            if not result_str or result_str.strip() == "":
                return {
                    "status": "error",
                    "message": "模型返回空结果"
                }
            
            # 尝试解析JSON结果
            try:
                # 确保结果是有效的JSON格式
                result_str = result_str.strip()
                result_json = json.loads(result_str)
                extracted_data = result_json.get("data", [])
                
                # 如果提供了关键词，则对匹配的条目进行详细内容提取
                if keywords and isinstance(keywords, list) and len(keywords) > 0:
                    # 过滤出标题中包含关键词的条目
                    filtered_data = []
                    for item in extracted_data:
                        title = item.get("title", "").lower()
                        # 检查标题是否包含任何关键词
                        if any(keyword.lower() in title for keyword in keywords):
                            # 如果有链接，则访问链接提取详细内容
                            link = item.get("link")
                            if link and link != "无":
                                try:
                                    # 将导入移到函数内部以避免循环导入
                                    from web_scraper import scrape_url_to_markdown
                                    
                                    # 使用异步事件循环运行抓取函数
                                    loop = asyncio.new_event_loop()
                                    asyncio.set_event_loop(loop)
                                    detail_result = loop.run_until_complete(scrape_url_to_markdown(link))
                                    loop.close()
                                    
                                    if detail_result.get("status") == "success":
                                        item["detail_content"] = detail_result.get("markdown", "")
                                    else:
                                        item["detail_content"] = f"无法获取详细内容: {detail_result.get('message', '未知错误')}"
                                except Exception as e:
                                    item["detail_content"] = f"获取详细内容时出错: {str(e)}"
                            else:
                                item["detail_content"] = "无链接可访问"
                            filtered_data.append(item)
                    
                    # 更新返回的数据为过滤后的数据
                    extracted_data = filtered_data
                
                return {
                    "status": "success",
                    "data": extracted_data
                }
            except json.JSONDecodeError as json_error:
                # 如果JSON解析失败，返回原始结果
                logger.error(f"JSON解析失败: {str(json_error)}")
                logger.error(f"原始结果: {result_str}")
                return {
                    "status": "error",
                    "message": f"JSON解析失败: {str(json_error)}",
                    "raw_result": result_str
                }
                
        except Exception as e:
            logger.error(f"提取Markdown栏目失败: {str(e)}")
            logger.exception(e)
            return {
                "status": "error",
                "message": f"提取Markdown栏目失败: {str(e)}"
            }

# 全局AI处理器实例
_ai_processor = None

def get_ai_processor() -> AIProcessor:
    """
    获取全局AI处理器实例
    
    Returns:
        AIProcessor: AI处理器实例
    """
    global _ai_processor
    if _ai_processor is None:
        _ai_processor = AIProcessor()
    return _ai_processor